import scrapy
from ..items import Product
from scrapy_splash import SplashRequest


class MySpider(scrapy.Spider):
    name = "woolworths"
    start_urls = ["https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge/cheese"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={"wait": 5})

    def parse(self, response):
        # item = Product()
        # for product in response.css('shelfProductTile'):
        #     item['product_name'] = product.css('shelfProductTile-description::text').extract_first()
        #     yield item

        _file = "parsed.html"
        with open(_file, "wb") as f:
            f.write(response.body)

        products = response.xpath(
            "//wow-shelf-product-tile"
        )
        print("PRODUCT LENGTH: {}".format(len(products)))
        for product in products:
            yield {"product": product.xpath(".//h3/a/text()").extract_first()}
