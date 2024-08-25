document.addEventListener('DOMContentLoaded', function() {
  const inputArea = document.querySelector('.input-area');
  const inputField = document.getElementById('input-field');
  const sendButton = document.getElementById('send-button');
  const messageArea = document.getElementById('message-area');
  const clearChatButton = document.getElementById('clear-chat');
renderMessages();
  let messages = JSON.parse(localStorage.getItem('chatHistory')) || [];

  function createMessageElement(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.textContent = content;
    return messageDiv;
  }

  function renderMessages() {
    messageArea.innerHTML = '';
    messages.forEach(({ type, content }) => {
      const messageDiv = createMessageElement(type, content);
      messageArea.appendChild(messageDiv);
    });

    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  }

  async function sendMessage() {
    const userInput = inputField.value.trim();
    if (!userInput) return;

    inputField.value = '';
    messages.push({ type: 'sent', content: userInput });
    renderMessages();

    try {
      const response = await fetch('/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: userInput }),
      });

      if (response.ok) {
        const result = await response.json();
        messages.push({ type: 'received', content: result.greeting });
        renderMessages();
        localStorage.setItem('chatHistory', JSON.stringify(messages));
      } else {
        messages.push({ type: 'error', content: 'Failed to get a response' });
        renderMessages();
      }
    } catch (error) {
      messages.push({ type: 'error', content: 'An error occurred' });
      renderMessages();
      console.error("Error sending message:", error);
    }
  }

  function clearChatHistory() {
    localStorage.removeItem('chatHistory');
    messages = [];
    renderMessages();
  }

  
  sendButton.addEventListener('click', sendMessage);
  inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  clearChatButton.addEventListener('click', clearChatHistory);
  window.addEventListener('scroll', handleScroll);

  // Render messages on page load
  renderMessages();
});
