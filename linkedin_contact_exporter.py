from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
from time import sleep


driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/uas/login")
sleep(randint(1,3))
driver.find_element_by_xpath(".//*[@id='session_key-login']").send_keys('jordandhart@gmail.com')
sleep(randint(1,4))
driver.find_element_by_xpath(".//*[@id='session_password-login']").send_keys('password')
sleep(randint(1,5))
driver.find_element_by_xpath(".//*[@id='btn-primary']").click()
sleep(randint(4, 6))
driver.get("https://www.linkedin.com/people/export-settings")
driver.find_element_by_xpath(".//*[@id='main']/div/form/ul/li[2]/input").click()
#driver.close()
