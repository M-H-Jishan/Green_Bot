// Function to fetch images from the server
async function fetchImages() {
    try {
        const response = await fetch('http://localhost:5000/images');
        if (!response.ok) {
            throw new Error('Failed to fetch images');
        }
        const images = await response.json();
        displayImages(images);
    } catch (error) {
        console.error('Error fetching images:', error);
        document.getElementById('imageGrid').innerHTML = '<p class="error">Failed to load images. Please try again later.</p>';
    }
}

// Function to display images in the grid
function displayImages(images) {
    const imageGrid = document.getElementById('imageGrid');
    imageGrid.innerHTML = '';

    images.forEach(image => {
        const imageCard = document.createElement('div');
        imageCard.className = 'image-card';

        const img = document.createElement('img');
        img.src = `http://localhost:5000${image.path}`;
        img.alt = image.name || 'Image';
        img.loading = 'lazy';

        img.addEventListener('load', function() {
            console.log('Image loaded successfully');
        });
        
        img.addEventListener('error', function() {
            console.error('Error loading image');
            img.style.display = 'none';
            img.parentElement.innerHTML = '<p style="text-align: center; color: red;">Error loading image</p>';
        });

        imageCard.appendChild(img);
        imageGrid.appendChild(imageCard);
    });
}

// Function to handle chat bot responses
async function getChatbotResponse(message) {
    try {
        const response = await fetch('http://localhost:8000/api/chatbot/ask/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })  
        });

        const data = await response.json();
        
        if (!response.ok) {
            console.error('Server error:', data);
            throw new Error(data.error || 'Server error');
        }

        return data.response;
    } catch (error) {
        console.error('Error getting chatbot response:', error);
        throw error;
    }
}

// Function to toggle chat window
function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
    if (chatWindow.style.display === 'block') {
        document.getElementById('userInput').focus();
    }
}

// Function to handle key press in input
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Function to show typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message typing-indicator';
    typingIndicator.id = 'typingIndicator';
    typingIndicator.innerHTML = `
        <div class="typing">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Function to get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Function to append message to chat
function appendMessage(message, isUser = false, isError = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    if (isError) messageDiv.classList.add('error-message');
    
    const time = getCurrentTime();
    messageDiv.innerHTML = `<span class="message-time">${time}</span>${message}`;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send message
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (message.length === 0) return;
    
    // Clear input
    userInput.value = '';
    
    // Append user message
    appendMessage(message, true);
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Get bot response
        const response = await getChatbotResponse(message);
        hideTypingIndicator();
        appendMessage(response);
    } catch (error) {
        hideTypingIndicator();
        appendMessage('Sorry, I encountered an error. Please try again.', false, true);
    }
}

// Load images when the page loads
document.addEventListener('DOMContentLoaded', fetchImages);

// Focus input when chat window is opened
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });
});