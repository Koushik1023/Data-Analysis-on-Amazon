from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

search_query = input("Enter the product you want to search on Amazon.in: ")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.amazon.in/")

wait = WebDriverWait(driver, 13)
search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
search_box.send_keys(search_query)
search_box.submit()

time.sleep(5)

for _ in range(4):
    driver.execute_script("window.scrollBy(0, 2000);")
    time.sleep(3)

products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

scraped_data = []

for product in products:
    try:
        sponsored = product.find_element(By.XPATH, ".//span[normalize-space()='Sponsored']")
        if not sponsored:
            continue
    except:
        continue

    try:
        title = product.find_element(By.TAG_NAME, 'h2').text.strip()
    except:
        title = "N/A"

    try:
        product_url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        product_url = "N/A"

    brand = "N/A"
    try:
        brand = product.find_element(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']").text.strip()
    except:
        try:
            brand = product.find_element(By.XPATH, ".//span[@class='a-size-base a-color-base']").text.strip()
        except:
            try:
                brand = product.find_element(By.XPATH, ".//span[@class='a-size-small a-color-base']").text.strip()
            except:
                try:
                    brand = product.find_element(By.XPATH, ".//h5").text.strip()
                except:
                    if title != "N/A":
                        brand = " ".join(title.split()[:2])

    rating = "N/A"
    try:
        rating_elem = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
        rating_text = rating_elem.get_attribute("innerHTML").strip()
        rating = rating_text.split(' ')[0]
    except:
        pass

    try:
        reviews = product.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text.strip()
    except:
        reviews = "0"

    price = "N/A"
    try:
        price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text.replace(",", "").strip()
        price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text.strip()
        price = price_whole + "." + price_fraction
    except:
        try:
            price = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text.replace(",", "").strip()
        except:
            pass

    try:
        image_url = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except:
        image_url = "N/A"

    scraped_data.append({
        "Title": title,
        "Brand": brand,
        "Rating": rating,
        "Reviews": reviews,
        "Price": price,
        "Image URL": image_url,
        "Product URL": product_url
    })

filename = f"sponsored_{search_query.replace(' ', '_').lower()}_raw.csv"
df = pd.DataFrame(scraped_data)
df.to_csv(filename, index=False)

print(f"Scraped {len(df)} sponsored products for '{search_query}'.")
print(f"Data saved to: {filename}")

driver.quit()
