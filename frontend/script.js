const BASE_URL = "http://127.0.0.1:8000";  // Backend API URL

document.getElementById("shortenBtn").addEventListener("click", shortenUrl);

async function shortenUrl() {
    const longUrl = document.getElementById("longUrl").value;
    const shortUrlDiv = document.getElementById("shortUrl");
    const errorDiv = document.getElementById("error");
    const loader = document.getElementById("loader");

    // Clear previous messages
    shortUrlDiv.innerHTML = "";
    errorDiv.innerHTML = "";

    if (!longUrl) {
        errorDiv.innerHTML = "❌ Please enter a valid URL.";
        return;
    }

    // Show loader while fetching
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
        loader.classList.add("hidden");  // Hide loader after request
    }
}
