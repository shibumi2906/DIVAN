import scrapy

class DivanLightingSpider(scrapy.Spider):
    name = 'divan_lighting'
    allowed_domains = ['divan.ru']
    start_urls = ['https://www.divan.ru/category/osveshchenie']  # примерный URL, уточните его

    def parse(self, response):
        # Поиск элементов, содержащих информацию об источниках освещения
        for product in response.css('div.product-item'):
            yield {
                'title': product.css('a.product-item__title::text').get().strip(),
                'price': product.css('span.product-item__price-value::text').get().strip(),
                'link': response.urljoin(product.css('a.product-item__title::attr(href)').get())
            }

        # Пагинация: поиск и переход по страницам
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
