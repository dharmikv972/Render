// Define and export the function using ES modules
export function getRandomGreeting(name) {
  const greetings = [
    `Hello, ${name}! How are you today?`,
    `Hi, ${name}! Nice to see you!`,
    `Hey, ${name}! Hope you're having a great day!`,
  ];
  return greetings[Math.floor(Math.random() * greetings.length)];
}
