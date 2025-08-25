document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Saludo automático con animación
    setTimeout(() => {
        const welcomeMsg = "¡Hola! 👋 Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?";
        displayMessage(welcomeMsg, 'bot-message');
    }, 800);
    
    // Enviar mensaje con Enter
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Enviar mensaje con botón
    sendBtn.addEventListener('click', sendMessage);
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        displayMessage(message, 'user-message');
        userInput.value = '';
        
        // Mostrar "escribiendo..." mientras espera respuesta
        const typingIndicator = displayMessage("Escribiendo...", 'bot-message');
        typingIndicator.classList.add('typing');
        
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            chatBox.removeChild(typingIndicator);
            displayMessage(data.response, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
            chatBox.removeChild(typingIndicator);
            displayMessage("⚠️ Lo siento, hubo un error. Por favor intenta nuevamente.", 'bot-message');
        });
    }
    
    function displayMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        
        // Auto-scroll suave
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: 'smooth'
        });
        
        return messageElement;
    }
});