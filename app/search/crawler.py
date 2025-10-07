import time
import requests
from collections import deque
from typing import Callable
from urllib.parse import urlparse
from .utils import soup_text, clean_url, same_registered_domain, Robots


class Crawler:
    def __init__(self, seed_url: str, max_pages=10000, delay=0.5, same_site=True, user_agent="MiniSearchBot/0.1"):
        self.seed = seed_url
        self.max_pages = max_pages
        self.delay = delay
        self.same_site = same_site
        self.ua = user_agent
        self.visited = set()
        self.frontier = deque([seed_url])
        self.robots = Robots(seed_url)
        self.seed_domain = urlparse(seed_url).netloc

    def crawl(self, on_page: Callable[[str, str, str], None]):
        session = requests.Session()
        headers = {"User-Agent": self.ua}
        count = 0
        while self.frontier and count < self.max_pages:
            url = self.frontier.popleft()
            if url in self.visited:
                continue
            if not self.robots.allowed(url, self.ua):
                continue
            self.visited.add(url)
            try:
                r = session.get(url, timeout=10, headers=headers)
                ctype = r.headers.get("Content-Type", "")
                if "text/html" not in ctype:
                    continue
                title, text = soup_text(r.text)
                on_page(url, title, text)
                count += 1
                # enqueue children
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    child = clean_url(a["href"], url)
                    if self.same_site and not same_registered_domain(self.seed, child):
                        continue
                    if child not in self.visited:
                        self.frontier.append(child)
                time.sleep(self.delay)
            except requests.RequestException:
                continue