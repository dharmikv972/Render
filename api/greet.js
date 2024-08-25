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
startChat();

export default function handler(req, res) {
  if (req.method === 'POST') {
    const { name } = req.body;

    if (!name || typeof name !== 'string') {
      return res.status(400).json({ error: 'Name is required and must be a string' });
    }

    const greeting = `Hello, ${name}! Nice to meet you.`;

    return res.status(200).json({ greeting });
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
