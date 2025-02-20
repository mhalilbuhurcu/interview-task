import random
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from decouple import config
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import instaloader
from TikTokApi import TikTokApi
import json
import os

class SocialMediaScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.tiktok_api = TikTokApi()
        self.ms_token = config('MS_TOKEN')  # Load ms_token from .env
        self.proxies = config('PROXY_LIST', default='').split(',')  # Load proxies from .env

    def get_instagram_followers_instaloader(self, username: str) -> Optional[int]:
        self._log(f"Fetching Instagram followers for {username} using Instaloader")
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            followers_count = profile.followers
            self._log(f"Instagram followers for {username}: {followers_count}")
            return followers_count
        except Exception as e:
            self._log(f"Error fetching Instagram followers: {e}")
        return None

    def get_tiktok_followers(self, username: str) -> Optional[int]:
        url = f"https://www.tiktok.com/@{username}"
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(url)
            time.sleep(5)  # Wait for JavaScript to load

            # Attempt to find the follower count using the provided XPath
            follower_count_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[2]/div[3]/h3/div[2]/strong'))
            )
            follower_count = follower_count_element.text.strip()

            # Convert follower count to integer
            if follower_count:
                if 'M' in follower_count:
                    return int(float(follower_count.replace('M', '').strip()) * 1_000_000)
                elif 'K' in follower_count:
                    return int(float(follower_count.replace('K', '').strip()) * 1_000)
                else:
                    return int(follower_count)

        except Exception as e:
            self._log(f"Error fetching TikTok followers: {e}")
            return None
        finally:
            driver.quit()

    def _parse_followers_count(self, soup) -> Optional[int]:
        try:
            # Find the followers count in the soup object
            followers_element = soup.find('strong', {'data-e2e': 'followers-count'})
            if followers_element:
                # Convert the followers count to an integer
                return followers_element.text.strip()
        except Exception as e:
            self._log(f"Error parsing followers count: {e}")
        return None

    def _log(self, message: str):
        print(f"[SocialMediaScraper] {message}")

    def close(self):
        pass  # No resources to clean up for Instaloader

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

    def _get_random_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            # Add more user agents as needed
        ]
        return random.choice(user_agents)

    async def _make_request(self, url: str) -> Optional[str]:
        headers = {
            'User-Agent': self._get_random_user_agent()
        }
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(random.uniform(2, 5))  # Random delay
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                return None

    def get_twitter_followers(self, username: str) -> Optional[int]:
        url = f"https://twitter.com/{username}"
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(url)
            time.sleep(5)  # Wait for JavaScript to load

            # Attempt to find the follower count in both div[4] and div[5]
            follower_count = None

            try:
                # Try to find the follower count in div[4]
                follower_count_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[4]/div[2]/a/span[1]/span'))
                )
                follower_count = follower_count_element.text.strip()
            except Exception:
                try:
                    # If not found, try to find it in div[5]
                    follower_count_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[5]/div[2]/a/span[1]/span'))
                    )
                    follower_count = follower_count_element.text.strip()
                except Exception as e:
                    print("Element not found in both locations, logging page source:")
                    print(driver.page_source)
                    return None

            # Convert follower count to integer
            if follower_count:
                if 'M' in follower_count:
                    return int(float(follower_count.replace('M', '').strip()) * 1_000_000)
                elif 'K' in follower_count:
                    return int(float(follower_count.replace('K', '').strip()) * 1_000)
                else:
                    return int(follower_count)

        except Exception as e:
            self._log(f"Error fetching Twitter followers: {e}")
            return None
        finally:
            driver.quit()