// netlify/functions/greet.js

exports.handler = async function(event, context) {
  if (event.httpMethod === 'POST') {
    const { name } = JSON.parse(event.body);

    if (!name || typeof name !== 'string') {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Name is required and must be a string' }),
      };
    }

    const greeting = `Hello, ${name}! Nice to meet you.`;

    return {
      statusCode: 200,
      body: JSON.stringify({ greeting }),
    };
  } else {
    return {
      statusCode: 405,
      headers: { 'Allow': 'POST' },
      body: `Method ${event.httpMethod} Not Allowed`,
    };
  }
};
