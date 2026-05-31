const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const LOG_FILE = path.join(__dirname, '..', 'TV_ERRORS.log');

const server = http.createServer((req, res) => {
    // Enable CORS to allow browser script to talk to us
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.method === 'POST' && req.url === '/log') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const timestamp = new Date().toLocaleString();
                const logEntry = `\n[${timestamp}] ${data.type.toUpperCase()}: ${data.message}\n`;

                console.log(`Received: ${data.message}`);

                fs.appendFileSync(LOG_FILE, logEntry);

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true }));
            } catch (e) {
                console.error("Error parsing request", e);
                res.writeHead(400);
                res.end();
            }
        });
    } else {
        res.writeHead(404);
        res.end();
    }
});

server.listen(PORT, () => {
    console.log(`🌉 TV Bridge Server running on http://localhost:${PORT}`);
    console.log(`📂 Writing errors to: ${LOG_FILE}`);
});
