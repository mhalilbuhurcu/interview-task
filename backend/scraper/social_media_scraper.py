import random
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from decouple import config
import aiohttp
import asyncio

class SocialMediaScraper:
    def __init__(self):
        self.proxies = config('PROXY_LIST', default='').split(',')
        self.user_agent = UserAgent()
        self.session = None

    def _get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    def _get_headers(self):
        return {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    def _get_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        if proxy := self._get_random_proxy():
            chrome_options.add_argument(f'--proxy-server={proxy}')
        
        chrome_options.add_argument(f'user-agent={self.user_agent.random}')
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    async def _make_request(self, url: str) -> Optional[str]:
        headers = self._get_headers()
        proxy = self._get_random_proxy()

        try:
            async with aiohttp.ClientSession() as session:
                await asyncio.sleep(random.uniform(2, 5))
                async with session.get(
                    url,
                    headers=headers,
                    proxy=f"http://{proxy}" if proxy else None,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    return None
        except Exception as e:
            print(f"Error making request: {e}")
            return None

    async def get_instagram_followers(self, username: str) -> Optional[int]:
        try:
            driver = self._get_chrome_driver()
            driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(random.uniform(3, 5))
            
            followers_element = driver.find_element(
                By.XPATH,
                "//meta[@property='og:description']"
            )
            content = followers_element.get_attribute('content')
            
            followers = int(content.split('Followers')[0].strip().replace(',', ''))
            return followers
        except Exception as e:
            print(f"Error scraping Instagram: {e}")
            return None
        finally:
            if 'driver' in locals():
                driver.quit()

    async def get_tiktok_followers(self, username: str) -> Optional[int]:
        url = f'https://www.tiktok.com/@{username}'
        html = await self._make_request(url)
        
        if html:
            try:
                # Implementation depends on TikTok's current structure
                # You might need to use regular expressions or BS4 here
                return 0  # Placeholder
            except Exception as e:
                print(f"Error parsing TikTok data: {e}")
        return None

    async def get_twitter_followers(self, username: str) -> Optional[int]:
        url = f'https://twitter.com/{username}'
        html = await self._make_request(url)
        
        if html:
            try:
                # Implementation depends on Twitter's current structure
                return 0  # Placeholder
            except Exception as e:
                print(f"Error parsing Twitter data: {e}")
        return None 