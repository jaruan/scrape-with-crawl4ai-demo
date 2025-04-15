from dotenv import load_dotenv
from house.phillips.crawl import PhillipsCrawler
import asyncio

load_dotenv()


async def main():
    await PhillipsCrawler().run()


if __name__ == "__main__":
    asyncio.run(main())
