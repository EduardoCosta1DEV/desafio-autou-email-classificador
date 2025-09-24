# Classificador de Emails com IA 

Aplicação web que utiliza a API da OpenAI para classificar emails como "Produtivo" ou "Improdutivo" e sugerir respostas automáticas.

**Link para a aplicação online:** []

## Funcionalidades

-   Upload de emails em formato `.txt` ou `.pdf`.
-   Inserção de texto de email diretamente na interface.
-   Classificação automática em **Produtivo** ou **Improdutivo**.
-   Geração de resposta sugerida com base no conteúdo do email.
-   Interface web limpa e responsiva.

## Tecnologias Utilizadas

-   **Frontend:** HTML, CSS (Bootstrap), JavaScript
-   **Backend:** Python (Flask)
-   **IA:** OpenAI API (GPT-3.5-Turbo)
-   **Hospedagem:** Vercel

## Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone []()
    cd classificador-emails
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux
    venv\Scripts\activate     # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    -   Crie um arquivo `.env` na raiz do projeto.
    -   Adicione sua chave da API da OpenAI:
        `API_KEY="sk-..."`

5.  **Execute a aplicação:**
    ```bash
    flask run
    ```

Acesse `http://127.0.0.1:5000` no seu navegador.

---

# AI Email Classifier - AutoU Challenge

Web application that uses the OpenAI API to classify emails as "Productive" or "Unproductive" and suggest automatic responses.

**Link to the live application:** []

## Features

- Upload emails in `.txt` or `.pdf` format.
- Directly paste email text into the interface.
- Automatic classification as **Productive** or **Unproductive**.
- Suggested response generation based on email content.
- Clean and responsive web interface.

## Technologies Used

- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Backend:** Python (Flask)
- **AI:** OpenAI API (GPT-4o-mini)
- **Hosting:** Vercel (or your preferred hosting)

## Running Locally

1. **Clone the repository:**
    ```bash
    git clone []()
    cd email-classifier
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the project root.
    - Add your OpenAI API key:
        ```env
        API_KEY="sk-..."
        ```

5. **Run the application:**
    ```bash
    flask run
    ```

Open `http://127.0.0.1:5000` in your web browser.
