document.addEventListener('DOMContentLoaded', () => {
  const inputField = document.getElementById('input-field');
  const sendButton = document.getElementById('send-button');
  const messageArea = document.getElementById('message-area');
  const clearChatButton = document.getElementById('clear-chat');

  let messages = JSON.parse(localStorage.getItem('chatHistory')) || [];

  function createMessageElement(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.textContent = content;
    return messageDiv;
  }

  function renderMessages() {
    // Use DocumentFragment for efficient DOM manipulation
    const fragment = document.createDocumentFragment();
    messages.forEach(({ type, content }) => {
      fragment.appendChild(createMessageElement(type, content));
    });
    messageArea.innerHTML = ''; // Clear existing messages
    messageArea.appendChild(fragment); // Append new messages

    // Smooth scroll to the bottom of the message area
    messageArea.scrollTop = messageArea.scrollHeight;
  }

  async function sendMessage() {
    const userInput = inputField.value.trim();
    if (!userInput) return;

    inputField.value = ''; // Clear input field
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
        localStorage.setItem('chatHistory', JSON.stringify(messages));
      } else {
        throw new Error('Failed to get a response');
      }
    } catch (error) {
      messages.push({ type: 'error', content: `Error: ${error.message}` });
    } finally {
      renderMessages();
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

  // Render messages on page load
  renderMessages();
});
