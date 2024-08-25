import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "@google/generative-ai";


 const API_KEY = "AIzaSyDEDNIwl3aMAT5l_Q-_SOWlFUyNY-d1UBE";

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { name } = req.body;

      if (!name || typeof name !== 'string') {
        return res.status(400).json({ error: 'Name is required and must be a string' });
      }

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

      // Initialize the AI client and model
      const genAI = new GoogleGenerativeAI(API_KEY);
      const model = genAI.getGenerativeModel({
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

      // Start a chat session with the AI model
      const chat = await model.startChat({
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

      // Send a message to the chat
      const result = await chat.sendMessage(name);
      const responseText = await result.response.text();

      // Prepare and send the response
      const greeting = responseText;
      return res.status(200).json({ greeting });

    } catch (error) {
      console.error('Error in handler:', error);
      return res.status(500).json({ error: 'Internal Server Error' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
