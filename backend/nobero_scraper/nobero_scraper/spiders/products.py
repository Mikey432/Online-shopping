from pathlib import Path
import scrapy # type: ignore
from datetime import datetime
import pymongo # type: ignore

client = pymongo.MongoClient("mongodb+srv://mayankuchariya0:mayank123@cluster0.u0zlvya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["nobero_database"]
def insertToDB(id,product_name,number,image_url,rating):
    collection = db["products"]
    
    doc = {"id": id,"title":product_name,"price":number,"image":image_url,"rating":rating,"qty":1,"sizes": ['S', 'M', 'L', 'XL'],"colors": ['Black', 'White', 'Gray'],"description": 'A classic plain t-shirt with a comfortable fit.'}
    collection.insert_one(doc)

class NoberoSpider(scrapy.Spider):
    name = "nobero"
    start_urls = ["https://nobero.com/pages/men"]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"products-{page}.html"
        productdetail = {}
        self.log(f"Saved file {filename}")
        # Path(filename).write_bytes(response.body)

        # for product in response.css('.slick-track'): 
        id = 0
        products = response.css('section.product-card-container')
        for product in products:
            product_name = product.css('h3::text').get().strip()
            # print(product_name)
            price = product.css('#price__regular span spanclass::text').get()
            number_str = price.replace("₹", "")
            number = int(number_str)
            # print(price)
            image_url = product.css('img::attr(src)').get()
            # print(image_url)
            rating =  product.css('article span::text').get(default='').strip()
            # print(rating)
            insertToDB(id,product_name,number,image_url,rating)
            id = id+1
