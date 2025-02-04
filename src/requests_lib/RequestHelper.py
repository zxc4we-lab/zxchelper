import requests
import json
from typing import Dict, Optional, List, Union
from http.cookiejar import MozillaCookieJar, CookieJar

class RequestManager:
    def __init__(self, default_headers: Optional[Dict[str, str]] = None, proxies: Optional[List[str]] = None, max_requests_per_proxy: int = 10):
        self.default_headers = default_headers if default_headers else {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept": "*/*",
        "Pragma": "no-cache"
    }
        self.proxies = proxies if proxies else []
        self.max_requests_per_proxy = max_requests_per_proxy
        self.current_proxy_index = 0
        self.request_count = 0
        self.cookie_jar = CookieJar()  # Initialize a cookie jar to store cookies

    def parse_proxy(self, proxy_str: str) -> Dict[str, str]:
        """
        Parse a proxy string in the format `proxy:port:user:pass`.
        Returns a dictionary with `http` and `https` proxy URLs.
        """
        if not proxy_str:
            return None
        parts = proxy_str.split(":")
        if len(parts) == 4:
            proxy, port, user, password = parts
            proxy_url = f"http://{user}:{password}@{proxy}:{port}"
            return {
                "http": proxy_url,
                "https": proxy_url,
            }
        elif len(parts) == 2:
            proxy, port = parts
            proxy_url = f"http://{proxy}:{port}"
            return {
                "http": proxy_url,
                "https": proxy_url,
            }
        else:
            raise ValueError("Invalid proxy format. Use 'proxy:port' or 'proxy:port:user:pass'.")

    def get_current_proxy(self) -> Optional[Dict[str, str]]:
        if not self.proxies:
            return None
        proxy_str = self.proxies[self.current_proxy_index]
        return self.parse_proxy(proxy_str)

    def rotate_proxy(self):
        if not self.proxies:
            return
        self.request_count += 1
        if self.request_count >= self.max_requests_per_proxy:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            self.request_count = 0

    def request(self, method: str, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None, json: Optional[Dict[str, str]] = None) -> requests.Response:
        headers = {**self.default_headers, **(headers if headers else {})}
        proxy = self.get_current_proxy()

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            json=json,
            proxies=proxy,
            cookies=self.cookie_jar,  # Use the cookie jar for the request
        )

        # Update the cookie jar with cookies from the response
        self.cookie_jar.update(response.cookies)
        self.rotate_proxy()
        return response

    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("GET", url, headers=headers)

    def post(self, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None, json: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("POST", url, headers=headers, data=data, json=json)

    def put(self, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None, json: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("PUT", url, headers=headers, data=data, json=json)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("DELETE", url, headers=headers)

    def add_cookie(self, name: str, value: str, domain: str, path: str = "/") -> None:
        """Add a cookie to the cookie jar."""
        from http.cookiejar import Cookie
        cookie = Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=True,
            domain_initial_dot=False,
            path=path,
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None,
        )
        self.cookie_jar.set_cookie(cookie)

    def get_cookies(self) -> Dict[str, str]:
        """Get all cookies as a dictionary."""
        return {cookie.name: cookie.value for cookie in self.cookie_jar}

    def import_cookies_from_json(self, file_path: str) -> None:
        """Import cookies from a JSON file."""
        with open(file_path, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.add_cookie(cookie["name"], cookie["value"], cookie["domain"], cookie.get("path", "/"))

    def export_cookies_to_json(self, file_path: str) -> None:
        """Export cookies to a JSON file."""
        cookies = [
            {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
            }
            for cookie in self.cookie_jar
        ]
        with open(file_path, "w") as f:
            json.dump(cookies, f, indent=4)

    def import_cookies_from_netscape(self, file_path: str) -> None:
        """Import cookies from a Netscape format file."""
        mozilla_cookie_jar = MozillaCookieJar(file_path)
        mozilla_cookie_jar.load()
        for cookie in mozilla_cookie_jar:
            self.cookie_jar.set_cookie(cookie)

    def export_cookies_to_netscape(self, file_path: str) -> None:
        """Export cookies to a Netscape format file."""
        mozilla_cookie_jar = MozillaCookieJar(file_path)
        for cookie in self.cookie_jar:
            mozilla_cookie_jar.set_cookie(cookie)
        mozilla_cookie_jar.save(ignore_discard=True, ignore_expires=True)

    # Header management methods
    def add_header(self, key: str, value: str) -> None:
        """Add or update a header in the default headers."""
        self.default_headers[key] = value

    def remove_header(self, key: str) -> None:
        """Remove a header from the default headers."""
        if key in self.default_headers:
            del self.default_headers[key]

    def clear_headers(self) -> None:
        """Clear all default headers."""
        self.default_headers.clear()

    def get_headers(self) -> Dict[str, str]:
        """Get the current default headers."""
        return self.default_headers

# Example usage:
if __name__ == "__main__":
    default_headers = {
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
    }

    # Proxies in the format "proxy:port:user:pass" or "proxy:port"
    proxies = [
        "proxy1.example.com:8080:user1:pass1",
        "proxy2.example.com:8080:user2:pass2",
        "proxy3.example.com:8080",  # Proxy without authentication
    ]

    manager = RequestManager(default_headers=default_headers, proxies=proxies, max_requests_per_proxy=5)

    # Add a header
    manager.add_header("Authorization", "Bearer token123")
    print("Headers after adding Authorization:", manager.get_headers())

    # Remove a header
    manager.remove_header("Accept")
    print("Headers after removing Accept:", manager.get_headers())

    # Clear all headers
    manager.clear_headers()
    print("Headers after clearing:", manager.get_headers())

    # Add a cookie
    manager.add_cookie("session_id", "12345", "example.com")

    # Get cookies
    print("Cookies:", manager.get_cookies())

    # GET request with cookies and proxy
    response = manager.get("https://example.com")
    print(response.status_code, response.text)