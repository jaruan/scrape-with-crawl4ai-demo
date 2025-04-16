from dotenv import load_dotenv
from house.phillips.crawl import PhillipsCrawler
from house.christies.crawl import ChristiesCrawler
import asyncio

load_dotenv()


async def main():
    # await PhillipsCrawler().run()
    await ChristiesCrawler().run()


if __name__ == "__main__":
    asyncio.run(main())
