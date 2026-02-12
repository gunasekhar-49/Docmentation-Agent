"""
Sample code to demonstrate docstring generation.
"""


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0


class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def clean_data(self):
        return [x for x in self.data if x is not None]
    
    def normalize(self, min_val=0, max_val=1):
        cleaned = self.clean_data()
        if not cleaned:
            return []
        current_min = min(cleaned)
        current_max = max(cleaned)
        range_val = current_max - current_min
        if range_val == 0:
            return [min_val] * len(cleaned)
        return [(x - current_min) / range_val * (max_val - min_val) + min_val for x in cleaned]


async def fetch_data(url):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


class APIClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
    
    def make_request(self, endpoint, method='GET', params=None):
        import requests
        url = f"{self.base_url}/{endpoint}"
        return requests.request(method, url, params=params, timeout=self.timeout)
    
    async def async_request(self, endpoint, method='GET'):
        url = f"{self.base_url}/{endpoint}"
        return await fetch_data(url)
