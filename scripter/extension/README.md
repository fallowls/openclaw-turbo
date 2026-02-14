# Scripter Live Assist (MVP)

This is a **Chrome extension scaffold** for live AI call assistance.

## Features (MVP)
- Popup to start/stop capture
- Tab audio capture via `chrome.tabCapture`
- WebSocket streaming of PCM audio to backend
- Overlay suggestions in the call tab

## How to run
1. Open Chrome → `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load unpacked** → select this `extension/` folder
4. Open your call web app tab
5. Click the extension icon → set **Backend WS URL** → Start

## Backend
You need a WebSocket server that accepts raw **Int16 PCM** audio (16kHz mono) and sends JSON suggestions:

```json
{ "type": "suggestion", "text": "Acknowledge the concern and offer a quick pilot." }
```

## Notes
- Uses `AudioWorklet` for low-latency audio processing (better performance).
- Some call apps may block `tabCapture`.
- For production, add consent UI and PII redaction.

## Quality & Testing (lightweight)
- **Manual smoke test**: load unpacked, start/stop capture, verify overlay text updates.
- **Latency check**: ensure WS roundtrip + suggestion render < 1500ms.
- **Resource check**: verify CPU < 5–8% on idle and no memory leaks after stop/start loops.
- **Failure test**: use invalid WS URL; ensure UI stays responsive.
