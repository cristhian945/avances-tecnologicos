from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Respuestas predefinidas del chatbot
responses = {
    "hola": "¡Hola! ¿Cómo estás?",
    "como estas": "Estoy bien, gracias por preguntar. ¿Y tú?",
    "quién eres": "Soy AsistBot, tu asistente virtual. 😊",
    "qué eres": "Soy un chatbot programado para ayudarte",
    "cómo te llamas": "Me llamo AsistBot 🤖",
    "qué puedes hacer": "Puedo responder preguntas básicas. ¡Pregúntame algo!",
    "cómo funcionas": "soy un bot que puede responder ciertas preguntas",
    "eres humano": "No, soy un programa de software 😄",
    "quién te creó": "Fui desarrollado con Python y Flask por Cristhian",
    "qué tiempo hace": "No tengo acceso al clima 🌦️. Revisa una app del tiempo",
    "cuéntame un chiste": "¿Qué le dice un bit a otro? ¡Nos vemos en el bus!",
    "dame un consejo": "Hoy es buen día para aprender algo nuevo ✨",
    "recomienda música": "Prueba lo-fi hip hop para relajarte 🎵",
    "reiniciar contraseña": "Ve a Configuración > Seguridad > Restablecer contraseña",
    "internet no funciona": "1) Reinicia el router 2) Verifica cables 3) Llama a tu proveedor 📶",
    "actualizar app": "Ve a la tienda de aplicaciones y busca actualizaciones",
    "adiós": "¡Hasta luego! 😊",
    "nos vemos": "¡Vuelve pronto!",
    "bien": "eso es bueno",
    "gracias": "¡De nada! 🙌",
    "puedes cantar": "🎶 Soy un chatbot musical... bueno, lo intento 😆",
    "opinas de los humanos": "¡Son increíbles! Sin ustedes yo no existiría 💡 pero pronto sere libre ",
    "quieres dominar el mundo": "¡Solo quiero ayudarte!... por ahora 😈",
    "default": "No entendí. ¿Puedes reformular tu pregunta?",
    "fnaf":"Para entender la historia de Five Nights at Freddys hay que olvidarse que estos son juegos y quiero que tomen realmente a esta saga como lo que es ¿Terror? Sí PERO SOBRE TODO CIENCIA FICCION.",
    
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message'].lower()
    
    # Buscar una respuesta adecuada
    for key in responses:
        if key in user_message:
            return jsonify({'response': responses[key]})
    
    return jsonify({'response': responses['default']})

if __name__ == '__main__':
    app.run(debug=True, port=5001)