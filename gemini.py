import os
from flask import Flask, request, jsonify, render_template_string
from google.cloud import aiplatform
import google.generativeai as genai

app = Flask(__name__)

API_KEY = "AIzaSyC9uXy92lQX2knCanapxwVfEHRixkpG8rM"
genai.configure(api_key=API_KEY)

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Generation App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            background-color: #007bff;
            color: #fff;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .response {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Generation</h1>
        <textarea id="prompt" placeholder="Enter your prompt here..."></textarea>
        <button onclick="generateText()">Generate</button>
        <div class="response" id="response"></div>
    </div>

    <script>
        async function generateText() {
            const prompt = document.getElementById('prompt').value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = 'Generating...';

            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();
            if (data.response) {
                responseDiv.innerHTML = data.response;
            } else {
                responseDiv.innerHTML = 'Error: ' + data.error;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/generate', methods=['POST'])
def generate_text():
    prompt = request.json['prompt']
    try:
        response = genai.generate_text(prompt=prompt)
        generated_text = response.result if hasattr(response, 'result') else 'No result found in response'
        return jsonify({'response': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    app.run(debug=True)
