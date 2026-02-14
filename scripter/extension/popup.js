async function load() {
  const { backendWsUrl } = await chrome.storage.local.get(["backendWsUrl"]);
  document.getElementById("wsUrl").value = backendWsUrl || "";
}

async function save() {
  const url = document.getElementById("wsUrl").value.trim();
  await chrome.storage.local.set({ backendWsUrl: url });
}

const statusEl = document.getElementById("status");

document.getElementById("start").onclick = async () => {
  await save();
  chrome.runtime.sendMessage({ type: "START" });
  statusEl.textContent = "Capturing…";
};

document.getElementById("stop").onclick = async () => {
  chrome.runtime.sendMessage({ type: "STOP" });
  statusEl.textContent = "Idle";
};

load();
