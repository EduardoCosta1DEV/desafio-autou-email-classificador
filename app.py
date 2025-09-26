import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import PyPDF2
import io
import json

# Importa a biblioteca do Google Gemini
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configura a API do Gemini com a chave do .env
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Erro ao configurar a API do Gemini. Verifique sua chave de API no .env: {e}")

def extrair_texto_do_pdf(fluxo_do_arquivo):
    """Extrai o texto de um arquivo PDF."""
    try:
        leitor = PyPDF2.PdfReader(fluxo_do_arquivo)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None

def analisar_email_com_ia(conteudo_email):
    """
    Usa a API do Google Gemini com um prompt avançado para análise completa do email.
    """
    # Usaremos o gemini-1.5-flash, que é rápido e poderoso.
    modelo = genai.GenerativeModel('gemini-2.5-flash')

    # Reutilizamos seu prompt, agora traduzido e pedindo um JSON em português.
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
        # A chamada para a API do Gemini é mais direta.
        resposta_api = modelo.generate_content(prompt)
        
        # O Gemini pode retornar o JSON dentro de ```json ... ```, então limpamos isso.
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
    conteudo_email = ""
    
    # Verifica se o texto foi enviado diretamente no formulário
    if 'email_text' in request.form and request.form['email_text']:
        conteudo_email = request.form['email_text']
    # Verifica se um arquivo foi enviado
    elif 'email_file' in request.files:
        arquivo = request.files['email_file']
        if arquivo.filename != '':
            if arquivo.filename.endswith('.txt'):
                conteudo_email = arquivo.read().decode('utf-8')
            elif arquivo.filename.endswith('.pdf'):
                conteudo_email = extrair_texto_do_pdf(io.BytesIO(arquivo.read()))
                if conteudo_email is None:
                    return jsonify({"erro": "Não foi possível ler o arquivo PDF."}), 400
        else:
            return jsonify({"erro": "Nenhum arquivo selecionado."}), 400
    
    if not conteudo_email:
        return jsonify({"erro": "Nenhum conteúdo de email fornecido."}), 400

    resultado_ia = analisar_email_com_ia(conteudo_email)

    if "erro" in resultado_ia:
        return jsonify(resultado_ia), 500
        
    return jsonify(resultado_ia)


if __name__ == '__main__':
    app.run(debug=True)