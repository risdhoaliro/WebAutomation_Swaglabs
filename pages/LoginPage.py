from selenium.webdriver.common.by import By
import time
import data.userData as userData

class LoginPage:
    
    @staticmethod
    def login_valid(driver):
        txtuname = driver.find_element(By.ID, "user-name")
        txtuname.send_keys(userData.STANDARD_USER)
        txtpass = driver.find_element(By.ID, "password")
        txtpass.send_keys(userData.STANDARD_PASSWORD)
        btnlogin = driver.find_element(By.ID, "login-button")
        btnlogin.click()
        time.sleep(3)
        print("test_login_valid_user finished successfully.")

    @staticmethod
    def login_locked(driver):
        txtuname = driver.find_element(By.ID, "user-name")
        txtuname.send_keys(userData.LOCKED_OUT_USER)
        txtpass = driver.find_element(By.ID, "password")
        txtpass.send_keys(userData.STANDARD_PASSWORD)
        btnlogin = driver.find_element(By.ID, "login-button")
        btnlogin.click()
        time.sleep(3)
        error_message = driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form')
        print(f"Error message: {error_message.text}")
        print("test_login_locked_out_user finished successfully.")