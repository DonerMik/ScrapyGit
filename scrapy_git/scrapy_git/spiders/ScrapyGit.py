import pathlib
from pathlib import Path

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..items import ScrapyGitItem, ScrapyLastCommit, ScrapyLastRelease

dir_path = pathlib.Path.home()
path = Path(dir_path, 'scrapy_git', 'link_user_git.txt')


class GitSpider(CrawlSpider):

    name = 'git_spider'
    allowed_domain = ['github.com']
    start_urls = []
    rules = (Rule(LinkExtractor(restrict_xpaths=['//a[@class="UnderlineNav-item "]',
                                                 '//a[@data-tab-item="repositories"]']), follow=True),
             Rule(LinkExtractor(restrict_xpaths=['//ul[@class="list-style-none d-flex"]']), follow=True),
             Rule(LinkExtractor(restrict_xpaths=['//h3[@class="wb-break-all"]']), callback='parse_item'),)

    def __init__(self):
        super(GitSpider, self).__init__()
        self.start_urls = input('Введите ссылки: ').split()

    def parse_commit(self, response):
        ''' Функция собирает информацию со странички коммитов'''

        l_i = ItemLoader(response.meta['item'], response)
        block_commit = response.xpath('//div[@class="TimelineItem TimelineItem--condensed pt-0 pb-2"]')
        l_c = ItemLoader(ScrapyLastCommit(), block_commit)
        l_c.add_xpath('author', '//*[contains(@class, "commit-author user-mention")]//text()')
        l_c.add_xpath('name', '//p[@class="mb-1"]//text()')
        l_c.add_xpath('datetime_UTC', '//relative-time[@class="no-wrap"]/@datetime')
        x = l_c.load_item()

        l_i.add_value('info_last_commit', x)
        item = l_i.load_item()
        release_page = response.meta['release_url']
        try:
            yield response.follow(release_page, callback=self.parse_release, meta={'item': item})
        except IndexError:
            yield item

    def parse_release(self, response):
        ''' Функция собирает информацию со странички релизов'''

        l_i = ItemLoader(response.meta['item'], response)

        l_r = ItemLoader(ScrapyLastRelease(), response)
        l_r.add_xpath('version', '//span[@class="Label Label--success Label--large"]/../../h1/a/text()')
        l_r.add_xpath('datetime_UTC', '//local-time/@datetime')
        l_r.add_xpath('changelog', '//span[@class="Label Label--success Label--large"]/../../../..'
                                   '/div[@class="markdown-body my-3"]//text()')

        a = l_r.load_item()
        l_i.add_value('info_last_release', a)
        yield l_i.load_item()

    def parse_item(self, response):
        '''Парсинг странички репозитория'''

        l_i = ItemLoader(ScrapyGitItem(), response)
        l_i.add_xpath('name', '//div[@id="repository-container-header"]//strong/a/text()')
        start_url = response.xpath('//a[@class="url fn"]/@href').extract()[0]
        absolut_start_url = response.urljoin(start_url)
        l_i.add_value('user_url', absolut_start_url)
        l_i.add_value('url', response.url)
        l_i.add_xpath('about', '//div[@class="BorderGrid-cell"]/p/text()')
        l_i.add_xpath('site', '//div[@class="Layout-sidebar"]//a[@class="text-bold"]/text()')
        list_rating = response.xpath('//div[@class="BorderGrid-cell"]//a[1]//strong/text()').extract()
        try:
            l_i.add_value('count_stars', list_rating[0])
            l_i.add_value('count_forks', list_rating[2])
            l_i.add_value('count_watching', list_rating[1])
        except IndexError:
            yield l_i.load_item()
        l_i.add_xpath('count_commit', '//div[@class="flex-shrink-0"]//strong/text()')
        l_i.add_xpath('count_release', '//a[@class="Link--primary no-underline"]//span[@class="Counter"]/text()')

        commit_url = response.xpath('//ul[@class="list-style-none d-flex"]//@href').extract()
        item = l_i.load_item()

        if len(commit_url) == 0:
            return item

        try:
            release_page = response.xpath('//div[@class="BorderGrid-cell"]//'
                                          'a[@class="Link--primary no-underline"]/@href').extract()[0]
            yield response.follow(commit_url[0], callback=self.parse_commit,
                                  meta={'item': item,
                                        'release_url': release_page})
        except IndexError:
            yield item
