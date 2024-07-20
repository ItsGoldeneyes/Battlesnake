# Clone joshhartmann11/BattleSnakeArena into the directory ml_snake/train_environment/BattleSnakeArena
import subprocess
import os

if __name__ == "__main__":
    # Clone the BattleSnakeArena repository if it does not exist
    if not os.path.exists("train_environment/BattleSnakeArena"):
        print("Cloning BattleSnakeArena")
        subprocess.run(["git", "clone", "https://github.com/ItsGoldeneyes/BattleSnakeArena.git", "train_environment/BattleSnakeArena"], shell=True)

    # Add ml snake to the snakes.py file
    with open("train_environment/BattleSnakeArena/snakes.py", "a") as f:
        f.write("\nfrom ml_snake.src.main import info, start, move, end\n")