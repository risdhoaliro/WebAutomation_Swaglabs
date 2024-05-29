import pytest
import allure
from selenium import webdriver
import data.userData as userData
from pages.LoginPage import LoginPage
from pages.CheckoutPage import CheckoutPage
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver_setup():
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(userData.URL)
    driver.implicitly_wait(userData.implicit_wait_time)
    yield driver
    driver.quit()

@pytest.mark.test01_login_with_valid_user
def test01_login_with_valid_user(driver_setup):
    LoginPage.login_valid(driver_setup)

@pytest.mark.test02_login_with_locked_out_user
def test02_login_with_locked_out_user(driver_setup):
    LoginPage.login_locked(driver_setup)
    
@pytest.mark.test03_login_with_checkout_user
def test03_login_with_checkout_user(driver_setup):
    CheckoutPage.checkout_process_e2e(driver_setup)
