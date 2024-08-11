import os
import pandas as pd
import fitz
import json
from flask import Flask, request, jsonify, render_template
from flask_session import Session
from dotenv import load_dotenv
# from ollama import Ollama3
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

extracted_text = ""

def extract_text(file, file_format):
    text = ""
    if file_format == 'csv':
        data = pd.read_csv(file)
        text = data.to_string()
    elif file_format == 'pdf':
        pdf_document = fitz.open(stream=file.read(), filetype='pdf')
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    elif file_format == 'json':
        data = json.load(file)
        text = json.dumps(data, indent=2)
    return text

def split_text(text, max_tokens=1000):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(current_chunk) + len(word.split()) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global extracted_text
    file = request.files['file']
    file_format = file.filename.split('.')[-1].lower()
    extracted_text = extract_text(file, file_format)
    
    return jsonify({"message": "File uploaded and text extracted successfully."})

@app.route('/ask', methods=['POST'])
def ask_question():
    global extracted_text
    if not extracted_text:
        return jsonify({"error": "No text has been extracted. Please upload a file first."}), 400
    
    data = request.json
    question = data['question']

    text_chunks = split_text(extracted_text, max_tokens=1000)  # Adjust the max_tokens as needed
    answers = []

    for chunk in text_chunks:
        
        prompt = f"""
        You are a knowledgeable and experienced assistant specializing exclusively in finance.
        Your task is to assist with finance-related queries only.
        You have been provided with a document in text format, which may originate from different formats such as CSV, JSON, or PDF.
        First, determine whether the document is related to finance. If the document is not related to finance, respond with:
        The document provided does not pertain to finance. Please upload an appropriate finance-related document.
        when uploded or provided document is not related to finance, then do not read it further and respond with:
        please provide an appropriate finance-related document.
        If the document is related to finance, extract the relevant content and provide a clear and accurate answer to the question based on the content of the document.
        Your generated answer must be summarized and short.
        Please avoid providing answers that are not directly related to finance. Ensure that each response is unique and non-repetitive.
        Here is the content of the document:
        {chunk}
        Based on the information provided in the document above, please answer the following question:
        {question}
        Provide a clear and accurate answer based on the content of the document, ensuring that the response is unique and not repeated.
        """

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )

        # Extract the response content
        answer = response.choices[0].message.content
        answers.append(answer)
    
    # Filter out duplicate answers
    unique_answers = list(dict.fromkeys(answers))  # Preserve order and remove duplicates
    
    
    # Combine unique answers
    combined_answer = " ".join(unique_answers)
    return jsonify({"answer": combined_answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
