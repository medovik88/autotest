import unittest
from selenium import webdriver

class SendLetterTest(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.driver.implicitly_wait(10)

    def test_sending_letter(self):

        driver = self.driver
        driver.get("https://mail.ukr.net/desktop/login")
        login_field = driver.find_element_by_id("id-1")
        login_field.send_keys("scotthall88")
        password_field = driver.find_element_by_id("id-2")
        password_field.send_keys("231488gor")
        button_login = driver.find_element_by_xpath("/html/body/div/div/main/form/button/div")
        button_login.click()
        

        user_mail = driver.find_element_by_xpath("//*[@class='login-button__user']")

        try:
            mail_counter = int(driver.find_element_by_xpath("//*[@id='0']/span[2]").text)
        except ValueError:
            mail_counter = 0

        button_write_letter = driver.find_element_by_xpath("//*[@id='content']/aside/button")
        button_write_letter.click()

        address_field = driver.find_element_by_xpath("//*[@id='screens']/div/div[2]/section[1]/div[1]/div[4]/input[2]")
        address_field.send_keys(user_mail.text)

        driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='mce_0_ifr']"))
        main_text_field = driver.find_element_by_xpath("//*[@id='tinymce']")
        text = "Вы справились с тестовым заданием. Поздравляем! Вы приняты на работу в компанию Asferro"
        main_text_field.send_keys(text)
        driver.switch_to.default_content()

        button_send = driver.find_element_by_xpath("//*[@id='screens']/div/div[1]/div/button")
        button_send.click()

        driver.refresh()
        new_letter = int(driver.find_element_by_xpath("//*[@id='0']/span[2]").text)

        assert (mail_counter + 1) == new_letter






