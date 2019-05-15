import scrapy
from ..items import Product
from scrapy_splash import SplashRequest


class MySpider(scrapy.Spider):
    name = "coles"
    start_urls = [
        "https://shop.coles.com.au/a/a-national/everything/browse/entertaining-at-home/cheese-board-selections?pageNumber=1"
    ]

    lua_script = """
    function main(splash, args)
      assert(splash:go(args.url))
      assert(splash:wait(0.5))
      return {
        html = splash:html(),
        png = splash:png(),
      }
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            # yield SplashRequest(url, self.parse, endpoint='render.json', args={"wait": 5, "png": 1, "render_all": 1})
            # yield SplashRequest(url, self.parse, args={"wait": 5})
            yield SplashRequest(
                url,
                self.parse,
                endpoint="execute",
                magic_response=True,
                meta={"handle_httpstatus_all": True},
                args={"lua_source": self.lua_script},
            )

    def parse(self, response):
        print("PRINTING BODY")
        print(response.body)
        # item = Product()
        # for product in response.css('shelfProductTile'):
        #     item['product_name'] = product.css('shelfProductTile-description::text').extract_first()
        #     yield item

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
