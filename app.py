import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import io
import json  

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("API_KEY"))

def extract_text_from_pdf(file_stream):
    """Extract text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def analyze_email_with_ai_advanced(email_content):
    """
    Uses OpenAI API with an advanced prompt for full email analysis.
    """
    try:
        prompt = f"""
        You are an email analysis specialist for a financial company. Analyze the email below and return a JSON object.

        The JSON object must have the following structure:
        - "category": Classify the email as "Technical Support", "Financial Inquiry", "General", or "Unproductive".
        - "urgency": Classify urgency as "High", "Medium", or "Low".
        - "confidence": A number from 0.0 to 1.0 indicating your confidence in the category classification.
        - "entities": An object containing extracted information. If not found, return null for the field.
            - "sender_name": Name of the person or company that sent the email.
            - "ticket_number": Any protocol, ticket, or request ID.
            - "company": Name of the company mentioned, if any.
        - "suggested_response": A professional response in English based on category and content. For high urgency, response should be faster.

        Email to analyze:
        ---
        {email_content}
        ---

        Return ONLY the valid JSON object, without any extra text or explanation.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are an AI assistant specialized in email analysis and productivity."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        result_str = response.choices[0].message.content
        return json.loads(result_str) 

    except Exception as e:
        print(f"Error with OpenAI API or JSON processing: {e}")
        return {
            "error": "Unable to process the request via AI. Check the content or try again."
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_email():
    email_content = ""
    
    if 'email_text' in request.form and request.form['email_text']:
        email_content = request.form['email_text']
    elif 'email_file' in request.files:
        file = request.files['email_file']
        if file.filename != '':
            if file.filename.endswith('.txt'):
                email_content = file.read().decode('utf-8')
            elif file.filename.endswith('.pdf'):
                email_content = extract_text_from_pdf(io.BytesIO(file.read()))
                if email_content is None:
                    return jsonify({"error": "Unable to read PDF file."}), 400
        else:
             return jsonify({"error": "No email content provided."}), 400
    
    if not email_content:
        return jsonify({"error": "Email content is empty."}), 400

    ai_result = analyze_email_with_ai_advanced(email_content)
    

    if "error" in ai_result:
        return jsonify(ai_result), 500
        
    return jsonify(ai_result)


if __name__ == '__main__':
    app.run(debug=True)
