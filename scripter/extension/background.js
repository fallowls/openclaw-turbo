// Background service worker
const DEFAULT_SETTINGS = {
  backendWsUrl: "wss://your-backend.example.com/stream",
  enabled: false,
  tabId: null
};

chrome.runtime.onInstalled.addListener(async () => {
  const current = await chrome.storage.local.get(null);
  if (!current || Object.keys(current).length === 0) {
    await chrome.storage.local.set(DEFAULT_SETTINGS);
  }
});

async function ensureOffscreen() {
  const exists = await chrome.offscreen.hasDocument();
  if (exists) return;
  await chrome.offscreen.createDocument({
    url: "offscreen.html",
    reasons: ["AUDIO_PLAYBACK", "BLOBS"],
    justification: "Capture and process tab audio for live transcription"
  });
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    if (msg.type === "START") {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      await ensureOffscreen();
      await chrome.storage.local.set({ enabled: true, tabId: tab.id });
      chrome.runtime.sendMessage({ type: "OFFSCREEN_START", tabId: tab.id });
      sendResponse({ ok: true });
    }
    if (msg.type === "STOP") {
      await chrome.storage.local.set({ enabled: false, tabId: null });
      chrome.runtime.sendMessage({ type: "OFFSCREEN_STOP" });
      sendResponse({ ok: true });
    }
    if (msg.type === "SUGGESTION") {
      // forward suggestion to content script overlay
      const { tabId } = await chrome.storage.local.get(["tabId"]);
      if (tabId) {
        chrome.tabs.sendMessage(tabId, { type: "SUGGESTION", payload: msg.payload });
      }
      sendResponse({ ok: true });
    }
  })();
  return true;
});
