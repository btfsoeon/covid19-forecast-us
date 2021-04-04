import json
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, SelectJmes
from ccrawler.items import CcrawlerItem

# STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI',
#           'ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN',
#           'MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH',
#           'OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA',
#           'WA','WV','WI','WY']


class CdcSpider(scrapy.Spider):
    name = 'cdc'
    allowed_domains = ['https://covid.cdc.gov/covid-data-tracker']
    start_urls = ['https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_county_condensed_data']

    jmes_paths = {
        'date': 'Date',
        'state': 'StateName',
        'county': 'County',
        'vaccination_pct': 'Series_Complete_Pop_Pct',
    }

    def parse(self, response):
        # this is the problem, see
        # https://docs.scrapy.org/en/latest/topics/request-response.html
        jsonresp = json.loads(response.body_as_unicode())['vaccination_county_condensed_data']

        for vacc in jsonresp:

            loader = ItemLoader(item=CcrawlerItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(',')

            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(vacc))

            yield loader.load_item()
