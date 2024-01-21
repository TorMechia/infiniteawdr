import cv2
import time
import logging
import ahk
import imageDetection

logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t %(message)s")

# todo: add params (random_cos = False, random_maps = False, random_weather = False, random_funds = False, random_income = False, ai_mode = normal)
# Process for simple game restart
def game_restart(special_type: str = None):
    logging.info(f"Restarting game. Parameters: Special type: {special_type}")
    if special_type is not None:
        if special_type == "simple":
            input_sequence = ["a", "a", "a", "a", "a", "a"]  # A x6
            exec_inputs(input_sequence)


def exec_inputs(input_sequence: list[str]):
    logging.info(f"Executing input sequence of {input_sequence}")
    keystrokes_made = 0
    for keystroke in input_sequence:
        menu_location = get_menu_location(keystrokes_made)
        time.sleep(get_location_delay(menu_location)) 
        logging.info(f"inputting key '{keystroke}'")
        ahk.key_down('a')
        time.sleep(.5) # Key to be must be held shortly for input to be registered by melonDS
        ahk.key_up('a')
        keystrokes_made += 1
        
        
def get_menu_location(keystrokes_made: int):
    '''number of keystrokes made shows where we are in the menu'''
    menu_location_index = ["endscreen", "end_stats", "single_ds_play", "entered_map_menu"]
    current_location = None
    try:
        current_location = menu_location_index[keystrokes_made]
    except IndexError:
        current_location = "unknown"
    logging.debug(f"In menu: {current_location}")
    return current_location 
    
    
def get_location_delay(menu_location: str):
    # delay_index = {"endscreen":5, "end_stats":5, "single_ds_play":2, "entered_map_menu":2, "unknown":2} #normal vals
    delay_index = {"endscreen":2, "end_stats":2, "single_ds_play":2, "entered_map_menu":2, "unknown":2} #debug vals
    delay = delay_index.get(menu_location, 2)
    logging.debug(f"Delay for this menu: {delay}")
    return delay
    

def main(emulation_scale = "4x", seconds_between_checks = 5):
    """
    Keyword Arguments:
        emulation_scale {str} -- Window scale melonDS is run at. "fullscreen" for maximized window. Fullscreen breaks input. (default: {"4x"})
        seconds_between_checks {int} -- Interval between checks for game end (default: {5})
    """    

    ## Setup images to be used in recognition 
    current_screenshot = cv2.imread("images\\default_screenshot.png")  # load dummy screenshot until real one is taken
    if emulation_scale == "fullscreen":
        end_screen_template = cv2.imread("images\\end_indicator_fullscreen.png")
    elif emulation_scale == "4x":
        end_screen_template = cv2.imread("images\\end_indicator_4x.png")
            
    #primary loop
    while True:
        time.sleep(seconds_between_checks)
        imageDetection.update_screenshot()
        current_screenshot = cv2.imread("images\\latest_screenshot.png")
        
        if imageDetection.is_image_present(current_screenshot, end_screen_template):
            logging.info("Game has ended.")
            game_restart(special_type="simple")
        else:
            logging.debug("Game is ongoing.")


main()
