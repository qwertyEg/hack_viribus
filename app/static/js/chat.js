document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const robotDog = document.querySelector('.robot-dog');
    let isProcessing = false;
    
    // Получаем CSRF токен
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (!csrfToken) {
        console.error('CSRF token not found');
        return;
    }
    
    // Функция для анимации робота-собачки
    function animateRobotDog(action) {
        const robot = robotDog.querySelector('.robot-body');
        robot.classList.remove('talking', 'listening', 'thinking');
        
        switch(action) {
            case 'talking':
                robot.classList.add('talking');
                break;
            case 'listening':
                robot.classList.add('listening');
                break;
            case 'thinking':
                robot.classList.add('thinking');
                break;
        }
    }
    
    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (isProcessing) return;
            
            const message = chatInput.value.trim();
            if (!message) return;
            
            isProcessing = true;
            chatInput.value = '';
            chatInput.disabled = true;
            
            // Добавляем сообщение пользователя в чат
            addMessage('user', message);
            
            // Анимируем робота-собачку
            animateRobotDog('listening');
            
            // Добавляем индикатор печати
            addTypingIndicator();
            
            try {
                // Отправляем запрос к API
                const response = await fetch('/api/chatbot/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ query: message })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                // Удаляем индикатор печати
                removeTypingIndicator();
                
                if (data.success) {
                    // Анимируем робота-собачку
                    animateRobotDog('talking');
                    
                    // Добавляем ответ бота в чат
                    addMessage('bot', data.response);
                    
                    // Если нужны уточнения, фокусируемся на поле ввода
                    if (data.needs_clarification) {
                        chatInput.focus();
                    }
                } else {
                    // Показываем ошибку
                    addMessage('error', data.error || 'Произошла ошибка при обработке запроса');
                }
            } catch (error) {
                removeTypingIndicator();
                console.error('Error:', error);
                addMessage('error', 'Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.');
            } finally {
                isProcessing = false;
                chatInput.disabled = false;
                chatInput.focus();
                
                // Возвращаем робота-собачку в исходное состояние
                setTimeout(() => {
                    animateRobotDog('listening');
                }, 1000);
            }
        });
    }
    
    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Прокручиваем чат вниз
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'message-content';
        typingContent.innerHTML = `
            <span class="typing-text">Думаю</span>
            <span class="typing-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </span>
            <span class="typing-emoji">✍️</span>
        `;
        
        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Анимируем робота-собачку
        animateRobotDog('thinking');
    }
    
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
}); 