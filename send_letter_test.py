import unittest
from selenium import webdriver
import time

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
        button_login = driver.find_element_by_xpath("/html/body/div/div/main/form/button/div")
        button_login.click()
# Compare e-mail field with our e-mail to be sure that is right account
        user_mail = driver.find_element_by_xpath("//*[@class='login-button__user']")
        assert user_mail.text == "yuriy.komrakov@ukr.net"
# Create variable mail_counter to count up letters we have got before creating new letter
        try:
            counter = int(driver.find_element_by_xpath("//*[@id='0']/span[2]").text)
        except ValueError:
            mail_counter = 0
        else:
            mail_counter = counter
# Create new letter
        button_write_letter = driver.find_element_by_xpath("//*[@id='content']/aside/button")
        button_write_letter.click()

        address_field = driver.find_element_by_xpath("//*[@id='screens']/div/div[2]/section[1]/div[1]/div[4]/input[2]")
        address_field.send_keys(user_mail.text)

        driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='mce_0_ifr']"))
        main_text_field = driver.find_element_by_xpath("//*[@id='tinymce']")
        text = "Вы справились с тестовым заданием. Поздравляем! Вы приняты на работу в компанию Asferro."
        main_text_field.send_keys(text)
        driver.switch_to.default_content()
# Send the letter
        button_send = driver.find_element_by_xpath("//*[@id='screens']/div/div[1]/div/button")
        button_send.click()
# Wait until the letter is delivered
        time.sleep(3)
# Refresh page and compare mail_counter with number of letters in this moment
        driver.refresh()
        new_letter = int(driver.find_element_by_xpath("//*[@id='0']/span[2]").text)
        assert (mail_counter + 1) == new_letter
# Expected result: number of letters should be equal (mail_counter + 1)