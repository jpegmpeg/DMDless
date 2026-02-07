const sendButton = document.getElementById("send");
const responseBox = document.getElementById("response");

async function sendMessage() {
  const playerId = document.getElementById("playerId").value.trim();
  const message = document.getElementById("message").value.trim();

  if (!playerId || !message) {
    responseBox.textContent = "Please enter a player ID and a message.";
    return;
  }

  responseBox.textContent = "Sending...";

  try {
    const apiResponse = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ player_id: playerId, message }),
    });

    if (!apiResponse.ok) {
      throw new Error(`API error: ${apiResponse.status}`);
    }

    const data = await apiResponse.json();
    responseBox.textContent = data.reply;
  } catch (error) {
    responseBox.textContent =
      "DM is offline. Use this space to plan the next judgment call.";
    console.error(error);
  }
}

sendButton.addEventListener("click", sendMessage);
