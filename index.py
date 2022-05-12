"""Project to automate reviews on the Trustpilot"""

import time
from main.controller import *


def main_loop():
    action = Use()
    progress(action)


def progress(action):
    action.click('/html/body/div[2]/div[3]/div/a[4]')
    action.click('/html/body/div[2]/div[5]/div/div[1]/table/tbody/tr[1]/td[3]/span[2]/a[1]')
    text = get_copy()
    action.switch(0)

    action.click('// *[ @ id = "__next"] / div / header / div / div[2] / div[2] / div / a[3]')
    action.click('// *[ @ id = "react-container"] / div / div / button[2]')
    action.send('// *[ @ id = "react-container"] / div / div / form / div / input', text, False)
    action.click('//*[@id="react-container"]/div/div/form/button')

    name = get_name()
    action.wait_until('//*[@id="react-container"]/div/div/form/div[2]/input')
    action.send('//*[@id="react-container"]/div/div/form/div[2]/input', name, False)
    action.click('// *[ @ id = "react-container"] / div / div / form / div[3] / label / input')
    action.click('//*[@id="react-container"]/div/div/form/button')

    time.sleep(1)
    action.switch(1)

    action.wait_until('/html/body/div[2]/div[5]/div/div[1]/table/tbody/tr[1]', False)
    content = action.get_value('predmet')
    action.switch(0)
    action.send('//*[@id="react-container"]/div/div/form/div/div/input', content, False)

    action.send('//*[@id="heroSearchContainer"]/div/div/div/div/form/input', 'NAME_OF_COMPANY')
    action.click('//*[@id="__next"]/div/main/div/div[3]/section/div[1]/div[2]/div/div[1]/input[5]')
    action.click('//*[@id="__next"]/div/main/div/div[2]/form/div/div/div[1]/input[5]')

    review = get_review()
    action.send('//*[@id="review-title"]', review[0], False)
    action.send('//*[@id="review-text"]', review[1], False)
    action.click('//*[@id="confirm-submit-checkox"]')
    action.click('//*[@id="__next"]/div/main/div/div[2]/form/div[6]/button', method=By.CLASS_NAME)
    action.driver.quit()


if __name__ == '__main__':
    rev_count = int(input("How many reviews do you want? "))
    timeout = int(input("Delay between reviews in seconds: "))
    for el in range(rev_count):
        main_loop()
        time.sleep(timeout)
