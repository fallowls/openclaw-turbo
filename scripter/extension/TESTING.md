# Testing Checklist (Performance-focused)

## Functional
- [ ] Extension loads (no console errors)
- [ ] Start/Stop capture toggles status correctly
- [ ] Suggestions appear in overlay

## Performance
- [ ] Audio capture starts < 1s after clicking Start
- [ ] WS send queue does not grow unbounded (no memory spike)
- [ ] CPU stays < 5–8% on idle page
- [ ] Suggestion render < 1.5s end-to-end

## Failure Modes
- [ ] Invalid WS URL shows no crash; UI remains responsive
- [ ] Stop cleans up audio/WS without leaks

## UX
- [ ] Overlay doesn’t obstruct important UI
- [ ] Pin + Dismiss behave correctly
