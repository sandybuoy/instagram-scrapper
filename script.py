from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from random import randint


options = Options()
options.add_argument("--disable-extensions")
options.add_argument('disable-infobars')
# options.add_argument('--headless')
options.add_argument('--incognito')

driver = webdriver.Chrome(chrome_options=options)


def loaderPresent():
    try:
        driver.find_element_by_xpath("//div[contains(@class, 'W1Bne  ztp9m ')]")
        return True
    except NoSuchElementException:
        return False


try:
    driver.get('https://www.instagram.com/accounts/login/')
    user = ''
    password = ''
    user_to_search = 'thisiszaar'
    with open("user_to_search.txt", "w") as text_file:
        text_file.write(user_to_search)
    time.sleep(3)

    user_field = driver.find_element_by_xpath("//input[@name='username']")
    user_field.send_keys(user)
    time.sleep(1)

    pass_field = driver.find_element_by_xpath("//input[@name='password']")
    pass_field.send_keys(password)
    time.sleep(1)

    login_btn = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/span/button")
    login_btn.click()

    time.sleep(4)
    driver.get('https://www.instagram.com/' + user_to_search)

    driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(4)

    follower = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]')

    time.sleep(1)

    check = driver.execute_script("return arguments[0].scrollHeight > arguments[0].offsetHeight;", follower)
    print(check)
    last_scroll_height = 0
    call = 0
    counter = 0
    if check:
        while True:
            driver.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight);", follower)
            # time.sleep(1)
            time.sleep(randint(30, 35))
            scroll_height = driver.execute_script("return arguments[0].scrollHeight;", follower)
            if scroll_height != last_scroll_height:
                call = call + 1
                follower_data = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/ul/div')
                text = follower_data.get_attribute('innerHTML')
                soup = bs(text, 'html.parser')
                with open("FollowersData.txt", "w") as text_file:
                    text_file.write(text)
                print('API Call: ' + str(call))
                last_scroll_height = scroll_height

            elif scroll_height == last_scroll_height:
                if loaderPresent():
                    counter = counter + 1
                    print('API Request Failed: ' + str(counter))
                    if counter == 5:
                        break
                else:
                    break

    with open("FollowersData.txt", "r") as text_file:
        text = text_file.read()
    soup = bs(text, 'html.parser')
    data = []
    for i in soup.find_all('img'):
        data.append('@' + i['alt'][:-18])

    df = pd.DataFrame(data)
    df.to_csv(user_to_search + ".csv", sep=',', index=False, header=False)

    print(len(data), data[-1])
    driver.close()
    driver.quit()



except:

    with open("FollowersData.txt", "r") as text_file:
        text = text_file.read()

    with open("user_to_search.txt", "r") as text_file:
        user_to_search = text_file.read()
    soup = bs(text, 'html.parser')
    data = []
    for i in soup.find_all('img'):
        data.append('@' + i['alt'][:-18])

    df = pd.DataFrame(data)
    df.to_csv(user_to_search + ".csv", sep=',', index=False, header=False)

    print(len(data), data[-1])
    driver.quit()
