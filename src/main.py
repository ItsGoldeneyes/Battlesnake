from datetime import datetime
from flask import request
from flask import Flask
import logging
import os

from game import Game

DEBUG_MODE = os.getenv('DEBUG_MODE', "True")=="True"
MOVE_MODE = os.getenv('MOVE_MODE', "False")=="True"
TIMING_MODE = os.getenv('TIMING_MODE', "False")=="True"

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
    print("")
    data = request.get_json()
    new_game = Game(data, debug_mode= DEBUG_MODE)
    game = {new_game.get_id() : new_game}
    games.update(game)
    
    if TIMING_MODE:
        start_times[data['game']['id']] = datetime.utcnow()
            
    print(f"START {data['game']['id']}")
    print(f"RULES {data['game']['id']} {new_game.get_rules()}", flush=True)
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is where move logic is held.
    Each turn, this function is called and the Battlesnake calculates a move.
    It also contains a failsafe to recreate a game in case the snake restarts during a game.
    """
    turn_start = datetime.utcnow()
    data = request.get_json()
    gameid = data["game"]["id"]
    if gameid in games: 
        move = games[gameid].turn(data)
    else:
        new_game = Game(data, debug_mode= DEBUG_MODE)
        game = {new_game.get_id() : new_game}
        games.update(game)
        move = games[gameid].turn(data)
        
    if MOVE_MODE:
        print(f"MOVE {move}", end="", flush=True)
        if TIMING_MODE:
            turn_end = datetime.utcnow()
            turn_duration = turn_end - turn_start
            print(f" DURATION {turn_duration.total_seconds()*1000}")
    
    return {"move": move, "shout": ""}



@app.post("/end")
def handle_end():
    """
    This function is called when a game the Battlesnake was in has ended.
    The "Game" object is removed from the games dictionary.
    """
    if TIMING_MODE:
        game_end = datetime.utcnow()
        
    data = request.get_json()
    games.pop(data["game"]["id"])
    
    print(f"END  {data['game']['id']}")
    
    if TIMING_MODE:
        game_time = game_end - start_times[data["game"]["id"]]
        print(f"-- Game took: {game_time.total_seconds()} seconds")
    
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
