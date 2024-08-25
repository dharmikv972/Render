import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold  } from "@google/generative-ai";

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { name } = req.body;

    if (!name || typeof name !== 'string') {
      return res.status(400).json({ error: 'Name is required and must be a string' });
    }

    // Example usage of Google Generative AI (if needed)
    const genAI = new GoogleGenerativeAI(process.env.API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    // Uncomment and adjust if you need to use safety settings and make actual AI requests
     const safetySettings = [
      {
        category: HarmCategory.HARM_CATEGORY_HARASSMENT,
    /   threshold: HarmBlockThreshold.BLOCK_NONE,
     },
    //   // Add other safety settings as needed
    ];


    // Respond with a simple greeting for now
    const greeting = `Hello, ${name}!`;

    return res.status(200).json({ greeting });
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
