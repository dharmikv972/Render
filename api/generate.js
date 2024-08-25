// api/ai-chat.js

const { GoogleGenerativeAI } = require('@google/generative-ai');

const apiKey = "AIzaSyDEDNIwl3aMAT5l_Q-_SOWlFUyNY-d1UBE";
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: "gemini-1.5-pro-exp-0801",
});

const generationConfig = {
  temperature: 1,
  topP: 0.95,
  topK: 64,
  maxOutputTokens: 8192,
  responseMimeType: "text/plain",
};

let chatSession;

async function startChat() {
  chatSession = await model.startChat({
    generationConfig,
    history: [
      {
        role: "user",
        parts: [
          { text: "Here's a Python function that sorts a list of numbers in ascending order..." } // Example input
        ],
      },
      {
        role: "model",
        parts: [
          { text: "## Time Complexity Analysis..." } // Example response
        ],
      },
    ],
  });
}

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { action, message } = req.body;

    if (action === 'start') {
      try {
        await startChat();
        return res.status(200).json({ success: true, message: 'Chat session started' });
      } catch (error) {
        console.error("Error starting chat:", error.message);
        return res.status(500).json({ error: 'Failed to start chat session' });
      }
    } else if (action === 'send' && message) {
      try {
        if (!chatSession) {
          return res.status(400).json({ error: 'Chat session not started' });
        }
        const result = await chatSession.sendMessage(message);
        const responseText = await result.response.text();

        return res.status(200).json({ message: responseText });
      } catch (error) {
        console.error("Error sending message:", error.message);
        return res.status(500).json({ error: 'Failed to send message' });
      }
    } else {
      res.setHeader('Allow', ['POST']);
      return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
