# DMDless

DMDless is a starter skeleton for building a DM-less 5e experience. The current focus is a single-player prompt loop where a lightweight DM agent makes a judgment call. This establishes the baseline interaction before we expand into character creation, world generation, and persistent state.

## Architecture (Skeleton)

```
frontend/     # Lightweight web UI for player ↔ DM interactions
backend/      # FastAPI service for DM logic, state, and orchestration
```

### Current Flow

1. Player submits a message in the web UI.
2. Backend stores minimal conversation state and returns a DM-style response.
3. The UI displays the DM response and keeps the loop moving.

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
python -m http.server 5173
```

Then open `http://localhost:5173` in the browser and send a test message.

## Testing

```bash
python -m pytest
```

## Next Steps

- Character creation flow and persistence (database + schema).
- Adventure briefing intake for players.
- Multi-modal DM responses (audio + visuals).
- Environment and NPC state tracking for longer sessions.
