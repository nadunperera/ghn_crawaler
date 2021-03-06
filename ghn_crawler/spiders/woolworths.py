import scrapy
from ..items import Product
from scrapy_splash import SplashRequest


class MySpider(scrapy.Spider):
    name = "woolworths"
    start_urls = ["https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge"]

    def start_requests(self):
        for url in self.start_urls:
            # Uncomment below if you want a screenshot of the response
            # yield SplashRequest(url, self.parse, endpoint='render.json', args={"wait": 5, "png": 1, "render_all": 1})
            yield SplashRequest(url, self.parse, args={"wait": 5})

    def parse(self, response):
        # Uses the product model in items.py
        # item = Product()
        # for product in response.css('shelfProductTile'):
        #     item['product_name'] = product.css('shelfProductTile-description::text').extract_first()
        #     yield item

        # Get screenshot of the output
        # imgdata = base64.b64decode(response.data['png'])
        # filename = "some_image.png"
        # with open(filename, "wb") as f:
        #     f.write(imgdata)

        products = response.xpath("//wow-shelf-product-tile")

        for product in products:
            yield {
                "product": product.xpath(".//h3/a/text()").extract_first(),
                "price_dollars": product.xpath(
                    ".//span[@class='price-dollars']/text()"
                ).extract_first(),
                "price_cents": product.xpath(
                    ".//span[@class='price-cents']/text()"
                ).extract_first(),
            }
