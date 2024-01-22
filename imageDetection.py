import logging
import cv2
from PIL import ImageGrab


def update_screenshot():
    logging.debug("Updating screenshot")
    screenshot = ImageGrab.grab() #todo: screenshot only the necessary window
    screenshot.save("images\\latest_screenshot.png", "PNG")
    logging.info("Screenshot updated")


def is_image_present(image, template, threshold=0.8):
    """Check if smaller image is present within the larger image

    Arguments:
        smaller_image -- Image to be searched for. end_screen_template in this implementation
        larger_image -- Image to be searched within. current_screenshot in this implementation
        threshold -- Detection threshold for confidence of image being present
    """
    logging.debug("Checking for image match")
    result = cv2.matchTemplate(
        image, template, cv2.TM_CCOEFF_NORMED
    )  # creates grayscale image showing pixel matches. probably
    _, max_val, _, _ = cv2.minMaxLoc(result)
    logging.debug(f"Match value of {max_val}")

    if max_val > threshold:
        logging.info("Image match success")
        return True
    else:
        logging.info("Image match failed")
        return False