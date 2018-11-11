import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from challenge3.items import Challenge3Item

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    global html_string
    html_string = "<table border=1><tr><th>author</th><th>quote</th><th>tags</th></tr><tr>"
    def start_requests(self):
        start_urls = [
           #  "http://quotes.toscrape.com/page/1/",
            "http://quotes.toscrape.com/page/2/"
        ]
        Rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse", follow= True),)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse )
    
    def parse(self, response):
	#html_string = "<table border=1><tr><th>author</th><th>quote</th><th>tags</th></tr><tr>"
        page = response.url.split("/")[-2]
        full_quote = Selector(response).xpath('//div[@class="quote"]')
        for quote in full_quote:
            item = Challenge3Item()
            item['tags'] = quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract()
            item['quote'] = quote.xpath('span[@class="text"]/text()').extract()
            item['author'] = quote.xpath('span/small[@class="author"]/text()').extract()
            author_split = str(item['author']).split("'")
            quote_split = str(item['quote']).split("\u201")
            q = quote_split[1].replace('c','', 1)
	    tag_cleaned = str(item['tags']).replace('[','')
	    tag_cleaned = tag_cleaned.replace(']','')
	    tag_cleaned = tag_cleaned.replace('u\'','\'')
            #quote_split = q[1:]
	    global html_string
            html_string +=  "<tr><td>"+author_split[1]+"</td><td>"+q+"</td><td>"+tag_cleaned+"</td></tr>"
            yield item
        
        # follow next page links
        next_page = response.xpath('//li[@class="next"]/a/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = 'http://quotes.toscrape.com' + next_href
            request = scrapy.Request(url=next_page_url)
            yield request

        filename = "quotes.html"
        with open(filename, "wb") as f:
            f.write(html_string)
            # self.log("Saved File %s" % filename)
