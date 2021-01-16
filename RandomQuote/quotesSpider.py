import scrapy

class QuotesSpider(scrapy.Spider):

    name = "quotes"

    ### CODE TO EXTRACT QUOTE FROM BABELIO
    """
    # URL TO GET QUOTE FROM 
    start_urls = ['https://www.babelio.com/auteur/Frederic-Dard/7187/citations']

    def parse(self, response):
        # Loop to check all quotes
        for quote in response.css('div.post_con div.text.row div'):
            # Extraction format
            yield {'quote': quote.css('div ::text').extract_first()}

        # Go to next page if there is one.
        next_pages = response.css('div.pagination.row > a').extract()
        for index, page in enumerate(next_pages):
            if 'class="active"' in page:
                n_page = next_pages[index + 1]
                next_page = scrapy.selector.Selector(text=n_page).xpath('//a/@href').extract()
                next_page_url = next_page[0]
                if index == (len(next_pages) - 1):
                    next_page = False

        if next_page:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
    """
    ### CODE TO EXTRACT QUOTES FROM 'http://quotes.toscrape.com/tag/humor/',

    start_urls = ['http://quotes.toscrape.com/tag/humor/']
    def parse(self, response):
            # Loop to check all quotes
            for quote in response.css('div.quote'):
                # Extraction format
                yield {'quote': quote.css('span.text::text').extract_first()}

            # Go to next page if there is one.
            next_page = response.css('li.next a::attr("href")').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
