from crawl4ai import AsyncWebCrawler

from utils import match_str


class BaseCrawler:
    _main_urls = []
    _filter_links_by_keys = []
    _house_name = ""

    def __init__(self, main_urls, filter_link_by_keys, house_name) -> None:
        self._main_urls = main_urls
        self._filter_links_by_keys = filter_link_by_keys
        self._house_name = house_name

    async def crawl_links(self, crawler: AsyncWebCrawler):
        links = []
        for url in self._main_urls:
            result = await crawler.arun(
                url=url,
            )
            if not result.success:
                raise Exception(result.error_message)

            for link in result.links["internal"]:
                href = link.get("href", "")
                if match_str(href, self._filter_links_by_keys):
                    links.append(href)

        return links

    async def crawl_auction(self, crawler, url) -> tuple[list, list]:
        pass

    def transform(self, items, metadata, link):
        pass

    async def run(self):
        try:
            async with AsyncWebCrawler() as crawler:
                links = await self.crawl_links(crawler)
                for link in links:
                    items, metadata = await self.crawl_auction(crawler, link)
                    self.transform(items, metadata, link)
                    return
        except Exception as e:
            print(e)

    def convert_to_model(self):
        pass
