from flask import Flask, render_template, request, jsonify
from datetime import datetime
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')

print(f"🔑 GEMINI_API_KEY cargada: {bool(GEMINI_API_KEY)}")
print(f"🔑 DEEPSEEK_API_KEY cargada: {bool(DEEPSEEK_API_KEY)}")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")

responses = {
    "hola": "¡Hola! ¿En qué puedo ayudarte?",
    "qué puedes hacer": "Puedo responder preguntas con la ayuda de IA avanzada",
    "qué hora es": f"Son las {datetime.now().strftime('%H:%M')}",
    "cuéntame un chiste": "¿Qué dice un semáforo a otro? ¡No me mires, me estoy cambiando! 😆",
    "adiós": "¡Hasta luego! 💻",
    "default": "No entendí. ¿Puedes reformular tu pregunta?"
}

def ask_gemini(user_message):
    """Consulta real a Gemini"""
    if not GEMINI_API_KEY:
        return "Gemini API Key no configurada."
    try:
        response = gemini_model.generate_content(user_message)
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        print(f"❌ Error consultando Gemini: {e}")
        return "Error consultando Gemini"

def ask_deepseek(user_message):
    """Consulta real a DeepSeek (requiere endpoint y API key)"""
    if not DEEPSEEK_API_KEY:
        return "DeepSeek API Key no configurada."
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        # Ajusta el path según la respuesta real de la API
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error consultando DeepSeek: {e}")
        return "Error consultando DeepSeek"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_message = request.form['message'].lower()
        ai_selected = request.form.get('ai_type', 'auto')
        
        print(f"📩 Mensaje recibido: '{user_message}'")
        print(f"🎯 IA seleccionada: '{ai_selected}'")
       
        for key in responses:
            if key in user_message:
                print(f"✅ Usando respuesta predefinida para: {key}")
                return jsonify({'response': responses[key]})
        
        bot_response = None
        
        if ai_selected == 'predefinido':
            print("🔧 Modo predefinido seleccionado")
            bot_response = responses['default']
        
        elif ai_selected == 'gemini':
            print("🔧 Solicitando Gemini...")
            bot_response = ask_gemini(user_message)
        
        elif ai_selected == 'deepseek':
            print("🔧 Solicitando DeepSeek...")
            bot_response = ask_deepseek(user_message)
        
        else:  # Modo automático
            print("🔧 Modo automático... usando Gemini")
            bot_response = ask_gemini(user_message)
        
        print(f"📤 Enviando respuesta: {bot_response}")
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"💥 Error grave: {e}")
        return jsonify({'response': "Error interno del servidor"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)