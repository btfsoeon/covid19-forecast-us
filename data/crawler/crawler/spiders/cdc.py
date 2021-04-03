import json
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, SelectJmes
from crawler.items import CrawlerItem


class CdcSpider(scrapy.Spider):
    name = 'cdc'
    allowed_domains = ['https://covid.cdc.gov/covid-data-tracker']
    start_urls = ['https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_timeseries_state_CA_external/']

    def parse(self, response):
        jsonresp = json.loads(response.body_as_unicode())['integrated_county_timeseries_external_data']

        for county in jsonresp:
            loader = ItemLoader(item=CrawlerItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')

            #TODO

        yield loader.load_item()
        #pass
