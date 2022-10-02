import logging
import os

from flask import Flask
from flask import request

from game import Game

DEBUG_MODE = True

app = Flask(__name__)

games = {}

@app.get("/")
def handle_info():
    """
    This function is called when the snake is registered on play.battlesnake.com.
    It is also called when the snake's status is checked before a game.
    """
    print("INFO", flush=True)
    print(games)
    return {
            "apiversion": "1",
            "author": "Goldeneyes",
            "color": "#DAA520",
            "head": "moto-helmet",
            "tail": "comet",
        }


@app.post("/start")
def handle_start():
    """
    This function is called every time a game is started.
    A "Game" object is created and stored in the games variable.
    """
    
    data = request.get_json()
    new_game = Game(data, debug_mode= DEBUG_MODE)
    game = {new_game.get_id() : new_game}
    games.update(game)
    
    print(f"{data['game']['id']} START", flush=True)
    print(f"{data['game']['id']} RULES {new_game.get_rules()}")
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is where move logic is held.
    Each turn, this function is called and the Battlesnake calculates a move.
    It also contains a failsafe to recreate a game in case the snake restarts during a game.
    """
    data = request.get_json()
    gameid = data["game"]["id"]
    if gameid in games: 
        move = games[gameid].turn(data)
    else:
        new_game = Game(data, debug_mode= DEBUG_MODE)
        game = {new_game.get_id() : new_game}
        games.update(game)
        move = games[gameid].turn(data)
    print(f"{gameid} MOVE {move}", flush=True)
    
    return {"move": move, "shout": ""}



@app.post("/end")
def handle_end():
    """
    This function is called when a game the Battlesnake was in has ended.
    The "Game" object is removed from the games dictionary.
    """
    data = request.get_json()
    games.pop(data["game"]["id"])
    
    print(f"{data['game']['id']} END")
    return "ok"


@app.after_request
def identify_server(response):
    response.headers["Server"] = "BattlesnakeOfficial/starter-snake-python"
    return response


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8080"))

    print(f"\nRunning Battlesnake server at http://{host}:{port}", flush=True)
    # app.env = 'development'
    app.run(host=host, port=port, debug=DEBUG_MODE)
