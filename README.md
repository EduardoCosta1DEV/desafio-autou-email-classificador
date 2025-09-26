# 🚀 Analisador Inteligente de E-mails com IA (Desafio AutoU)

Uma aplicação web avançada que utiliza a API do Google Gemini para realizar uma análise completa de e-mails, extraindo dados, classificando conteúdo e sugerindo respostas contextuais.

**Link para a aplicação online:** `[COLE AQUI O LINK DA SUA APLICAÇÃO DO RENDER]`

## ✨ Funcionalidades

-   **Upload de Arquivos:** Envio de e-mails em formato `.txt` ou `.pdf`.
-   **Análise por Texto:** Inserção de texto de e-mail diretamente na interface.
-   **Classificação Avançada:** O conteúdo é classificado em múltiplas categorias ("Suporte Técnico", "Questão Financeira", etc.).
-   **Análise de Urgência:** Determina a urgência da mensagem como "Alta", "Média" ou "Baixa".
-   **Extração de Entidades:** Identifica e extrai informações importantes como nome do remetente, número de ticket e nomes de empresas.
-   **Geração de Resposta:** A IA sugere uma resposta profissional em português, adaptada ao contexto e à urgência do e-mail.
-   **Interface Moderna:** Interface limpa, intuitiva e agradável.

## 🛠️ Tecnologias e Ferramentas

-   **Frontend:** HTML5, CSS3, JavaScript (ES6+)
-   **Backend:** Python 3, Flask, Gunicorn
-   **Inteligência Artificial:** Google Gemini API (modelo `gemini-2.5-flash`)
-   **Bibliotecas Principais:** `google-generativeai`, `PyPDF2`, `python-dotenv`
-   **Hospedagem:** Render.com

## ⚙️ Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No Mac/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Adicione sua chave da API do Google Gemini:
        ```env
        GEMINI_API_KEY="SUA_CHAVE_GEMINI_AQUI"
        ```

5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

Acesse `http://127.0.0.1:5000` no seu navegador.

---

# 🚀 Intelligent AI Email Analyzer (AutoU Challenge)

An advanced web application that leverages the Google Gemini API to perform a complete analysis of emails, extracting data, classifying content, and suggesting contextual responses.

**Link to the live application:** `[PASTE YOUR RENDER APP LINK HERE]`

## ✨ Features

-   **File Upload:** Submit emails in `.txt` or `.pdf` format.
-   **Text Analysis:** Paste email text directly into the interface.
-   **Advanced Classification:** Content is classified into multiple categories ("Technical Support", "Financial Inquiry", etc.).
-   **Urgency Analysis:** Determines the message urgency as "High", "Medium", or "Low".
-   **Entity Extraction:** Identifies and extracts key information such as sender name, ticket number, and company names.
-   **Response Generation:** The AI suggests a professional response in Portuguese, tailored to the email's context and urgency.
-   **Modern Interface:** A clean, intuitive, and pleasant user interface.

## 🛠️ Technologies & Tools

-   **Frontend:** HTML5, CSS3, JavaScript (ES6+)
-   **Backend:** Python 3, Flask, Gunicorn
-   **Artificial Intelligence:** Google Gemini API (`gemini-1.5-flash` model)
-   **Key Libraries:** `google-generativeai`, `PyPDF2`, `python-dotenv`
-   **Hosting:** Render.com

## ⚙️ Running Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-user/your-repo.git](https://github.com/your-user/your-repo.git)
    cd your-repo
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a file named `.env` in the project root.
    -   Add your Google Gemini API key:
        ```env
        GEMINI_API_KEY="YOUR_GEMINI_KEY_HERE"
        ```

5.  **Run the application:**
    ```bash
    python app.py
    ```

Access `http://127.0.0.1:5000` in your browser.