let mediaStream = null;
let audioCtx = null;
let workletNode = null;
let ws = null;
let pending = 0;
const MAX_IN_FLIGHT = 8; // backpressure guard

async function startCapture(tabId) {
  try {
    // tabCapture for audio; some apps may block it.
    mediaStream = await chrome.tabCapture.capture({
      audio: true,
      video: false
    });

    audioCtx = new AudioContext({ sampleRate: 16000 });
    await audioCtx.audioWorklet.addModule("audio-worklet.js");

    const source = audioCtx.createMediaStreamSource(mediaStream);
    workletNode = new AudioWorkletNode(audioCtx, "pcm-worklet");

    const { backendWsUrl } = await chrome.storage.local.get(["backendWsUrl"]);
    ws = new WebSocket(backendWsUrl);
    ws.binaryType = "arraybuffer";

    ws.onopen = () => console.log("WS connected");

    ws.onmessage = (evt) => {
      // Expect JSON messages like: { type: "suggestion", text: "..." }
      try {
        const msg = JSON.parse(evt.data);
        if (msg.type === "suggestion") {
          chrome.runtime.sendMessage({ type: "SUGGESTION", payload: msg });
        }
      } catch (_) {}
    };

    workletNode.port.onmessage = (e) => {
      if (!ws || ws.readyState !== WebSocket.OPEN) return;
      if (pending >= MAX_IN_FLIGHT) return; // drop if congested
      pending++;
      try {
        ws.send(e.data);
      } finally {
        pending--;
      }
    };

    source.connect(workletNode);
    workletNode.connect(audioCtx.destination);
  } catch (err) {
    console.error("Capture failed", err);
  }
}

async function stopCapture() {
  if (workletNode) {
    workletNode.disconnect();
    workletNode = null;
  }
  if (audioCtx) {
    await audioCtx.close();
    audioCtx = null;
  }
  if (mediaStream) {
    mediaStream.getTracks().forEach(t => t.stop());
    mediaStream = null;
  }
  if (ws) {
    ws.close();
    ws = null;
  }
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "OFFSCREEN_START") startCapture(msg.tabId);
  if (msg.type === "OFFSCREEN_STOP") stopCapture();
});
