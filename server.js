const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const { fetchEmails } = require('./nylasClient');
const { summarizeEmail } = require('./groqClient');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// Validate required environment variables
const requiredEnvVars = ['NYLAS_API_KEY', 'NYLAS_USER_GRANT_ID', 'GROQ_API_KEY'];
const missingVars = requiredEnvVars.filter((v) => !process.env[v]);
if (missingVars.length > 0) {
  console.warn(`⚠️  Warning: Missing environment variables: ${missingVars.join(', ')}`);
  console.warn('   The server will start, but /emails endpoint will return errors.');
}

// Health check
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: '📧 AI Email Summarizer API is running' });
});

// Main endpoint
app.get('/emails', async (req, res) => {
  const limit = Math.min(Math.max(parseInt(req.query.limit) || 2, 1), 10);

  console.log(`\n📬 Fetching ${limit} email(s)...`);

  // Guard: missing env vars
  if (missingVars.length > 0) {
    return res.status(500).json({
      success: false,
      error: `Missing required environment variables: ${missingVars.join(', ')}. Please check your .env file.`,
    });
  }

  let rawEmails;
  try {
    rawEmails = await fetchEmails(limit);
  } catch (err) {
    console.error('❌ Nylas fetch error:', err.message);
    return res.status(502).json({
      success: false,
      error: `Failed to fetch emails from Nylas: ${err.message}`,
    });
  }

  if (!rawEmails || rawEmails.length === 0) {
    return res.json({ success: true, count: 0, emails: [] });
  }

  console.log(`✅ Fetched ${rawEmails.length} email(s). Starting AI summarization...`);

  const summarizedEmails = [];

  // Sequential to avoid Groq rate limits
  for (const email of rawEmails) {
    const rawBody =
      email.body ||
      (email.snippet ? email.snippet : '') ||
      '(No body content available)';

    const cleanBody = rawBody
      .replace(/<[^>]*>?/gm, '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 1000);

    const fromField =
      email.from && email.from.length > 0
        ? `${email.from[0].name || ''} <${email.from[0].email || ''}>`.trim()
        : 'Unknown';

    const dateStr = email.date
      ? new Date(email.date * 1000).toLocaleString()
      : 'Unknown Date';

    let summary = '(Summary unavailable)';
    try {
      summary = await summarizeEmail(email.subject || '(No subject)', cleanBody);
      console.log(`  ✅ Summarized: "${(email.subject || '').slice(0, 40)}..."`);
    } catch (err) {
      console.error(`  ⚠️  Groq error for email ${email.id}: ${err.message}`);
      summary = `Summary failed: ${err.message}`;
    }

    summarizedEmails.push({
      id: email.id || '',
      from: fromField,
      subject: email.subject || '(No subject)',
      date: dateStr,
      summary,
    });
  }

  return res.json({
    success: true,
    count: summarizedEmails.length,
    emails: summarizedEmails,
  });
});

app.listen(PORT, () => {
  console.log(`\n🚀 AI Email Summarizer backend running on http://127.0.0.1:${PORT}`);
  console.log(`   GET /emails?limit=5  →  Fetch and summarize emails\n`);
});
