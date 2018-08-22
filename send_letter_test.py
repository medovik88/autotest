import unittest
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This test log in, send letter and check the letter was delivered

Preconditions:
register account on "https://mail.ukr.net/desktop/login"

"""
class SendLetterTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.driver.implicitly_wait(10)

    def test_sending_letter(self):

# Go to "https://mail.ukr.net/desktop/login" and set login and password to corresponding fields
        driver = self.driver
        driver.get("https://mail.ukr.net/desktop/login")
        login_field = driver.find_element_by_id("id-1")
        login_field.send_keys("Yuriy.Komrakov")
        password_field = driver.find_element_by_id("id-2")
        password_field.send_keys("0937536859yk")
        button_login = driver.find_element_by_xpath("//*[@class = 'button__content']")
        button_login.click()

# Compare e-mail field with our e-mail to be sure that is right account
        user_mail = driver.find_element_by_xpath("//*[@class='login-button__user']")
        assert user_mail.text == "yuriy.komrakov@ukr.net"

# Create variable mail_counter to count up letters we have got before creating new letter
        try:
            counter = int(driver.find_element_by_xpath("//*[@class='sidebar__list-link-count']").text)
        except ValueError:
            mail_counter = 0
        else:
            mail_counter = counter

# Create new letter
        button_write_letter = driver.find_element_by_xpath("//*[@class='default compose']")
        button_write_letter.click()

        address_field = driver.find_element_by_xpath("//*[@name='toInput']")
        address_field.send_keys(user_mail.text)

        driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='mce_0_ifr']"))
        main_text_field = driver.find_element_by_xpath("//*[@id='tinymce']")
        text = "This text should not contain Cyrillic characters."
        main_text_field.send_keys(text)
        driver.switch_to.default_content()

# Send the letter
        button_send = driver.find_element_by_xpath("//*[@class='default send']")
        button_send.click()

# Wait until the letter is delivered
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='default']")))

# Refresh page and compare mail_counter with number of letters in this moment
        driver.refresh()
        new_letter = int(driver.find_element_by_xpath("//*[@class='sidebar__list-link-count']").text)

        assert (mail_counter + 1) == new_letter
# Expected result: number of letters should be equal (mail_counter + 1)

# Check first incoming letter to compare it to sent letter
        incoming_letters = driver.find_element_by_xpath("//a[@id='0']")
        incoming_letters.click()
# (We should use index in XPATH here because we need even first letter)
        first_letter = driver.find_element_by_xpath("//tr[contains(@class,'msglist__row')][1]")
        first_letter.click()
        comparable_letter = driver.find_element_by_xpath("//*[@class = 'xfmc1']").text
        print(comparable_letter)

        assert comparable_letter == text
# Expected result: text of incoming letter compare to sent letter