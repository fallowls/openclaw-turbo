// Inject overlay for suggestions
const overlayId = "scripter-overlay";

function createOverlay() {
  if (document.getElementById(overlayId)) return;
  const el = document.createElement("div");
  el.id = overlayId;
  el.innerHTML = `
    <div class="scripter-card">
      <div class="scripter-header">
        <div class="scripter-title">Live Assist</div>
        <div class="scripter-dot" title="Connected"></div>
      </div>
      <div class="scripter-text" id="scripter-text">Waiting for suggestions…</div>
      <div class="scripter-actions">
        <button id="scripter-pin">Pin</button>
        <button id="scripter-dismiss">Dismiss</button>
      </div>
    </div>
  `;
  document.body.appendChild(el);

  el.querySelector("#scripter-dismiss").onclick = () => {
    el.querySelector("#scripter-text").textContent = "Waiting for suggestions…";
  };
  el.querySelector("#scripter-pin").onclick = () => {
    el.classList.toggle("pinned");
  };
}

createOverlay();

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "SUGGESTION") {
    createOverlay();
    const text = msg.payload?.text || "(empty suggestion)";
    document.getElementById("scripter-text").textContent = text;
  }
});
