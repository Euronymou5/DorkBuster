import base64
import random
import re
import urllib.parse
import urllib.request
from typing import Callable, Dict, List, Optional, Set, Tuple
import requests
from bs4 import BeautifulSoup

try:
    import primp
    PRIMP_AVAILABLE = True
except ImportError:
    primp = None
    PRIMP_AVAILABLE = False

DEFAULT_DORK_TEMPLATES = [
    "allintext:{target}",
    "allinurl:{target}",
    "intext:{target} filetype:pdf",
    "intext:{target} filetype:venv",
    "intitle:{target}",
    "intext:{target} filetype:pcf",
    "intext:{target}",
    "inurl:{target}",
    "intitle:index.of {target}",
    "filetype:conf {target}",
    "intitle:{target} filetype:doc OR filetype:pdf OR filetype:txt",
    "intitle:{target} filetype:sql",
    "intitle:{target} filetype:log",
    "intitle:{target} filetype:backup OR filetype:bkf OR filetype:sqlbak",
    "intitle:{target} filetype:err",
    "intitle:{target} filetype:htpasswd OR filetype:htaccess",
    "intitle:{target} filetype:config OR filetype:ini OR filetype:conf",
]

DEFAULT_COMMON_DORKS = [
    'intitle:"index of"',
    'inurl:admin.php',
    'inurl:login.php',
    'intext:password filetype:log',
    'filetype:sql "dump"',
    'filetype:env "DB_PASSWORD"',
    'intitle:"index of" intext:backup',
    'inurl:wp-config.php',
    'filetype:conf intext:password',
    'intitle:"Dashboard" inurl:admin',
]

DEFAULT_TLDS = ["com", "com.tw", "co.in", "be", "de", "co.uk", "co.ma", "dz", "ru", "ca"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
]

def format_requests_proxies(proxy: Optional[str]) -> Optional[Dict[str, str]]:
    """Convierte una cadena de proxy en el diccionario esperado por requests."""
    if not proxy or not proxy.strip():
        return None
    p = proxy.strip()
    return {"http": p, "https": p}

def get_default_dorks(target: str = "", count: Optional[int] = None) -> List[str]:
    if target:
        formatted = [template.format(target=target) for template in DEFAULT_DORK_TEMPLATES]
    else:
        formatted = list(DEFAULT_COMMON_DORKS)
    if count is not None and count > 0:
        return random.sample(formatted, min(count, len(formatted)))
    return formatted

def normalize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    try:
        parsed = urllib.parse.urlparse(url)
        scheme = parsed.scheme.lower() or "https"
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip("/")
        
        query_params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=False)
        filtered_params = [
            (k, v) for k, v in query_params 
            if not k.lower().startswith("utm_") and k.lower() not in ("ref", "fbclid", "gclid")
        ]
        new_query = urllib.parse.urlencode(filtered_params)
        return urllib.parse.urlunparse((scheme, netloc, path, parsed.params, new_query, ""))
    except Exception:
        return url.rstrip("/").lower()

def deduplicate_results(results: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], int]:
    seen: Set[str] = set()
    unique_list: List[Dict[str, str]] = []
    duplicates_count = 0

    for item in results:
        raw_url = item.get("url", "").strip()
        if not raw_url:
            continue
        norm = normalize_url(raw_url)
        if norm in seen:
            duplicates_count += 1
            continue
        seen.add(norm)
        unique_list.append(item)

    return unique_list, duplicates_count

class SearchEngineBase:
    name: str = "Base"
    last_error: Optional[str] = None

    def search(
        self,
        query: str,
        max_results: int = 10,
        pause: float = 0.0,
        stop_check: Optional[Callable[[], bool]] = None,
        proxy: Optional[str] = None,
    ) -> List[str]:
        raise NotImplementedError


