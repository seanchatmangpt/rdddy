import asyncio
from playwright.async_api import async_playwright


class AsyncWebCrawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.visited_urls = set()

    async def extract_links(self, page):
        """Extract links from the page."""
        links = set()
        els = await page.query_selector_all("a")
        for el in els:
            link = await el.get_attribute("href")
            if link and link.startswith("http"):
                links.add(link)
        return links

    async def crawl(self, url, depth=0, max_depth=2):
        """Recursively crawl the given url."""
        if depth > max_depth or url in self.visited_urls:
            return
        self.visited_urls.add(url)
        print(f"Crawling {url}...")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            try:
                await page.goto(url, wait_until="networkidle")
                links = await self.extract_links(page)
                for link in links:
                    await self.crawl(link, depth + 1, max_depth)
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")
            await browser.close()

    async def start(self):
        """Starts the web crawling process."""
        await self.crawl(self.start_url)


async def main():
    cr = AsyncWebCrawler("https://google.com")
    await cr.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
