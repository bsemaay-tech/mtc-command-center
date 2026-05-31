// ==UserScript==
// @name         TradingView to VSCode Bridge
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Sends Pine Script errors to local VS Code server
// @author       Antigravity
// @match        https://www.tradingview.com/chart/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function () {
    'use strict';

    const LOG_ENDPOINT = 'http://localhost:3000/log';
    let lastError = "";

    console.log("🌉 TradingView Bridge Loaded");

    function senLog(message, type = "error") {
        // Debounce exact duplicates
        if (message === lastError) return;
        lastError = message;

        console.log("🌉 Bridge sending:", message);

        GM_xmlhttpRequest({
            method: "POST",
            url: LOG_ENDPOINT,
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify({ message: message, type: type }),
            onload: function (response) {
                console.log("🌉 Sent to VS Code!");
            }
        });
    }

    // Observer for Pine Editor Console (Bottom Panel)
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach((node) => {
                    // Check if it's an error line in the console
                    // TradingView classes are obfuscated, so we look for structure or keywords
                    // This is a heuristic - adapt as TV changes
                    if (node.innerText && (node.innerText.includes("Error") || node.innerText.includes("Processing script"))) {
                        // Find specific error text
                        // Usually inside a div with specific colors or classes
                        senLog(node.innerText.trim(), "log");
                    }
                });
            }
        });
    });

    // Strategy: Wait for bottom dock to load
    const waitForDock = setInterval(() => {
        // Try to find the console container. Generic selector for the bottom panel content.
        const bottomPanel = document.querySelector('.bottom-widget-container') || document.body;

        if (bottomPanel) {
            console.log("🌉 Bridge attached to:", bottomPanel);
            observer.observe(bottomPanel, { childList: true, subtree: true });

            // Also monkey-patch console.error (fallback)
            /*
            const origError = console.error;
            console.error = function(...args) {
                const msg = args.join(' ');
                if (msg.includes("Pine")) {
                    senLog(msg, "console_error");
                }
                origError.apply(console, args);
            };
            */

            clearInterval(waitForDock);
        }
    }, 2000);

    // Initial ping
    senLog("Bridge connected to Browser!", "info");

})();
