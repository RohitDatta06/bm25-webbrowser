from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse
from urllib import robotparser
import tldextract


def soup_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return title, text


def clean_url(href: str, parent: str) -> str:
    url = urljoin(parent, href)
    url, _ = urldefrag(url)
    return url


def same_registered_domain(u1: str, u2: str) -> bool:
    d1 = tldextract.extract(u1).registered_domain
    d2 = tldextract.extract(u2).registered_domain
    return d1 == d2


class Robots:
    def __init__(self, base_url: str):
        parsed = urlparse(base_url)
        self.rp = robotparser.RobotFileParser()
        self.rp.set_url(f"{parsed.scheme}://{parsed.netloc}/robots.txt")
        try:
            self.rp.read()
        except Exception:
            pass

    def allowed(self, url: str, ua: str = "*") -> bool:
        try:
            return self.rp.can_fetch(ua, url)
        except Exception:
            return True