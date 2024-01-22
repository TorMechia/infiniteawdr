import cv2
import time
import logging
import ahk
import imageDetection
import random

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:\t %(message)s")


# todo: add params (random_cos = False, random_maps = False, random_weather = False, random_funds = False, random_income = False, ai_mode = normal)
# Process for simple game restart
def game_restart(restart_type: str = "simple"):
    logging.info(f"Restarting game. Restart type: {restart_type}")
    if restart_type == "simple":  # restart with same game parameters
        input_sequence = ["a", "a", "a", "a", "a", "a"]  # A x6
        exec_inputs(input_sequence, delay_type="dynamic")
    if restart_type == "random":  # restart with randomized COs and map
        random_game_restart()


def random_game_restart():
    exec_inputs(["a", "a", "a"], delay_type="dynamic")  # enter map menu
    logging.debug("Now in map selection menu")
    new_map_number = random_map_number()
    select_map(new_map_number)
    logging.info(f"Map {new_map_number} selected")
    logging.debug("Now in co menu. Selecting random COs")
    select_cos()
    logging.info("COs randomly selected, starting game")
    exec_inputs(["a", "a"])


def random_map_number(map_type="fourP"):
    """Give random map number for the given menu"""
    num_maps = None
    if map_type == "fourP":
        num_maps = 30
    map_number = random.randint(1, num_maps)

    logging.debug(f"Randomly chose map {map_number}")
    return map_number


def select_cos(no_co=False):
    """Picks a random CO for each cpu.
    Starts on and returns to NEXT button on menu.
    Assumes 4 player map because this project is a mess and I want out. What was I on yesterday, writing this shit?

    no_co keyword, if set true, will set all CPUs to CO 12, giving them no CO
    """
    # assign new cos to each cpu (within program)
    for cpu in range(4):
        new_co = 0
        if no_co:
            new_co = 12
        else:
            new_co = random.randint(0, 11)
        game_params["cos"][cpu] = new_co
    logging.info(f"New COs choosen: {game_params['cos']}")

    ##assign new cos to each cpu (within game(so actually do it))
    # move up to first co (up 2)
    exec_inputs(["up", "up"])
    ##begin loop
    for cpu in range(4):
        target_co = game_params["cos"][cpu]
        # select co (a)
        exec_inputs(["a"])
        # move right number equal to co number (x right)
        input_sequence = []
        for i in range(target_co):
            input_sequence.append("right")
        exec_inputs(input_sequence, delay_type="fast")
        # select co (a)
        exec_inputs("a")
        # move to next cpu (right)
        exec_inputs("right")
        logging.debug(f"CO selected for CPU {cpu}")

    # after loop, return to NEXT button (2 down)
    exec_inputs(["down", "down"])


def select_map(target_map: int):
    """Navigates to and selects given map number in the menu, moving from current map
    Also updates global game params variable
    """
    current_map = game_params["map_number"]
    logging.debug(f"Navigating to map {target_map} from map {current_map}")

    # find inputs required, negative for left, postive for right
    distance = target_map - current_map
    key_to_press = ""
    if distance < 0:
        key_to_press = "left"
    else:
        key_to_press = "right"
    logging.debug(f"Distance found to be {distance}, moving to the {key_to_press}")

    # create and submit input sequence to navigate and select map
    input_sequence = []
    for i in range(abs(distance)):
        input_sequence.append(key_to_press)
    input_sequence.append("a")
    logging.debug(f"Input sequence construction concluded: {input_sequence}")
    exec_inputs(input_sequence, delay_type="fast")

    # update global var
    game_params["map_number"] = target_map


def exec_inputs(input_sequence: list[str], delay_type="default"):
    """Executes the given sequence of inputs.
    Delay types are:
        - "dynamic" for it to be handled based on the keystroke number (see get_location_delay())
        - "fast" for 0.25 seconds

    Arguments:
        input_sequence {list[str]} -- Sequence of inputs to be executed.

    Keyword Arguments:
        delay_type{str} -- Type of delay.
    """
    logging.info(f"Executing input sequence of {input_sequence}")
    keystrokes_made = 0
    for keystroke in input_sequence:
        delay = 2
        if delay_type == "dynamic":
            menu_location = get_menu_location(keystrokes_made)
            delay = get_location_delay(menu_location)
        if delay_type == "fast":
            delay = 0.25

        time.sleep(delay)
        logging.info(f"inputting key '{keystroke}'")
        ahk.key_down(keystroke)
        # Key to be must be held shortly for input to be registered by melonDS
        time.sleep(0.1)
        ahk.key_up(keystroke)
        keystrokes_made += 1


def get_menu_location(keystrokes_made: int):
    """number of keystrokes made shows where we are in the menu"""
    menu_location_index = [
        "endscreen",
        "end_stats",
        "single_ds_play",
        "entered_map_menu",
    ]
    current_location = None
    try:
        current_location = menu_location_index[keystrokes_made]
    except IndexError:
        current_location = "unknown"
    logging.debug(f"In menu: {current_location}")
    return current_location


def get_location_delay(menu_location: str):
    """Get delay that should be given before each input for a given menu.
    Gives 2 as a default value.

    Arguments:
        menu_location {str} -- current

    Returns:
        int -- delay
    """
    # delay_index = {"endscreen":5, "end_stats":5, "single_ds_play":2, "entered_map_menu":2, "unknown":2} #normal vals
    delay_index = {
        "endscreen": 2,
        "end_stats": 2,
        "single_ds_play": 2,
        "entered_map_menu": 2,
        "unknown": 2,
    }  # debug vals
    delay = delay_index.get(menu_location, 2)
    logging.debug(f"Delay for this menu: {delay}")
    return delay


def main(emulation_scale="4x", seconds_between_checks=5):
    """
    Keyword Arguments:
        emulation_scale {str} -- Window scale melonDS is run at. "fullscreen" for maximized window. Fullscreen breaks input. (default: {"4x"})
        seconds_between_checks {int} -- Interval between checks for game end (default: {5})
    """

    ## Setup images to be used in recognition
    # load dummy screenshot until real one is taken
    current_screenshot = cv2.imread("images\\default_screenshot.png")
    if emulation_scale == "fullscreen":
        end_screen_template = cv2.imread("images\\end_indicator_fullscreen.png")
    elif emulation_scale == "4x":
        end_screen_template = cv2.imread("images\\end_indicator_4x.png")

    # primary loop
    while True:
        time.sleep(seconds_between_checks)
        imageDetection.update_screenshot()
        current_screenshot = cv2.imread("images\\latest_screenshot.png")

        if imageDetection.is_image_present(current_screenshot, end_screen_template):
            logging.info("Game has ended.")
            game_restart(restart_type="random")
        else:
            logging.debug("Game is ongoing.")


global game_params
game_params = {"map_number": 1, "cos": [0, 0, 0, 0]}
# cos is the co number for each player 1-4, counting left to right in rows

main()
