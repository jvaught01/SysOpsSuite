document.addEventListener("DOMContentLoaded", function () {
  const socket = new WebSocket(
    "ws://" + window.location.host + "/ws/trigger-socket-server/"
  );

  socket.onopen = function () {
    console.log("WebSocket connection established.");
  };

  socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type === "progress_update") {
      updateProgressBar(data.progress);
    } else if (data.type === "process_complete") {
      updateProgressBar(100); // Ensure progress bar is at 100%
      showCompletionMessage(data.message);
    }
  };

  function updateProgressBar(progress) {
    const progressBar = document.getElementById("progress-bar");
    const progressText = document.getElementById("progress-text");

    progressBar.style.width = `${progress}%`;
    progressText.textContent = `${progress}% Complete`;
  }

  function showCompletionMessage(message) {
    const completionMessage = document.getElementById("completion-message");
    completionMessage.textContent = message;
    completionMessage.classList.remove("hidden"); // Display the message
  }

  const startButton = document.getElementById("start-backup-button");
  if (startButton) {
    startButton.addEventListener("click", function () {
      socket.send(JSON.stringify({ command: "start_backup_process" }));
    });
  }
});
