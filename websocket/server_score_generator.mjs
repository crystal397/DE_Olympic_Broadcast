// 스코어 무작위 생성기

import express from 'express';
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

let previousData = null;
let liveGame = null;
let games = [];

function generateRandomGameData() {
    const teams = [
        'Brazil', 'Germany', 'France', 'Norway', 'Japan', 'USA',
        'Australia', 'Sweden', 'Denmark', 'South Korea'
    ];
    const venues = ['Olympic Stadium', 'Handball Arena', 'Main Sports Hall'];

    const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

    const createGame = (gender, status, startTime) => {
        let homeTeam, awayTeam;
        while (!awayTeam || homeTeam === awayTeam) {
            homeTeam = getRandomElement(teams);
            awayTeam = getRandomElement(teams);
        }
        return {
            sport_event: {
                id: `sr:match:${Math.random().toString(36).substring(2)}`,
                start_time: startTime.toISOString(),
                competitors: [
                    { name: homeTeam },
                    { name: awayTeam }
                ],
                venue: { name: getRandomElement(venues) }
            },
            sport_event_status: {
                status: status,
                home_score: status === 'live' ? Math.floor(Math.random() * 3) : 0,
                away_score: status === 'live' ? Math.floor(Math.random() * 3) : 0
            },
            gender: gender
        };
    };

    const games = [];

    // 하나의 live 경기 생성 (2024년 8월 6일 오전 03:00 KST 고정)
    const liveStartTime = new Date(Date.UTC(2024, 7, 5, 18, 0, 0)); // 2024년 8월 5일 18:00 UTC (한국 시간 2024년 8월 6일 오전 03:00)
    liveGame = createGame('남자', 'live', liveStartTime);
    games.push(liveGame);

    // 나머지 not_started 경기 생성
    for (let i = 1; i < 10; i++) {
        const gender = i % 2 === 0 ? '남자' : '여자';
        const futureTime = new Date();
        futureTime.setHours(17 + Math.floor(Math.random() * 8)); // 오늘 17:00부터 24:00 사이의 무작위 시간
        futureTime.setMinutes(0, 0, 0); // 정각으로 설정
        const game = createGame(gender, 'not_started', futureTime);
        games.push(game);
    }

    return games;
}

function updateLiveGameScore(game) {
    console.log("Response status code: 200"); // 점수 업데이트 전에 로그 추가
    if (Math.random() < 0.5) {
        game.sport_event_status.home_score += 1;
    } else {
        game.sport_event_status.away_score += 1;
    }
    // 점수 업데이트 로그 제거
    fetchAndUpdateClients(); // 점수 업데이트 후 클라이언트에 데이터 전송
}

function scheduleNextScoreUpdate() {
    const minDelay = 5000;  // 최소 5초
    const maxDelay = 15000; // 최대 15초
    const delay = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;

    setTimeout(() => {
        if (liveGame) {
            updateLiveGameScore(liveGame);
        }
        scheduleNextScoreUpdate();
    }, delay);
}

function filterGames(games) {
    return games.filter(game => ['live', 'not_started'].includes(game.sport_event_status.status));
}

async function fetchAndUpdateClients() {
    const liveGames = filterGames(games);
    const currentData = { summaries: liveGames };

    previousData = currentData;
    const data = JSON.stringify(currentData.summaries);
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(data);
        }
    });
    // 'Data sent to clients' 로그 제거
}

// 서버 시작 시 한 번만 경기 데이터를 생성
games = generateRandomGameData();

// 랜덤한 시간 간격으로 점수 업데이트 시작
scheduleNextScoreUpdate();

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
