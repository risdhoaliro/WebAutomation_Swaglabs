from selenium.webdriver.common.by import By
import time
import data.userData as userData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CheckoutPage:
        
    @staticmethod
    def checkout_process_e2e(driver):
        txtuname = driver.find_element(By.ID, "user-name")
        txtuname.send_keys(userData.STANDARD_USER)
        txtpass = driver.find_element(By.ID, "password")
        txtpass.send_keys(userData.STANDARD_PASSWORD)
        btnlogin = driver.find_element(By.ID, "login-button")
        btnlogin.click()
        time.sleep(3)
        
        #Add Item To Card   
        card_one = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
        card_one.click()
        card_two = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bike-light']")
        card_two.click()
        card_tree = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']")
        card_tree.click()
        
        cart_icon = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "shopping_cart_container")))
        cart_icon.click()
        
        #Validation Item For Card
        expected_item_count = 3
        for _ in range(10):
            item_count_element = driver.find_element(By.XPATH, "//span[contains(text(), '3')]")
            if item_count_element:
                actual_item_count = int(item_count_element.text)
                if actual_item_count == expected_item_count:
                    print(f"There are {expected_item_count} items in the cart.")
                    break
            time.sleep(1)
        else:
            print(f"There are not {expected_item_count} items in the cart.")
        
        # Validation: Check product names and prices in the cart
        product_names = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        product_prices = ["29.99", "9.99", "15.99"]

        for i in range(len(product_names)):
            product_name_xpath = f"//div[@class='inventory_item_name'][text()='{product_names[i]}']"
            product_price_xpath = f"//div[@class='inventory_item_price'][text()='{product_prices[i]}']"

            wait = WebDriverWait(driver, 10)
        try:
            product_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_name_xpath)))
            product_price_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_price_xpath)))
            
            product_name = product_name_element.text
            product_price = product_price_element.text
            
            print(f"Product {i + 1}:")
            print(f"Name: {product_name}")
            print(f"Price: {product_price}")
        except TimeoutException:
            print(f"Timeout: Product {i + 1} not found")
        
        time.sleep(5)
        #Click button checkout
        btn_checkout = driver.find_element(By.XPATH, "//button[@id='checkout']")
        btn_checkout.click()
        
        #Input data Information - if firstname not input - Negative Case 
        waiting = WebDriverWait(driver, 10)
        firstname = waiting.until(EC.presence_of_element_located((By.ID, "first-name")))
        firstname.send_keys(userData.EMPTY_STRING)
        lastname = driver.find_element(By.ID, "last-name")
        lastname.send_keys(userData.LASTNAME)
        zipcode = driver.find_element(By.ID, "postal-code")
        zipcode.send_keys(userData.ZIP)
        btn_continue = driver.find_element(By.NAME, "continue")
        btn_continue.click()
        #validation eror message
        error_message = driver.find_element(By.XPATH, '//*[@id="checkout_info_container"]/div/form/div[1]/div[4]/h3').text
        assert "Error: First Name is required" in error_message, f"Pesan kesalahan tidak sesuai dengan yang diharapkan. Sebenarnya: {error_message}"
        time.sleep(5)
        
        #Input data Information - Positive Case
        firstname = driver.find_element(By.ID, "first-name")
        firstname.send_keys(userData.FIRSTNAME)
        lastname = driver.find_element(By.ID, "last-name")
        lastname.send_keys(userData.LASTNAME)
        zipcode = driver.find_element(By.ID, "postal-code")
        zipcode.send_keys(userData.ZIP)
        btn_continue = driver.find_element(By.NAME, "continue")
        btn_continue.click()
        time.sleep(5)
        
        #Validation Subtitle Checkout: Overview 
        assert driver.find_element(By.XPATH, "//span[contains(text(),'Checkout: Overview')]").text == "Checkout: Overview", "Teks subheader tidak sesuai."
        
        # Subtotal Calculation
        subtotal_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        subtotal = 0.0

        for price in subtotal_elements:
            subtotal += float(price.text[1:])  

        expected_total = 55.97  
        assert subtotal == expected_total, f"Subtotal tidak sesuai. Sebenarnya: {subtotal}, Diharapkan: {expected_total}"
        print(f"Expected Subtotal {subtotal}")
        time.sleep(10)
        btn_finish = driver.find_element(By.ID, "finish")
        btn_finish.click()
        
        waiting = WebDriverWait(driver, 10)
        waiting.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Checkout: Complete!')]")))
        
        #Validation Subtitle Checkout: Complete! 
        assert driver.find_element(By.XPATH, "//span[contains(text(),'Checkout: Complete!')]").text == "Checkout: Complete!", "Teks subheader tidak sesuai."
        assert driver.find_element(By.XPATH, "//h2[contains(text(),'Thank you for your order!')]").text == "Thank you for your order!", "Teks deskripsi tidak sesuai."
        
        #Validation Item For Card after Checkout
        cart_item_count_selector = (By.CLASS_NAME, "shopping_cart_badge")
        cart_items = driver.find_elements(*cart_item_count_selector)
        if cart_items:
            num_items_in_cart = cart_items[0].text
            result = int(num_items_in_cart)
            print(f"Jumlah barang di keranjang: {result}")
        else:
            result = 0
        print("Keranjang belanja kosong.")
        return result
