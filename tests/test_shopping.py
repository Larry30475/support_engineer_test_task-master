from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def test_shopping(driver):
    global bestbuy_price
    product = "samsung galaxy s22"
    driver = webdriver.Chrome()

    driver.get("https://www.amazon.com")
    search_box = driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
    search_box.send_keys(product)
    search_box.submit()
    products_list = driver.find_elements_by_xpath('//div[@data-component-type="s-search-result"]')
    max_review_product = 0
    max_i = 0
    for product_from_list in products_list:
        try:
            review = product_from_list.find_element_by_xpath(".//span[@class='a-size-base']")
            review_text = review.text
            if max_review_product < float(review_text):
                max_review_product = float(review_text)
                max_i = products_list.index(product_from_list)
        except:
            review_text = "N/A"
    amazon_price_whole = products_list[max_i].find_element_by_xpath('.//span[@class="a-price-whole"]').text
    amazon_price_whole_arr = amazon_price_whole.split(",")
    amazon_price_whole_parsed = ""
    for price in amazon_price_whole_arr:
        amazon_price_whole_parsed += price
    amazon_price_fraction = products_list[max_i].find_element_by_xpath('.//span[@class="a-price-fraction"]').text
    amazon_price = float(amazon_price_whole_parsed + "." + amazon_price_fraction)

    driver.get("https://www.bestbuy.com")
    driver.find_element_by_xpath('//*[@class="us-link"]').click()
    search_box = driver.find_element_by_xpath('//input[@class="search-input"]')
    search_box.send_keys(product)
    search_box.submit()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sku-title")))
    max_review_product = 0
    max_i = 0
    try:
        wait = WebDriverWait(driver, 10)
        products_list = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sku-title"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products_list = soup.find_all('li', class_="sku-item")
        for products in products_list:
            review = products.find('p', class_="visually-hidden")
            review_str_arr = review.text.split(" ")
            review_str = review_str_arr[1]
            if review_str != "Yet":
                if max_review_product < float(review_str):
                    max_review_product = float(review_str)
                    max_i = products_list.index(products)
        bestbuy_price_unparsed = products_list[max_i].find('span', class_="sr-only").text
        bestbuy_price_str_arr = bestbuy_price_unparsed.split(" ")
        bestbuy_price = float(bestbuy_price_str_arr[len(bestbuy_price_str_arr) - 1][1:])
    except Exception as e:
        print("An error occurred: ", e)
    driver.quit()
    # once script completed the line below should be uncommented.
    assert amazon_price > bestbuy_price
