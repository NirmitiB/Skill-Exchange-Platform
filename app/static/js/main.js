// Main JavaScript file for SkillSwap

document.addEventListener('DOMContentLoaded', function () {
    // Add subtle hover effects to skill cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('shadow-lg');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('shadow-lg');
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Chatbot functionality
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotBox = document.getElementById('chatbot-box');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    if (chatbotToggle && chatbotBox) {
        chatbotToggle.addEventListener('click', () => {
            chatbotBox.classList.toggle('d-none');
        });

        chatbotClose.addEventListener('click', () => {
            chatbotBox.classList.add('d-none');
        });

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message to UI
            addMessage(message, 'user');
            chatInput.value = '';

            // Show typing indicator
            const typingId = addMessage('...', 'bot typing');

            try {
                const response = await fetch('/chatbot/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();

                // Remove typing indicator and add bot response
                const typingEl = document.getElementById(typingId);
                if (typingEl) typingEl.remove();
                addMessage(data.response, 'bot');
            } catch (error) {
                console.error('Chat error:', error);
                const typingEl = document.getElementById(typingId);
                if (typingEl) typingEl.remove();
                addMessage("Sorry, I'm having trouble connecting. Please try again later.", 'bot text-danger');
            }
        });
    }

    function addMessage(text, type) {
        const id = 'msg-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = `chat-message ${type} mb-3 d-flex ${type === 'user' ? 'justify-content-end' : 'justify-content-start'}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = `d-inline-block p-2 rounded shadow-sm small ${type === 'user' ? 'bg-primary text-white' : 'bg-white text-dark'}`;
        contentDiv.innerText = text;

        div.appendChild(contentDiv);
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }
});
