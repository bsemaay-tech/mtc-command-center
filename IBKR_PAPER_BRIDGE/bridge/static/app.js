const statusNode = document.getElementById("status");

async function loadStatus() {
  if (!statusNode) return;
  try {
    const response = await fetch("/api/status");
    const status = await response.json();
    statusNode.textContent = `Status: ${status.status} / ${status.network}`;
  } catch (error) {
    statusNode.textContent = "Status: unavailable";
  }
}

loadStatus();