class BingEngine(SearchEngineBase):
    name = "Bing"

    def search(
        self,
        query: str,
        max_results: int = 10,
        pause: float = 0.0,
        stop_check: Optional[Callable[[], bool]] = None,
        proxy: Optional[str] = None,
    ) -> List[str]:
        self.last_error = None
        results: List[str] = []
        encoded_query = urllib.parse.quote_plus(query)
        num_query = max(int(max_results), 10)
        url = f"https://www.bing.com/search?q={encoded_query}&count={num_query}"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        }
        clean_proxy = proxy.strip() if proxy and proxy.strip() else None
        html_text = ""
        try:
            if PRIMP_AVAILABLE:
                try:
                    client = primp.Client(impersonate="chrome_131", proxy=clean_proxy)
                    resp = client.get(url, headers=headers, timeout=12)
                    if resp.status_code == 200:
                        html_text = resp.text
                    else:
                        self.last_error = f"Bing respondió con estado HTTP {resp.status_code}"
                except Exception as ex:
                    html_text = ""
                    if clean_proxy:
                        self.last_error = f"Error conectando vía proxy en Bing: {ex}"

            if not html_text:
                resp = requests.get(url, headers=headers, proxies=format_requests_proxies(clean_proxy), timeout=12)
                if resp.status_code == 200:
                    html_text = resp.text
                else:
                    self.last_error = f"Bing respondió con estado HTTP {resp.status_code}"

            if html_text:
                soup = BeautifulSoup(html_text, "html.parser")
                for li in soup.select("li.b_algo h2 a[href]"):
                    if stop_check and stop_check():
                        break
                    href = li.get("href", "")
                    target = ""
                    # Bing redirige a través de /ck/a?!...&u=a1<base64>
                    if "/ck/a?" in href and "u=a1" in href:
                        m = re.search(r"u=a1([a-zA-Z0-9_\-]+)", href)
                        if m:
                            b64 = m.group(1).replace("-", "+").replace("_", "/")
                            b64 += "=" * ((4 - len(b64) % 4) % 4)
                            try:
                                decoded = base64.b64decode(b64).decode("utf-8", errors="ignore")
                                if decoded.startswith("http"):
                                    target = decoded
                            except Exception:
                                pass
                    elif href.startswith("http") and "bing.com" not in href and "microsoft.com" not in href:
                        target = href

                    if target and target not in results:
                        results.append(target)
                        if len(results) >= max_results:
                            break
        except Exception as e:
            self.last_error = f"Error en Bing: {str(e)}"

        return results[:max_results]

class YahooEngine(SearchEngineBase):
    name = "Yahoo"

    def search(
        self,
        query: str,
        max_results: int = 10,
        pause: float = 0.0,
        stop_check: Optional[Callable[[], bool]] = None,
        proxy: Optional[str] = None,
    ) -> List[str]:
        self.last_error = None
        results: List[str] = []
        encoded_query = urllib.parse.quote_plus(query)
        num_query = max(int(max_results), 10)
        url = f"https://search.yahoo.com/search?p={encoded_query}&n={num_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        }
        clean_proxy = proxy.strip() if proxy and proxy.strip() else None
        html_text = ""
        try:
            if PRIMP_AVAILABLE:
                try:
                    client = primp.Client(impersonate="chrome_131", proxy=clean_proxy)
                    resp = client.get(url, headers=headers, timeout=12)
                    if resp.status_code == 200:
                        html_text = resp.text
                    else:
                        self.last_error = f"Yahoo respondió con estado HTTP {resp.status_code}"
                except Exception as ex:
                    html_text = ""
                    if clean_proxy:
                        self.last_error = f"Error conectando vía proxy en Yahoo: {ex}"

            if not html_text:
                resp = requests.get(url, headers=headers, proxies=format_requests_proxies(clean_proxy), timeout=12)
                if resp.status_code == 200:
                    html_text = resp.text
                else:
                    self.last_error = f"Yahoo respondió con estado HTTP {resp.status_code}"

            if html_text:
                soup = BeautifulSoup(html_text, "html.parser")
                v1_matches = soup.find_all("div", class_="compTitle options-toggle")
                for div in v1_matches:
                    if stop_check and stop_check():
                        break
                    a = div.find("a")
                    if a and a.get("href"):
                        href = a["href"]
                        if href.startswith("http") and "yahoo.com" not in href and href not in results:
                            results.append(href)

                if len(results) < max_results:
                    for a in soup.find_all("a", href=True):
                        if stop_check and stop_check():
                            break
                        raw_href = a["href"]
                        if "r.search.yahoo.com" in raw_href and "/RU=" in raw_href:
                            match = re.search(r"/RU=(http[^/]+.*?)/RK=", raw_href)
                            if match:
                                decoded = urllib.parse.unquote(match.group(1))
                                if decoded.startswith("http") and "yahoo.com" not in decoded and decoded not in results:
                                    results.append(decoded)
                                    if len(results) >= max_results:
                                        break
        except Exception as e:
            self.last_error = f"Error en Yahoo: {str(e)}"

        return results[:max_results]

