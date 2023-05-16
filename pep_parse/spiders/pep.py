import scrapy
import re

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        num_idx_table = response.css('#numerical-index')
        tr_list = num_idx_table.css('tr')
        for pep in tr_list:
            td_list = pep.css('td')
            try:
                href = td_list[1].css("a::attr(href)").get()
                yield response.follow(href, callback=self.parse_pep)
            except Exception:
                pass

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        reg_num = r'(\d+)'
        reg_name = r'....[\s–]+(.*)'
        number = re.search(reg_num, title)
        name = re.search(reg_name, title)
        dd = response.css('dd.field-even')
        status = dd.css('abbr::text').get()
        data = {
            'number': number.group(1),
            'name': name.group(1),
            'status': status
        }
        yield PepParseItem(data)
