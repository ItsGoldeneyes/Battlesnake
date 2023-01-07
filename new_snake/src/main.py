from flask import request
from flask import Flask
import logging
import time
import os

from game import Game

PORT = os.getenv('PORT', "8008")
DEBUG_MODE = os.getenv('DEBUG_MODE', "False")=="True"
MOVE_MODE = os.getenv('MOVE_MODE', "True")=="True"
TIMING_MODE = os.getenv('TIMING_MODE', "True")=="True"

app = Flask(__name__)

games = {}
start_times = {}

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
            "color": "#88EBB8",
            "head": "all-seeing",
            "tail": "mlh-gene",
        }


@app.post("/start")
def handle_start():
    """
    This function is called every time a game is started.
    A "Game" object is created and stored in the games variable.
    """
    print("")
    data = request.get_json()
    new_game = Game(data, debug_mode= DEBUG_MODE)
    game = {new_game.get_id() : new_game}
    games.update(game)
            
    print(f"START {data['game']['id']}")
    print(f"  RULES {new_game.get_rules()}", flush=True)
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
    
    return {"move": move, "shout": ""}



@app.post("/end")
def handle_end():
    """
    This function is called when a game the Battlesnake was in has ended.
    The "Game" object is removed from the games dictionary.
    """        
    data = request.get_json()
    games.pop(data["game"]["id"])
    
    print(f"END {data['game']['id']}")
    
    return "ok"


@app.after_request
def identify_server(response):
    response.headers["Server"] = "Golden/Snake"
    return response


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    host = "0.0.0.0"
    port = int(PORT)

    print(f"\nRunning Battlesnake server at http://{host}:{port}", flush=True)
    # app.env = 'development'
    app.run(host=host, port=port, debug=DEBUG_MODE)
