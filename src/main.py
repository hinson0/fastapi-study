from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web import explorer, creature, user, file, greet, game

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)
app.include_router(file.router)
app.include_router(greet.router)
app.include_router(game.router)

# mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
