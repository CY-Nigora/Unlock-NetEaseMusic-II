# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005029F9843BD56D82303C45C942ED09D5CD7F03B321B840C0147CD33BD686C5818F30AECAFD6A5C1726CF0FD66DF8334944668FA42562F38F7AE9AC5CE05208E8E77E1FC0D4523534ED727F05D63C346415EF830ECCAD5202FB73C9FF698333B860D53FA7C082AC80C737E5BBE9750CFE48DDFF3CECF5B0F40579A840F763726A75D5EF90E95ABE2776544578F9DD751EDF02AB83D2EC8F37B6063AB2B89C19777E336CA8B38D7D3479D6631DC9B16DB49955575D0D7151A51F59A37133F93AB407C57F8FAA52AFA736A73F32FDFB02D6287B9943F257FD82253C7D16C22D393F3ACF957B431727D4BA576452AE51D99D46244FD34D6D286DC42F085F2AD61A5A1B4CD231FFA30B2F421694705CAE6308A1AC113020D07AA3069E59EE121EFC24577539CC5FE71C467F71808458352A72E5F02D0BAAC7A96A6D816D2AC8DDA76D326888B173E011EF411B7987919E48BC6B2FD5187CB25238DB9E00EC3AFBC801A2B037C91598943B8D0C9973FB2D336F8042324BB2DE4E1E52AA9BB66425ACEFBEA17828F73301FB4FCB620976D5288D"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
