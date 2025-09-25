import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import PyPDF2
import io
import json
from PyPDF2.errors import PdfReadError


import google.generativeai as genai


load_dotenv()

app = Flask(__name__)

try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Erro ao configurar a API do Gemini. Verifique sua chave de API no .env: {e}")

def extrair_texto_do_pdf(fluxo_do_arquivo):
    """Extrai o texto de um arquivo PDF com tratamento de erros aprimorado."""
    try:
        leitor = PyPDF2.PdfReader(fluxo_do_arquivo)

        # Verifica se o PDF está criptografado (protegido por senha)
        if leitor.is_encrypted:
            print("Erro de leitura: O arquivo PDF está protegido por senha.")
            return None

        texto = ""
        for pagina in leitor.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto += texto_pagina
        
        # Se nenhum texto foi extraído, pode ser um PDF de imagem
        if not texto.strip():
            print("Aviso: Nenhum texto encontrado no PDF (pode ser um arquivo de imagem).")
            return None
            
        return texto
        
    except PdfReadError:
        print("Erro de leitura: O arquivo parece ser um PDF corrompido ou inválido.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao processar o PDF: {e}")
        return None

def analisar_email_com_ia(conteudo_email):
    """
    Usa a API do Google Gemini com um prompt avançado para análise completa do email.
    """
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Você é um especialista em análise de emails para uma empresa financeira. Analise o email abaixo e retorne um objeto JSON.

    O objeto JSON deve ter a seguinte estrutura:
    - "categoria": Classifique o email como "Suporte Técnico", "Questão Financeira", "Geral", ou "Improdutivo".
    - "urgencia": Classifique a urgência como "Alta", "Média", ou "Baixa".
    - "confianca": Um número de 0.0 a 1.0 indicando sua confiança na classificação da categoria.
    - "entidades": Um objeto contendo informações extraídas. Se não encontrar, retorne null para o campo.
        - "remetente": Nome da pessoa ou empresa que enviou o email.
        - "numero_ticket": Qualquer protocolo, ticket ou ID de solicitação.
        - "empresa": Nome da empresa mencionada, se houver.
    - "resposta_sugerida": Uma resposta profissional em português baseada na categoria e no conteúdo. Para urgência alta, a resposta deve ser mais rápida.

    Email para analisar:
    ---
    {conteudo_email}
    ---

    Retorne APENAS o objeto JSON válido, sem nenhum texto ou explicação extra.
    """

    try:
        resposta_api = modelo.generate_content(prompt)
        
        resultado_texto = resposta_api.text.replace("```json", "").replace("```", "").strip()
        return json.loads(resultado_texto)

    except Exception as e:
        print(f"Erro com a API do Gemini ou no processamento do JSON: {e}")
        return {
            "erro": "Não foi possível processar a solicitação via IA. Verifique o conteúdo ou tente novamente."
        }


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/processar', methods=['POST'])
def processar_email():
    conteudo_email = None # Começamos com None para garantir
    
    # 1. Tenta pegar o conteúdo do formulário de texto
    texto_digitado = request.form.get('email_text', '').strip()
    if texto_digitado:
        conteudo_email = texto_digitado
    
    # 2. Se não houver texto, tenta pegar do arquivo
    elif 'email_file' in request.files:
        arquivo = request.files['email_file']
        
        # Verifica se um arquivo foi realmente selecionado
        if arquivo and arquivo.filename:
            if arquivo.filename.endswith('.txt'):
                try:
                    conteudo_email = arquivo.read().decode('utf-8')
                except Exception as e:
                    print(f"Erro ao ler arquivo .txt: {e}")
                    return jsonify({"erro": "Não foi possível ler o arquivo .txt."}), 400
            
            elif arquivo.filename.endswith('.pdf'):
                conteudo_email = extrair_texto_do_pdf(io.BytesIO(arquivo.read()))
                # A função 'extrair_texto_do_pdf' já retorna None em caso de erro
                if conteudo_email is None:
                    mensagem_erro = "Não foi possível extrair texto do PDF. O arquivo pode estar corrompido, protegido por senha ou ser apenas uma imagem."
                    return jsonify({"erro": mensagem_erro}), 400
        else:
             # Este caso ocorre se o campo de arquivo existe mas está vazio
             return jsonify({"erro": "Nenhum arquivo foi selecionado."}), 400

    # 3. Verificação final: se depois de tudo, não temos conteúdo, retorne um erro.
    if not conteudo_email or not conteudo_email.strip():
        return jsonify({"erro": "Nenhum conteúdo de email válido foi fornecido."}), 400

    # 4. Se chegamos até aqui, temos um conteúdo válido para analisar
    print("Enviando conteúdo para análise da IA...")
    resultado_ia = analisar_email_com_ia(conteudo_email)

    if "erro" in resultado_ia:
        return jsonify(resultado_ia), 500
        
    return jsonify(resultado_ia)


if __name__ == '__main__':
    app.run(debug=True)