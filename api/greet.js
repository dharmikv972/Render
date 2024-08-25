// Import the function using ES modules
import { getRandomGreeting } from '../utils';

export default function handler(req, res) {
  if (req.method === 'POST') {
    const { name } = req.body;

    if (!name || typeof name !== 'string') {
      return res.status(400).json({ error: 'Name is required and must be a string' });
    }

    getRandomGreeting(name) {
  const greetings = [
    `Hello, ${name}! How are you today?`,
    `Hi, ${name}! Nice to see you!`,
    `Hey, ${name}! Hope you're having a great day!`,
  ];
  return greetings[Math.floor(Math.random() * greetings.length)];
}
    const greeting = getRandomGreeting(name);

    return res.status(200).json({ greeting });
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
