import os
import time
import json
import psutil
import subprocess
import rotatescreen
from tkinter import messagebox


def setup() -> None:
    """
    Setup config file.
    """
    with open("config.json", "w") as f:
        f.write(
            json.dumps(
                        {
                            "LAUNCHER_PATH": None,
                            "WAIT_LAUNCHER_TIMEOUT": 60,
                            "WAIT_GAME_TIMEOUT": 5,
                            "FLIPPED": True
                        },
                        indent=4
                    )
            )


def open_config_file() -> None:
    """
    Open the config file.
    """
    os.startfile("config.json")


def open_config_directory() -> None:
    """
    Open the config file directory.
    """
    os.startfile(".")
    

try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    setup()
    messagebox.showinfo("Setup Config", 
                        "Please setup the config file.")
    open_config_file()
    exit()

if config["LAUNCHER_PATH"] is None or not os.path.exists(config["LAUNCHER_PATH"]):
    messagebox.showinfo("SDVX Launcher Not Found",
                        'SDVX Launcher not found.\nPlease set the path in the config file.\ne.g. "D:/Games/SOUND VOLTEX EXCEED GEAR/launcher/modules/launcher.exe"')
    open_config_file()
    exit()
    

LAUNCHER_PATH = config["LAUNCHER_PATH"]
WAIT_LAUNCHER_TIMEOUT = config["WAIT_LAUNCHER_TIMEOUT"]
WAIT_GAME_TIMEOUT = config["WAIT_GAME_TIMEOUT"]
FLIPPED = config["FLIPPED"]

SCREEN: rotatescreen.Display = rotatescreen.get_primary_display()
START_ORIENTATION: int = SCREEN.current_orientation


def launcher_running() -> bool:
    """
    Check if the SDVX launcher is running.

    Returns:
        bool: True if the launcher is running, False otherwise.
    """
    for proc in psutil.process_iter():
        if proc.name() == "launcher.exe":
            return True
    return False


def wait_for_launcher(timeout=WAIT_LAUNCHER_TIMEOUT) -> None:
    """
    Waits for the launcher to start.
    """
    curr_time = time.time()
    while not launcher_running():
        time.sleep(0.5)
        if time.time() - curr_time > timeout:
            raise TimeoutError("Timeout waiting for launcher to start.")
            break

def wait_for_launcher_close() -> None:
    """
    Waits for the launcher to close.
    """
    while launcher_running():
        time.sleep(0.5)


def game_running() -> bool:
    """Check if the game is running.

    Returns:
        bool: True if the game is running, False otherwise.
    """
    for proc in psutil.process_iter():
        if proc.name() == "errorreporter.exe":
            return True
    return False


def wait_for_game(timeout=WAIT_GAME_TIMEOUT) -> None:
    """
    Waits for the game to start.
    """
    curr_time = time.time()
    while not game_running():
        time.sleep(0.5)
        if time.time() - curr_time > timeout:
            raise TimeoutError("Timeout waiting for game to start.")
            break


def wait_for_game_close() -> None:
    """
    Waits for the game to close.
    """
    while game_running():
        if SCREEN.current_orientation == 0:
            SCREEN.set_portrait_flipped() if FLIPPED else SCREEN.set_portrait()
        time.sleep(0.5)


def start_launcher() -> bool():
    """
    Starts the SDVX launcher.
    """
    os.startfile(LAUNCHER_PATH)


def main() -> None:
    """
    Main function.
    """
    start_launcher()

    try:
        wait_for_launcher()
        print("Launcher started.")

        wait_for_launcher_close()
        print("Launcher closed.")

        if START_ORIENTATION == 0:
            SCREEN.set_portrait_flipped()

        time.sleep(5)

        wait_for_game()
        print("Game started.")

        wait_for_game_close()
        print("Game closed.")

    except TimeoutError as err:
        print(err)

    SCREEN.rotate_to(START_ORIENTATION)


if __name__ == "__main__":
    main()
