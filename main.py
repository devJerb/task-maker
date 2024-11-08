from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import date
import random

app = FastAPI(title="Game Data API", version="1.0.0", docs_url="/")


class Game(BaseModel):
    title: str
    description: str
    price: float
    date_released: date


def generate_random_games(n: int) -> List[Game]:
    titles = [
        "Adventure Quest",
        "Mystery Manor",
        "Fantasy World",
        "Space Odyssey",
        "Pirate's Cove",
    ]
    descriptions = [
        "An exciting journey awaits you in this thrilling adventure game.",
        "Solve puzzles and uncover secrets in this mysterious game.",
        "A magical world filled with mythical creatures and quests.",
        "Explore the galaxy and face unknown dangers in space.",
        "A pirate-themed game where you search for hidden treasures.",
    ]
    games = []
    for _ in range(n):
        game = Game(
            title=random.choice(titles),
            description=random.choice(descriptions),
            price=round(random.uniform(5.0, 50.0), 2),
            date_released=date(
                random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28)
            ),
        )
        games.append(game)
    return games


@app.get(
    "/games",
    response_model=List[Game],
    summary="Get a list of games",
    description="Returns a list of games with random data.",
)
async def get_games():
    return generate_random_games(5)
