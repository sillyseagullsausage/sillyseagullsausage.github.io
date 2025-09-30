const express = require('express');
const fetch = require('node-fetch');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const CLIENT_ID = process.env.TWITCH_CLIENT_ID;

app.get('/token/:channel', async (req, res) => {
  const channel = req.params.channel;
  const url = `https://api.twitch.tv/api/channels/${channel}/access_token`;

  try {
    const response = await fetch(url, {
      headers: {
        'Client-ID': CLIENT_ID,
        'Accept': 'application/vnd.twitchtv.v5+json'
      }
    });

    if (!response.ok) throw new Error('Twitch API error');

    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('Token fetch failed:', err);
    res.status(500).json({ error: 'Failed to fetch token' });
  }
});

app.listen(PORT, () => {
  console.log(`Twitch proxy running on port ${PORT}`);
});    
