let previousData = {};

function isValidDate(date) {
    return date instanceof Date && !isNaN(date);
}

function groupByDate(games) {
    return games.reduce((acc, game) => {
        const date = new Date(game.sport_event.start_time).toLocaleDateString();
        if (!acc[date]) {
            acc[date] = [];
        }
        acc[date].push(game);
        return acc;
    }, {});
}

function renderSchedule(data) {
    const scheduleElement = document.getElementById('schedule');
    const groupedData = groupByDate(data);
    const sortedDates = Object.keys(groupedData).sort((a, b) => new Date(a) - new Date(b));

    sortedDates.forEach(date => {
        let dateHeader = scheduleElement.querySelector(`h2[data-date="${date}"]`);
        if (!dateHeader) {
            dateHeader = document.createElement('h2');
            dateHeader.dataset.date = date;
            dateHeader.innerText = date;
            scheduleElement.appendChild(dateHeader);
        }

        groupedData[date].forEach(game => {
            const gameId = game.sport_event.id;
            let matchElement = scheduleElement.querySelector(`div[data-id="${gameId}"]`);
            const gender = game.gender;
            const scheduledDate = new Date(game.sport_event.start_time);
            const formattedDate = isValidDate(scheduledDate) ? scheduledDate.toLocaleString() : 'TBA';
            const homeScore = game.sport_event_status.home_score || 0;
            const awayScore = game.sport_event_status.away_score || 0;

            if (!matchElement) {
                matchElement = document.createElement('div');
                matchElement.className = 'match';
                matchElement.dataset.id = gameId;
                matchElement.innerHTML = `
                    <h3>${game.sport_event.competitors[0].name} vs ${game.sport_event.competitors[1].name} (${gender})</h3>
                    <p><strong>Date:</strong> ${formattedDate}</p>
                    <p><strong>Venue:</strong> ${game.sport_event.venue.name}</p>
                    <p><strong>Status:</strong> ${game.sport_event_status.status}</p>
                    <p><strong>Score:</strong>
                        <div class="score-horizontal-result-number">${homeScore}</div>
                        <div class="score-horizontal-result-number">${awayScore}</div>
                    </p>
                `;
                scheduleElement.appendChild(matchElement);
            } else {
                // Update only if there are changes
                if (matchElement.querySelectorAll('.score-horizontal-result-number')[0].innerText != homeScore || matchElement.querySelectorAll('.score-horizontal-result-number')[1].innerText != awayScore) {
                    matchElement.querySelectorAll('.score-horizontal-result-number')[0].innerText = homeScore;
                    matchElement.querySelectorAll('.score-horizontal-result-number')[1].innerText = awayScore;
                }
                if (matchElement.querySelector('p strong').nextSibling.textContent != game.sport_event_status.status) {
                    matchElement.querySelector('p strong').nextSibling.textContent = game.sport_event_status.status;
                }
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Initialize WebSocket connection
    const socket = new WebSocket('ws://3.38.230.0:5000');

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        renderSchedule(data);
    };

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    socket.onclose = function() {
        console.log('WebSocket connection closed');
    };
});
