from crawl4ai import AsyncWebCrawler

from utils import match_str


class BaseCrawler:
    _main_urls = []
    _filter_keys = []
    _item_schema = {}
    _metadata_schema = {}
    _house_name = ""

    def __init__(
        self, main_urls, filter_keys, item_schema, metadata_schema, house_name
    ) -> None:
        self._main_urls = main_urls
        self._filter_keys = filter_keys
        self._item_schema = item_schema
        self._metadata_schema = metadata_schema
        self._house_name = house_name

    async def crawl_links(self, crawler: AsyncWebCrawler):
        links = []
        for url in self._main_urls:
            result = await crawler.arun(
                url=url,
            )
            for link in result.links["internal"]:
                href = link.get("href", "")
                if match_str(href, self._filter_keys):
                    links.append(href)

        return links

    async def crawl_auction(self, crawler, url) -> tuple[list, list]:
        pass

    def transform(self, items, metadata, link):
        pass

    async def run(self):
        async with AsyncWebCrawler() as crawler:
            links = await self.crawl_links(crawler)
            for link in links:
                items, metadata = await self.crawl_auction(crawler, link)
                self.transform(items, metadata, link)
                return

    def convert_to_model(self):
        pass
