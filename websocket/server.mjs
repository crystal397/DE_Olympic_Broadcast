// 웹 소켓 스트리밍 서버

import express from 'express';
import axios from 'axios';
import path from 'path';
import http from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

const PORT = 5000;

const API_KEY = '8hbysPzTB95iyTwOOrrnUakSq4qV0KCaa85JSWWg';
const WOMEN_API_URL = `https://api.sportradar.com/handball/trial/v2/ko/seasons/sr%3Aseason%3A105531/summaries?api_key=${API_KEY}`;
const MEN_API_URL = `https://api.sportradar.com/handball/trial/v2/ko/seasons/sr%3Aseason%3A105529/summaries?api_key=${API_KEY}`;

let previousData = null;

async function getGameData(apiUrl, gender) {
    let attempt = 0;
    const maxAttempts = 5;

    while (attempt < maxAttempts) {
        try {
            const response = await axios.get(apiUrl, {
                headers: { 'Accept': 'application/json' }
            });
            console.log(`Response status code: ${response.status}`);
            const data = response.data;
            data.summaries.forEach(game => game.gender = gender);
            return data;
        } catch (error) {
            console.error(`Request error: ${error.message}`);
            if (error.response && error.response.status === 429) {
                const waitTime = (2 ** attempt) + Math.random();
                console.log(`Rate limit exceeded. Retrying in ${waitTime} seconds...`);
                await new Promise(resolve => setTimeout(resolve, waitTime * 1000));
                attempt++;
            } else {
                return {};
            }
        }
    }
    return {};
}

function filterGames(games) {
    return games.filter(game => ['live', 'not_started'].includes(game.sport_event_status.status));
}

function hasChanged(currentData, previousData) {
    if (!previousData) return true;
    return JSON.stringify(currentData) !== JSON.stringify(previousData);
}

async function fetchAndUpdateClients() {
    const womenData = await getGameData(WOMEN_API_URL, '여자');
    await new Promise(resolve => setTimeout(resolve, 5000));
    const menData = await getGameData(MEN_API_URL, '남자');

    const combinedSummaries = [...womenData.summaries, ...menData.summaries];
    const liveGames = filterGames(combinedSummaries);
    const currentData = { summaries: liveGames };

    if (hasChanged(currentData, previousData)) {
        previousData = currentData;
        const data = JSON.stringify(liveGames);
        wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    }
}

// 주기적으로 데이터를 가져와 클라이언트에 전송
setInterval(fetchAndUpdateClients, 60000); // 60초마다 실행

wss.on('connection', ws => {
    console.log('Client connected');
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

app.use(express.static(path.join(__dirname, 'templates')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index3.html'));
});

server.listen(PORT, () => {
    console.log(`Server is running on http://3.38.230.0:${PORT}`);
});