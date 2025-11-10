from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict
import json
app = FastAPI(title="Text Adventure Starter")

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Simple in-memory "world" for the text adventure
# Rooms are nodes, edges are actions
WORLD: Dict[str, Dict[str, str]] = {
    "start": {
        "description": "You wake up in a tiny room. A single door to the north.",
        "north": "hall"
    },
    "hall": {
        "description": "A long hallway with flickering lights. Doors east and west, and stairs up.",
        "east": "lab",
        "west": "armory",
        "up": "roof"
    },
    "lab": {
        "description": "A dusty lab with notes about 'Project Rabbital'. You can go west.",
        "west": "hall"
    },
    "armory": {
        "description": "Empty racks. A rusty key lies here. You can go east.",
        "east": "hall",
        "take key": "key_taken"
    },
    "roof": {
        "description": "Wind in your face. A locked hatch leads north. You can go down.",
        "down": "hall",
        "unlock": "exit"  # requires key
    },
    "exit": {
        "description": "The hatch opens. Sunlight. Freedom. You win! Refresh to play again.",
    }
}

def get_state(request: Request) -> Dict[str, str]:
    # Very simple cookie-backed state (no security needed for demo)
    state_cookie = request.cookies.get("adventure_state")
    if state_cookie:
        try:
            return json.loads(state_cookie)
        except Exception:
            pass
    return {"room": "start", "inventory": []}

def set_state(response: Response, state: Dict[str, str]):
    response.set_cookie("adventure_state", json.dumps(state))

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    state = get_state(request)
    room = state.get("room", "start")
    desc = WORLD.get(room, {}).get("description", "Unknown place.")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "room": room,
        "description": desc,
        "inventory": ", ".join(state.get("inventory", [])) or "(empty)"
    })

@app.post("/action", response_class=HTMLResponse)
async def action(request: Request):
    form = await request.form()
    cmd = (form.get("command") or "").strip().lower()
    state = get_state(request)
    room = state.get("room", "start")
    inventory = state.get("inventory", [])

    # Handle special logic
    if cmd == "look":
        # stay in place, just re-render
        pass
    elif cmd in ("north","south","east","west","up","down"):
        next_room = WORLD.get(room, {}).get(cmd)
        if next_room:
            state["room"] = next_room
        else:
            # no movement
            pass
    elif cmd == "take key" and room == "armory":
        if "key" not in inventory:
            inventory.append("key")
            state["inventory"] = inventory
    elif cmd in ("unlock hatch", "unlock"):
        if room == "roof" and "key" in inventory:
            state["room"] = "exit"
    elif cmd == "restart":
        state = {"room": "start", "inventory": []}
    # else unrecognized commands are ignored in this minimal demo

    # Render
    new_room = state.get("room","start")
    desc = WORLD.get(new_room, {}).get("description","Unknown place.")
    html = templates.TemplateResponse("partials.html", {
        "request": request,
        "room": new_room,
        "description": desc,
        "inventory": ", ".join(state.get("inventory", [])) or "(empty)"
    })
    response = Response(content=await html.body(), media_type="text/html")
    set_state(response, state)
    return response

@app.get("/healthz")
def health():
    return {"ok": True}