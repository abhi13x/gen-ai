const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendButton.click();
    }
});

function formatLLMResponse(text) {
    try {
        // Create a container for the formatted content
        const formattedText = document.createElement('div');
        // Split the text into parts (thinking and response)
        const thinkMatch = text.match(/<think>([\s\S]*?)<\/think>/);
        const mainContent = text.replace(/<think>[\s\S]*?<\/think>/, '').trim();
        // If there's a thinking block, add it
        if (thinkMatch) {
            const thinkContent = thinkMatch[1].trim();
            const thinkDiv = document.createElement('div');
            thinkDiv.className = 'think-block';
            thinkDiv.textContent = thinkContent;
            formattedText.appendChild(thinkDiv);
        }

        // Add the main response content
        if (mainContent) {
            const contentDiv = document.createElement('div');
            contentDiv.className = 'response-content';
            // Format the content with markdown and other styling
            let formattedContent = mainContent
                //Bold Text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                // Italic Text
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                // Line Breaks
                .replace(/\n/g, '<br>');
            contentDiv.innerHTML = formattedContent;
            formattedText.appendChild(contentDiv);
        }
        return formattedText.innerHTML;
    }
    catch (error) {
        console.error('Error formatting response:', error);
        // If there's an error, return the original text
        return text;
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    // Disable input and button while processing
    userInput.disabled = true;
    sendButton.disabled = true;
    // Add user message
    addMessage(message, 'user');
    userInput.value = '';
    // Show typing indicator and scroll
    typingIndicator.style.display = 'flex';
    scrollToBottom();

    try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        if (!response.ok) {
            throw new Error('Failed to get response from server');
        }
        const data = await response.json();
        // Hide typing indicator and add formatted but response
        typingIndicator.style.display = 'none';
        addMessage(data.response, 'bot', true);
    }
    catch (error) {
        typingIndicator.style.display = 'none';
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        console.error('Error sending message:', error);
    }

    // Re-enable input and button
    userInput.disabled = false;
    sendButton.disabled = false;
    userInput.focus();
};

function addMessage(text, sender, format = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    try {
        if (format && sender === 'bot') {
            contentDiv.innerHTML = formatLLMResponse(text);
        }
        else {
            contentDiv.textContent = text;
        }
    }
    catch (error) {
        console.error('Error in addMessage:', error);
        contentDiv.textContent = text;
    }
    messageDiv.appendChild(contentDiv);
    chatMessages.insertBefore(messageDiv, typingIndicator);
    scrollToBottom();
};

function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}