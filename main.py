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
    exec_inputs(["a", "a", "a"], delay_type="default")


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
    prev_cos = game_params["cos"].copy()

    for cpu in range(4):
        new_co = 0
        if no_co:
            new_co = 12
        else:
            new_co = random.randint(0, 11)
        game_params["cos"][cpu] = new_co
    logging.debug(f"New random COs choosen: {game_params['cos']}")
    
    cleaned_co_list = organize_cos(game_params["cos"].copy())
    game_params["cos"] = cleaned_co_list
    logging.info(f"New COs choosen: {game_params['cos']}")
    
    # calc distance for each CO selection
    co_distance = [0, 0, 0, 0]
    for cpu in range(4):
        co_distance[cpu] = game_params["cos"][cpu] - prev_cos[cpu]
        logging.debug(f"Distance for cpu {cpu} found to be {co_distance[cpu]}")

    ##assign new cos to each cpu (within game(so actually do it))
    # move up to first co (up 2)
    exec_inputs(["up", "up"])
    ##begin loop
    for cpu in range(4):
        # select co (a)
        exec_inputs(["a"], delay_type="fast")

        # move Right number equal to co number (x Right)
        input_sequence = []
        for i in range(abs(co_distance[cpu])):
            if co_distance[cpu] < 0:
                input_sequence.append("Left")
            else:
                input_sequence.append("Right")

        exec_inputs(input_sequence, delay_type="fast")
        # select co (a)
        exec_inputs(["a"], delay_type="fast")
        # move to next cpu (Right)
        exec_inputs(["Right"], delay_type="fast")
        logging.debug(f"CO selected for CPU {cpu}")

    # after loop, return to NEXT button (2 down)
    exec_inputs(["down", "down"], delay_type="fast")


def organize_cos(co_list: list[int]) -> list[int]:
    """Re-arranges the given COs to "soft sort" them into their proper teams
    Function will attempt to place COs onto the CPU slot corresponding with their proper team,
    unless that slot has already been filled by another CO.

    Each CPU slot correlates to a team:
    - CPU 0: 12th Battalion
    - CPU 1: New Rubinelle Army
    - CPU 2: Lazurian Army
    - CPU 3: Intelligent Defense Systems
    """

    # CO_number : CPU_slot
    co_team_allegiance = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 1,
        5: 1,
        6: 1,
        7: 2,
        8: 2,
        9: 3,
        10: 3,
        11: 3,
        12: None,  # 12 means no CO. If that comes up, something has gone horribly wrong
    }

    # each co looks up their team, then attempts to swap
    for moving_cpu in range(len(co_list)):
        moving_co = co_list[moving_cpu]
        target_cpu = co_team_allegiance[moving_co]
        target_co = co_list[target_cpu]
        # check if target CPU slot is used
        if co_team_allegiance[target_co] != target_cpu:  # slot empty, swap!
            co_list[target_cpu] = moving_co
            co_list[moving_cpu] = target_co
            logging.debug(f"CO {moving_co} swapped with CO {target_co}")

    return co_list


def select_map(target_map: int):
    """Navigates to and selects given map number in the menu, moving from current map
    Also updates global game params variable
    """
    current_map = game_params["map_number"]
    logging.debug(f"Navigating to map {target_map} from map {current_map}")

    # find inputs required, negative for Left, postive for Right
    distance = target_map - current_map
    key_to_press = ""
    if distance < 0:
        key_to_press = "Left"
    else:
        key_to_press = "Right"
    logging.debug(f"Distance found to be {distance}, moving to the {key_to_press}")

    # create and submit input sequence to navigate and select map
    input_sequence = []
    for i in range(abs(distance) + 1):
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
        - "fast" for 0.4 seconds

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
            delay = 0.4

        time.sleep(delay)
        logging.debug(f"inputting key '{keystroke}'")
        ahk.key_down(keystroke)
        # Key to be must be held shortly for input to be registered by melonDS
        time.sleep(0.15)
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
