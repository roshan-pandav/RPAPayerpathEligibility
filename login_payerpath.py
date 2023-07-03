from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def waits(el, driver):
    """
    This function waits robotscraper until element given in the argument loads
    :param el: element of interest
    :return: None
    """
    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, el)))

def payerpath_login(folder_path, customer_name, username, payer_pswd, url):
    """
    :param folder_path: "Downloading excel file from payerpath if Needed"
    :param customer_name: "Specify Cutomer name"
    :param username: "Specify Username"
    :param payer_pswd: "Specify Password
    :param url: ""Payerpath URL
    :return: "return success if login else return error
    """
    try:
        session = requests.session()
        status_code = session.post(url=url, allow_redirects=True).status_code
        if status_code == 200:
            chrome_options = Options()
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option('prefs',
                                                   {"download.default_directory": folder_path,
                                                    "download.prompt_for_download": False,
                                                    "download.directory_upgrade": True,
                                                    "plugins.always_open_pdf_externally": True,
                                                    "profile.default_content_settings.images": 2
                                                    })
            driver = webdriver.Chrome(options=chrome_options, executable_path=r"E:\gloData_Share\chromedriver_new.exe")
            driver.get(url)
            driver.maximize_window()
            time.sleep(2)
            waits('//*[@id="CustomerName"]', driver)
            driver.find_element(by=By.XPATH, value='//*[@id="CustomerName"]').send_keys(customer_name)
            driver.find_element(by=By.XPATH, value='//*[@id="UserName"]').send_keys(username)
            driver.find_element(by=By.XPATH, value='//*[@id="Password"]').send_keys(payer_pswd)
            driver.find_element(by=By.XPATH, value='//*[@id="login"]').click()
            waits('//*[@id="container"]/div/div[1]/div/div[1]/div[3]/a', driver)
            driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[1]/div/div[1]/div[3]/a').click()
            waits('//*[@id="container"]/div/div[1]/div/div[1]/div[3]/div/a[1]/span', driver)
            driver.find_element(by=By.XPATH,
                                value='//*[@id="container"]/div/div[1]/div/div[1]/div[3]/div/a[1]/span').click()
            # a=WebDriverWait(driver,10).until((EC.presence_of_element_located(driver.title)))
            # print(a)
            # shutting down
            # loc = driver.find_element(by=By.XPATH, value="//a[normalize-space()='Roshan Pandav']")
            # print("Loc", loc)
            # time.sleep(1)
            # hover = ActionChains(driver).move_to_element(loc)
            # hover.perform()
            # time.sleep(2)
            # driver.find_element(by=By.XPATH, value="//span[normalize-space()='Logout']").click()
            return driver
        else:
            return "error"
    except Exception as error:
        print(error)
        error_message = str(error)
        print(error_message)
        return "error"
