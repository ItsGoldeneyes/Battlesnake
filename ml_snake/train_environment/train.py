from distutils.dir_util import copy_tree
import subprocess
import os


def _clone_arena_repository():
    if not os.path.exists("train_environment/BattleSnakeArena"):
        print("Cloning BattleSnakeArena")
        subprocess.run(["git", "clone", "https://github.com/ItsGoldeneyes/BattleSnakeArena.git", "train_environment/BattleSnakeArena"], shell=True)
        return True
    return False

def _load_snake():
    # Copy ml_snake/src to train_environment/BattleSnakeArena/ml_snake on Windows
    print(os.getcwd()+"/src")
    copy_tree(os.getcwd()+"/src", "train_environment/BattleSnakeArena/test_snakes/ml_snake")

    with open("train_environment/BattleSnakeArena/snakes.py", "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write("import test_snakes.ml_snake.main\n" + content)

        # Move pointer to end of file, then append the new snake
        f.seek(0, 2)
        f.write(
            """
SNAKES.append(
    {
    "move": test_snakes.ml_snake.main.move,
    "name": "ml_snake",
    "color": COLORS["red"]
    }
)
            """)
        f.close()


def setup(versions=[]):
    """
    TODO: Add support for multiple snake models, specify versions to load, and make src code dynamic. Maybe look for a generic model file?
    """
    _clone_arena_repository()
    # If first line of snakes.py is not import test_snakes.ml_snake.main, add it
    with open("train_environment/BattleSnakeArena/snakes.py", "r") as f:
        if f.readline() != "import test_snakes.ml_snake.main\n":
            _load_snake()


def run_game(snakes=[], game_count=1, speed=50, output=True, threads=16):
    if snakes == []:
        raise ValueError("No snakes provided")

    # Run the game
    args = ["python", "train_environment/BattleSnakeArena/battlesnake.py", "-sp", str(speed), "-t", str(threads)]
    if game_count >= 1:
        args += ["-g", str(game_count)]
    if not output:
        args += ["-b"]
    args += ["-s", *snakes]

    stdout = subprocess.run(args, shell=True, capture_output=True)

    # Parse the output
    out = stdout.stdout.decode("utf-8")

    # Parse output for if game_count >= 1
    if game_count > 1:
        # Parse output to get results
        rough_results = []
        for line in out.split("\n"):
            if any(name in line for name in snakes):
                rough_results.append(line)
        # Parse results to {snake: wins}
        results = {}
        for snake in snakes:
            results[snake] = 0
        for line in rough_results:
            results[line.partition(", Games Won: ")[0]] = int(line.partition(", Games Won: ")[2][:-1])
        return results

    # Parse the output for if game_count == 1
    else:
        # Last line of output
        last_line = out.split("\n")[-2]
        winner = [name for name in snakes if name in last_line]
        if winner == []:
            winner = "DRAW"
        return winner[0]




if __name__ == "__main__":
    # Setup arena and load snake
    setup()

    run_game(["ml_snake", "battleJake2018", "battleJake2019"], 1, 500, True)
    print(run_game(["ml_snake", "battleJake2018", "battleJake2019"], 5000, 10000, False))
