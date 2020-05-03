from selenium import webdriver
from time import sleep
import pandas as pd
import pymongo

#set up connection to mongodb cluster
client = pymongo.MongoClient("mongodb+srv://marwa:marwa_98@cluster0-c3mtu.gcp.mongodb.net/test?retryWrites=true&w=majority")

#set up the selenium chrome driver
chromedriver_path= 'C:\Program Files/chromedriver.exe'
driver= webdriver.Chrome(executable_path = chromedriver_path)

link= 'https://www.aliexpress.com/'
driver.get(link)
sleep(3)
driver.find_element_by_class_name('close-layer').click()
sleep(3)
driver.find_element_by_link_text('Flash Deals').click()
sleep(1)

#scroll to the very bottom of the page


last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    else:
        last_height= new_height


products=driver.find_elements_by_css_selector('div.deals-item-inner')

# product=products[0]
# print(product.find_element_by_css_selector('h3.item-details-title').text)
# print(product.find_element_by_css_selector('div.current-price').text)
# print(product.find_element_by_css_selector('span.folatR').text)
# print(product.find_element_by_tag_name('img').get_attribute('src'))
#print(product.find_element_by_css_selector('span.solder').get_attribute("innerHTML"))

database=[]
for product in products:
    title=product.find_element_by_css_selector('h3.item-details-title').text
    current_price = product.find_element_by_css_selector('div.current-price').text
    discount= product.find_element_by_css_selector('span.folatR').text
    quantity_sold = product.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/a/div[2]/div[3]/div[2]/span').get_attribute("innerHTML")
    image_link= product.find_element_by_tag_name('img').get_attribute('src')
    
    product_info={
        "title": title, 
        "current_price": current_price,
        "discount": discount, 
        "image_link" : image_link,
        "quantity_sold": quantity_sold
    }
    database.append(product_info)

populated_db=pd.DataFrame(database)
#populated_db.reset_index(inplace=True)
print(populated_db)

db= client['aliexpress']
product_db = db['product-flashdeals']
db.product_db.insert_many(populated_db.to_dict('records'))