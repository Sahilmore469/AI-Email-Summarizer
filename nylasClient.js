const Nylas = require('nylas');
require('dotenv').config();

let nylasInstance = null;

function getNylas() {
  if (!nylasInstance) {
    if (!process.env.NYLAS_API_KEY) {
      throw new Error('NYLAS_API_KEY is not set in .env');
    }
    nylasInstance = new Nylas({
      apiKey: process.env.NYLAS_API_KEY,
      apiUri: process.env.NYLAS_API_URI || 'https://api.us.nylas.com',
    });
  }
  return nylasInstance;
}

/**
 * Fetch emails using Nylas Messages API
 * @param {number} limit - Number of emails to fetch (1–10)
 * @returns {Promise<Array>} - Array of email message objects
 */
async function fetchEmails(limit = 5) {
  const nylas = getNylas();
  const identifier = process.env.NYLAS_USER_GRANT_ID;

  if (!identifier) {
    throw new Error('NYLAS_USER_GRANT_ID is not set in .env');
  }

  try {
    const response = await nylas.messages.list({
      identifier,
      queryParams: {
        limit: limit,
      },
    });

    // Nylas SDK v7+ returns { data, requestId, ... }
    const emails = response.data || response;

    if (!Array.isArray(emails)) {
      throw new Error('Unexpected response format from Nylas API');
    }

    return emails;
  } catch (err) {
    // Provide clearer error messages for common Nylas errors
    if (err.statusCode === 401 || (err.message && err.message.includes('401'))) {
      throw new Error('Nylas authentication failed. Check your NYLAS_API_KEY and NYLAS_USER_GRANT_ID.');
    }
    if (err.statusCode === 404 || (err.message && err.message.includes('404'))) {
      throw new Error('Nylas grant ID not found. Verify NYLAS_USER_GRANT_ID is correct.');
    }
    if (err.statusCode === 429 || (err.message && err.message.includes('429'))) {
      throw new Error('Nylas rate limit exceeded. Please wait and try again.');
    }
    throw err;
  }
}

module.exports = { fetchEmails };
