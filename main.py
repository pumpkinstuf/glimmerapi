from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

import os

load_dotenv()
#pip install -r requirements.txt

app = Flask(__name__)
port = int(os.getenv("PORT", 3000))

genai.configure(api_key=os.getenv("API_KEY"))
text_generation_config = {
    "temperature": 1.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=text_generation_config, safety_settings=safety_settings)
access_key = os.getenv("ACCESS_KEY", "GLIMMERTEMP")

@app.route("/api/v1/endpoints/shimmer", methods=["POST"])
def shimmer():
    if request.json.get("accessKey") == access_key:
        try:
            response = gemini_model.generate_content(request.json.get("prompt"))
            if response._error:
                return str(response._error), 500
            print(jsonify(response.text))
            return jsonify(response.text)
        except Exception as error:
            return str(error), 500
    else:
        return "403 Forbidden", 403

if __name__ == "__main__":
    print(f"Glimmer Server starting on port {port}")
    app.run(port=port)
