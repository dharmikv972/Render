



 const safetySettings = [
      {
        category: HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold: HarmBlockThreshold.BLOCK_NONE,
      },
      {
        category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold: HarmBlockThreshold.BLOCK_NONE,
      },
      {
        category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold: HarmBlockThreshold.BLOCK_NONE,
      },
      {
        category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold: HarmBlockThreshold.BLOCK_NONE,
      },
    ];

    const instructions = `Imagine you're a helpful but impatient older brother...`;

    import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "https://esm.run/@google/generative-ai";

    const genAI = new GoogleGenerativeAI("AIzaSyBwa_QW5ejTYfjRNLbAF9Lk9eG5s-rYaqU");
    let model;
    let chat;

    async function startChat() {
      try {
        model = genAI.getGenerativeModel({
          model: "gemini-1.5-flash",
          generationConfig: {
            temperature: 0.7,
            topP: 0.95,
            topK: 64,
            maxOutputTokens: 80,
            responseMimeType: "text/plain",
          },
          systemInstruction: instructions,
          safetySettings,
        });
        chat = await model.startChat({
          history: [
            {
              role: "user",
              parts: [{ text: "Hello" }],
            },
            {
              role: "model",
              parts: [{ text: "Great to meet you. What would you like to know?" }],
            },
          ],
        });
      } catch (error) {
        console.error("Error starting chat:", error);
      }
    }

    startChat();
const inputArea = document.querySelector('.input-area');
    const inputField = document.getElementById('input-field');
    const sendButton = document.getElementById('send-button');
    const messageArea = document.getElementById('message-area');
    const clearChatButton = document.getElementById('clear-chat');

    const messages = JSON.parse(localStorage.getItem('chatHistory')) || [];

    function renderMessages() {
      messageArea.innerHTML = '';
      messages.forEach(({ type, content }) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.innerHTML = content;
        messageArea.appendChild(messageDiv);
      });
      
      window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  });
    }

    renderMessages();

    async function sendMessage() {
      const userInput = inputField.value.trim();
      if (!userInput) return;

      inputField.value = '';
      messages.push({ type: 'sent', content: userInput });
      renderMessages();

      try {
        const result = await chat.sendMessage(userInput);
        const responseText = marked.parse(await result.response.text());
        messages.push({ type: 'received', content: responseText });
        renderMessages();
        localStorage.setItem('chatHistory', JSON.stringify(messages));
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }

    sendButton.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    clearChatButton.addEventListener('click', () => {
      localStorage.removeItem('chatHistory');
      messages.length = 0;
      renderMessages();
    });
   let prevScrollpos = window.pageYOffset;

    window.onscroll = function() {
      let currentScrollPos = window.pageYOffset;

      if (prevScrollpos > currentScrollPos) {
        inputArea.classList.remove('hide');
      } else {
        inputArea.classList.add('hide');
      }
      prevScrollpos = currentScrollPos;
    }
