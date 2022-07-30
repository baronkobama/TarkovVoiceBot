"""TarkovBot's Python Run Script"""

# Built-in Modules
import os

# Local Modules
from src.bot import TarkovBot


def main() -> None:
    # Console clearing
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print("> --------Run Info--------")

    # Running the bot itself
    bot = TarkovBot()
    bot.run()


if __name__ == "__main__":
    main()
