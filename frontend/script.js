

const BASE_URL = "http://127.0.0.1:8000";  // Backend API URL

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("shortenBtn").addEventListener("click", shortenUrl);
    document.getElementById("statsBtn").addEventListener("click", getStats);
});


async function shortenUrl() {
    const longUrl = document.getElementById("longUrl").value;
    const shortUrlDiv = document.getElementById("shortUrl");
    const errorDiv = document.getElementById("error");
    const loader = document.getElementById("loader");

    shortUrlDiv.innerHTML = "";
    errorDiv.innerHTML = "";

    if (!longUrl) {
        errorDiv.innerHTML = "❌ Please enter a valid URL.";
        return;
    }

    loader.classList.remove("hidden");

    try {
        const response = await fetch(`${BASE_URL}/shorten`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ long_url: longUrl })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Error shortening URL.");
        }

        shortUrlDiv.innerHTML = `✅ Short URL: <a href="${result.short_url}" target="_blank">${result.short_url}</a>`;
    } catch (error) {
        errorDiv.innerHTML = `❌ ${error.message}`;
    } finally {
        loader.classList.add("hidden");
    }
}



async function getStats() {
    let shortUrlInput = document.getElementById("shortUrlInput").value;
    const statsDiv = document.getElementById("stats");
    const statsErrorDiv = document.getElementById("statsError");
    const statsLoader = document.getElementById("statsLoader");

    statsDiv.innerHTML = "";
    statsErrorDiv.innerHTML = "";

    if (!shortUrlInput) {
        statsErrorDiv.innerHTML = "❌ Please enter a short URL.";
        return;
    }

    // ✅ Extract the short URL ID from a full URL
    try {
        const urlObj = new URL(shortUrlInput);
        shortUrlInput = urlObj.pathname.substring(1); // Extracts '06995e' from 'http://127.0.0.1:8000/06995e'
    } catch (error) {
        statsErrorDiv.innerHTML = "❌ Invalid URL format.";
        return;
    }

    statsLoader.classList.remove("hidden");

    try {
        const response = await fetch(`${BASE_URL}/stats/${shortUrlInput}`, {
            method: "GET"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Error fetching stats.");
        }

        statsDiv.innerHTML = `
            ✅ <strong>Long URL:</strong> <a href="${result.long_url}" target="_blank">${result.long_url}</a><br>
            🔢 <strong>Click Count:</strong> ${result.click_count}<br>
            ⏳ <strong>Expiry Date:</strong> ${result.expiry_date}
        `;
    } catch (error) {
        statsErrorDiv.innerHTML = `❌ ${error.message}`;
    } finally {
        statsLoader.classList.add("hidden");
    }
}