class DuckDuckGoEngine(SearchEngineBase):
    name = "DuckDuckGo"

    def search(
        self,
        query: str,
        max_results: int = 10,
        pause: float = 0.0,
        stop_check: Optional[Callable[[], bool]] = None,
        proxy: Optional[str] = None,
    ) -> List[str]:
        self.last_error = None
        results: List[str] = []
        clean_proxy = proxy.strip() if proxy and proxy.strip() else None

        try:
            from duckduckgo_search import DDGS
            with DDGS(proxy=clean_proxy) as ddgs:
                raw_results = ddgs.text(query, max_results=max_results)
                for item in raw_results:
                    if stop_check and stop_check():
                        break
                    if isinstance(item, dict) and "href" in item:
                        href = item["href"]
                        if href and href not in results:
                            results.append(href)
                            if len(results) >= max_results:
                                return results
            if results:
                return results
        except Exception as e:
            err_str = str(e)
            if "202" in err_str or "Ratelimit" in err_str:
                self.last_error = "DuckDuckGo devolvió HTTP 202 (Límite temporal anti-bot)."
            else:
                self.last_error = f"DuckDuckGo error: {err_str}"

        if len(results) < max_results and PRIMP_AVAILABLE:
            try:
                client = primp.Client(impersonate="chrome_131", proxy=clean_proxy)
                encoded = urllib.parse.quote_plus(query)
                resp = client.get(f"https://html.duckduckgo.com/html/?q={encoded}", timeout=10)
                if resp.status_code == 200:
                    self.last_error = None
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for a in soup.find_all("a", href=True):
                        if stop_check and stop_check():
                            break
                        h = a["href"]
                        if "uddg=" in h:
                            target = urllib.parse.unquote(h.split("uddg=")[1].split("&")[0])
                            if target.startswith("http") and "duckduckgo.com" not in target and target not in results:
                                results.append(target)
                                if len(results) >= max_results:
                                    break
                elif resp.status_code == 202:
                    self.last_error = "DuckDuckGo devolvió HTTP 202 (Límite temporal anti-bot)."
            except Exception:
                pass

        return results[:max_results]

