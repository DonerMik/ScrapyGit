import pathlib
from pathlib import Path

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from ..items import ScrapyGitItem, ScrapyLastCommit, ScrapyLastRelease

dir_path = pathlib.Path.home()
path = Path(dir_path, 'scrapy_git', 'link_user_git.txt')


class GitSpider(CrawlSpider):
    name = 'git_spider'
    allowed_domain = ['github.com']
    start_urls = []
    rules = (Rule(LinkExtractor(restrict_xpaths=['//a[@class="UnderlineNav-item "]',
                                                 '//a[@data-tab-item="repositories"]']), follow=True),
             Rule(LinkExtractor(restrict_xpaths=['//h3[@class="wb-break-all"]']), callback='parse_item'),)

    def __init__(self):
        super(GitSpider, self).__init__()
        self.start_urls = input('Введите ссылки: ').split()
        # [self.start_urls.append(url) for url in urls]
    #
    #     # for line in open('../link_user_git.txt', 'r').readlines():
    #     #     self.start_urls.append(line)


    def parse_release(self, response):
        l_i = ItemLoader(response.meta['item'], response)
        l_r = ItemLoader(ScrapyLastRelease(), response)
        l_r.add_xpath('version', '//span[@class="Label Label--success Label--large"]/../../h1/a/text()')
        l_r.add_xpath('datetime_UTC', '//local-time/@datetime')
        l_r.add_xpath('changelog', '//span[@class="Label Label--success Label--large"]/../../../../div/p/text()')
        a = l_r.load_item()
        l_i.add_value('info_last_release', a)

        yield l_i.load_item()

    def parse_item(self, response):
        l_i = ItemLoader(ScrapyGitItem(), response)
        l_i.add_xpath('name', '//div[@id="repository-container-header"]//strong/a/text()')
        l_i.add_value('url', response.url)
        l_i.add_xpath('about', '//div[@class="BorderGrid-cell"]/p/text()')
        l_i.add_xpath('site', '//div[@class="Layout-sidebar"]//a[@class="text-bold"]/text()')
        list_rating = response.xpath('//div[@class="BorderGrid-cell"]//a[1]//strong/text()').extract()
        l_i.add_value('count_stars', list_rating[0])
        l_i.add_value('count_forks', list_rating[2])
        l_i.add_value('count_watching', list_rating[1])
        l_i.add_xpath('count_commit', '//div[@class="flex-shrink-0"]//strong/text()')
        l_i.add_xpath('count_release', '//a[@class="Link--primary no-underline"]//span[@class="Counter"]/text()')
        l_c = ItemLoader(ScrapyLastCommit(), response)

        l_c.add_xpath('author', '//a[@class="commit-author user-mention"]/text()')
        l_c.add_xpath('name',
                      '//div[@class="Box-header position-relative"]//pre/text()')
        l_c.add_xpath('datetime_UTC', '//a[@class="Link--secondary ml-2"]/relative-time/@datetime')
        info_commit = l_c.load_item()
        l_i.add_value('info_last_commit', info_commit)

        release_page = response.xpath('//div[@class="BorderGrid-cell"]//'
                                      'a[@class="Link--primary no-underline"]/@href').extract()[0]
        yield response.follow(release_page, callback=self.parse_release,
                              meta={'item': l_i.load_item()})
