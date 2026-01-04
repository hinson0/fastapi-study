from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from service import game as game_service


router = APIRouter(prefix="/game")


@router.get("")
async def game_start(request: Request):
    word = game_service.get_word()
    templates = Jinja2Templates(directory="template")
    return templates.TemplateResponse("game.html", {"request": request, "word": word})


@router.post("/score")
async def get_score(request: Request):
    data = await request.json()
    guess = data.get("guess", "")
    word = data.get("word", "")

    result = game_service.calculate_score(guess, word)
    return result
