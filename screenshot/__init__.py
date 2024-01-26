from io import BytesIO
import os
import logging
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Set default download folder for ChromeDriver
RESULT_FOLDER = r"./download"
if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)
prefs = {"download.default_directory": RESULT_FOLDER}


def open_url(address, wait, file_name):
    # SELENIUM SETUP
    # just to hide not so rilevant webdriver-manager messages
    logging.getLogger('WDM').setLevel(logging.WARNING)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Disable GPU usage when running headless
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')   # Disable sandboxing
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(wait)
    driver.maximize_window()
    driver.get(address)
    time.sleep(wait)
    driver.set_window_size(1250, 1780)
    ss = save_screenshot(driver, f'{file_name}')
    driver.quit()

    return ss


def save_screenshot(driver, file_name):
    try:
        height, width = scroll_down(driver)
        driver.set_window_size(width, height)
        img_binary = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img_binary))
        img.save(f'{file_name}.png', 'PNG', quality=100)
        # print(file_name)
        # image to pdf
        image_1 = Image.open(f'{file_name}.png')
        im_1 = image_1.convert('RGB')
        pdf_path = f'{file_name}.pdf'
        im_1.save(pdf_path)
        print("Screenshot saved!")

        return pdf_path
    except Exception as e:
        return False


def scroll_down(driver):
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script(
        "return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script(
                f"window.scrollTo({rectangle[0]}, {rectangle[1]})")
            time.sleep(0.5)
        # time.sleep(0.2)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        previous = rectangle

    return total_height, total_width


def handler(url, wait, file_name):
    return open_url(url, wait, file_name)
