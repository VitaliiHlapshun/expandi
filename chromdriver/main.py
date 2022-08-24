import os
import csv
import wget
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://www.instagram.com/'
USERNAME = 'hlapshun'
PASSWORD = 'selenium'
S = Service('/home/vitalii/PycharmProjects/expandio/chromdriver/chromedriver')
driver = webdriver.Chrome(service=S)


def login():
    """Opens browser, navigates to main page, checks login cookies,
    logs in"""
    driver.get(url=URL)
    try:
        with open('cookies.pickle', 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print('File does not exist')
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    password.clear()

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()
    sleep(2)
    not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    sleep(2)
    not_now_button_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    get_followers_data()


def get_followers_data():
    """Navigates to the followers' popup, scrolls down scrapping user
    links, usernames and profile pictures at once"""
    driver.get(url=f'{URL}hlapshun/followers')
    scroll_box = driver.find_element(By.XPATH,
                                     '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')
    scrolling = driver.execute_script(""" 
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight; """, scroll_box)
    images_obj = driver.find_elements(By.TAG_NAME, 'img')
    images = [image.get_attribute('src') for image in images_obj]

    account_links_obj = driver.find_elements(By.TAG_NAME, 'a')
    account_links = [link.get_attribute('href') for link in account_links_obj]

    user_names_obj = driver.find_elements(By.XPATH,
                                          '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/span/a/span/div')
    user_names = [name.get_attribute('innerHTML') for name in
                  user_names_obj]
    record_to_csv(user_names, account_links, images)
    save_images(images)


def record_to_csv(instagram_names, instagram_links, images):
    """Records scrapped data into csv-file"""
    headers = ['User name', 'Link', 'Image link']
    with open('users.csv', 'w') as f:
        writer = csv.writer(f)
        header = writer.writerow(headers)
        writer.writerows(zip(instagram_names, instagram_links, images))


def save_images(images: list):
    """Saves images into the folder"""
    keyword = 'pictures'
    current_path = os.getcwd()
    path_to_images = os.path.join(current_path, keyword)

    os.mkdir(path_to_images)
    counter = 0
    for image in images:
        save_as = os.path.join(path_to_images,
                               keyword + str(counter) + '.jpg')
        wget.download(image, save_as)
        counter += 1


def quit_session():
    """Terminates a session"""
    driver.quit()


def get_cookies():
    """Gets and serializes cookies"""
    with open('cookies.pickle', 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


if __name__ == "__main__":
    login()
    get_cookies()
    quit_session()