class GoogleRequestsEngine(SearchEngineBase):
    name = "Google-Python-Requests"

    def search(
        self,
        query: str,
        max_results: int = 10,
        pause: float = 0.0,
        stop_check: Optional[Callable[[], bool]] = None,
        proxy: Optional[str] = None,
    ) -> List[str]:
        self.last_error = None
        results: List[str] = []
        encoded_query = urllib.parse.quote_plus(query)
        num_query = max(int(max_results), 10)
        url = f"https://www.google.com/search?q={encoded_query}&num={num_query}&hl=es"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
        }
        clean_proxy = proxy.strip() if proxy and proxy.strip() else None
        html_text = ""
        try:
            if PRIMP_AVAILABLE:
                try:
                    client = primp.Client(impersonate="chrome_131", proxy=clean_proxy)
                    resp = client.get(url, headers=headers, timeout=12)
                    status_code = resp.status_code
                    if status_code == 200:
                        html_text = resp.text
                    elif status_code == 429:
                        self.last_error = "Google devolvió HTTP 429 (Bloqueo anti-bot / límite temporal)."
                except Exception as ex:
                    html_text = ""
                    if clean_proxy:
                        self.last_error = f"Error conectando vía proxy en Google: {ex}"

            if not html_text and not self.last_error:
                resp = requests.get(url, headers=headers, proxies=format_requests_proxies(clean_proxy), timeout=12)
                status_code = resp.status_code
                if status_code == 200:
                    html_text = resp.text
                elif status_code == 429:
                    self.last_error = "Google devolvió HTTP 429 (Bloqueo anti-bot / límite temporal)."

            if html_text:
                soup = BeautifulSoup(html_text, "html.parser")
                for part in html_text.split('<a href="/url?q='):
                    if stop_check and stop_check():
                        break
                    candidate = part.split("&amp;sa=")[0].split("&sa=")[0]
                    if candidate.startswith("http") and not any(x in candidate for x in ["google.com", "accounts.google"]):
                        candidate = urllib.parse.unquote(candidate)
                        if candidate not in results:
                            results.append(candidate)
                            if len(results) >= max_results:
                                return results

                for a in soup.select("div.yuRUbf a[href], div.MjjYud a[href]"):
                    if stop_check and stop_check():
                        break
                    href = a.get("href", "")
                    if href.startswith("http") and not any(x in href for x in ["google.com", "gstatic.com", "schema.org"]):
                        if href not in results:
                            results.append(href)
                            if len(results) >= max_results:
                                break

                if len(results) < max_results:
                    for a in soup.find_all("a", href=True):
                        if stop_check and stop_check():
                            break
                        href = a["href"]
                        if href.startswith("/url?q="):
                            target = href.split("/url?q=")[1].split("&sa=")[0]
                            target = urllib.parse.unquote(target)
                            if target.startswith("http") and not any(x in target for x in ["google.com", "accounts.google"]):
                                if target not in results:
                                    results.append(target)
                        elif href.startswith("http") and not any(x in href for x in ["google.com", "gstatic.com", "schema.org"]):
                            if href not in results:
                                results.append(href)
                        if len(results) >= max_results:
                            break
        except Exception as e:
            self.last_error = f"Error en Google-Python-Requests: {str(e)}"

        return results[:max_results]

class GooglePythonEngine(SearchEngineBase):
    name = "Google-Python"

    def search(
        self,
        query: str,
        max_results: int = 10,
        pause: float = 0.0,
        stop_check: Optional[Callable[[], bool]] = None,
        proxy: Optional[str] = None,
    ) -> List[str]:
        self.last_error = None
        results: List[str] = []
        clean_proxy = proxy.strip() if proxy and proxy.strip() else None

        if clean_proxy:
            proxy_handler = urllib.request.ProxyHandler({"http": clean_proxy, "https": clean_proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)

        try:
            import googlesearch
            if hasattr(googlesearch, "cookie_jar"):
                try:
                    googlesearch.cookie_jar.clear()
                except Exception:
                    pass

            tld = random.choice(DEFAULT_TLDS)
            ua = random.choice(USER_AGENTS)
            generator = googlesearch.search(
                query,
                tld=tld,
                num=int(max_results),
                stop=int(max_results),
                pause=float(pause) if pause > 0 else 1.0,
                user_agent=ua,
            )
            for url in generator:
                if stop_check and stop_check():
                    break
                if url and isinstance(url, str):
                    results.append(url)
                    if len(results) >= max_results:
                        break
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "Too Many Requests" in err_str:
                self.last_error = "Google devolvió HTTP 429 (Bloqueo anti-bot / límite temporal)."
            else:
                self.last_error = f"Google-Python error: {err_str}"
        finally:
            if clean_proxy:
                urllib.request.install_opener(urllib.request.build_opener())

        return results

AVAILABLE_ENGINES: Dict[str, SearchEngineBase] = {
    "Bing": BingEngine(),
    "Yahoo": YahooEngine(),
    "DuckDuckGo": DuckDuckGoEngine(),
    "Google-Python": GooglePythonEngine(),
    "Google-Python-Requests": GoogleRequestsEngine(),
}

__all__ = [
    "DEFAULT_DORK_TEMPLATES",
    "DEFAULT_COMMON_DORKS",
    "DEFAULT_TLDS",
    "USER_AGENTS",
    "format_requests_proxies",
    "get_default_dorks",
    "normalize_url",
    "deduplicate_results",
    "SearchEngineBase",
    "BingEngine",
    "YahooEngine",
    "DuckDuckGoEngine",
    "GooglePythonEngine",
    "GoogleRequestsEngine",
    "AVAILABLE_ENGINES",
]
