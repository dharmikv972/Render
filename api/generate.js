import { GoogleGenerativeAI } from "@google/generative-ai";

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

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { action, message } = req.body;

    if (!action || !message) {
      return res.status(400).json({ error: 'Action and message are required' });
    }

    try {
      const chatSession = model.startChat({
        generationConfig,
        history: [
          {
            role: "user",
            parts: [
              { text: message },
            ],
          },
        ],
      });

      const result = await chatSession.sendMessage(message);
      return res.status(200).json({ response: result.response.text() });
    } catch (error) {
      console.error('Error generating response:', error);
      return res.status(500).json({ error: 'Failed to generate response' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
