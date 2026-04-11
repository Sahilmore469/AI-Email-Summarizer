const Groq = require('groq-sdk');
require('dotenv').config();

let groqInstance = null;

function getGroq() {
  if (!groqInstance) {
    if (!process.env.GROQ_API_KEY) {
      throw new Error('GROQ_API_KEY is not set in .env');
    }
    groqInstance = new Groq({ apiKey: process.env.GROQ_API_KEY });
  }
  return groqInstance;
}

const SUMMARIZATION_PROMPT = `You are an expert email assistant. Summarize the email clearly and concisely.

Return output in exactly this format:

Summary:
2-3 lines overview of what the email is about.

Key Points:
- Bullet point 1
- Bullet point 2
- Bullet point 3 (if applicable)

Action Required:
Mention any actions the reader needs to take, or write "None" if none.

Deadline:
Mention any deadlines or dates mentioned, or write "None" if none.`;

/**
 * Summarize a single email using Groq LLM
 * @param {string} subject - Email subject
 * @param {string} body - Cleaned email body (max 1000 chars)
 * @returns {Promise<string>} - Formatted AI summary
 */
async function summarizeEmail(subject, body) {
  const groq = getGroq();

  const userMessage = `Subject: ${subject}\n\nEmail Body:\n${body || '(No content available)'}`;

  let retries = 0;
  const maxRetries = 2;

  while (retries <= maxRetries) {
    try {
      const completion = await groq.chat.completions.create({
        model: 'llama-3.1-8b-instant',
        messages: [
          { role: 'system', content: SUMMARIZATION_PROMPT },
          { role: 'user', content: userMessage },
        ],
        max_tokens: 500,
        temperature: 0.3,
      });

      const result = completion?.choices?.[0]?.message?.content;
      if (!result) {
        throw new Error('Empty response from Groq API');
      }

      return result.trim();
    } catch (err) {
      // Rate limit: wait and retry
      if (
        err.status === 429 ||
        (err.message && err.message.includes('rate limit'))
      ) {
        if (retries < maxRetries) {
          const waitMs = 3000 * (retries + 1);
          console.warn(`  ⏳ Groq rate limit hit. Retrying in ${waitMs / 1000}s...`);
          await new Promise((r) => setTimeout(r, waitMs));
          retries++;
          continue;
        }
        throw new Error('Groq rate limit exceeded after retries. Try again in a moment.');
      }

      // Token overflow
      if (
        err.status === 400 ||
        (err.message && err.message.toLowerCase().includes('token'))
      ) {
        throw new Error('Email content too large for AI processing (token overflow).');
      }

      // Auth error
      if (err.status === 401) {
        throw new Error('Groq authentication failed. Check your GROQ_API_KEY.');
      }

      // Network / unknown errors
      throw new Error(`Groq API error: ${err.message}`);
    }
  }
}

module.exports = { summarizeEmail };
