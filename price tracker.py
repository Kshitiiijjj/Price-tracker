import requests
from bs4 import BeautifulSoup

class PriceTracer:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        self.soup = self.fetch_page()

    def fetch_page(self):
        try:
            response = requests.get(url=self.url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def product_title(self):
        if not self.soup:
            return "Page not available"

        title_tag = self.soup.find("span", {"id": "productTitle"})
        return title_tag.text.strip() if title_tag else "Title not found"

    def product_price(self):
        if not self.soup:
            return "Page not available"

        price_tag = self.soup.find("span", {"id": "a-price-whole"}) \
                    or self.soup.find("span", {"class": "a-price-whole"}) \
                    or self.soup.find("span", {"id": "priceblock_ourprice"}) \
                    or self.soup.find("span", {"id": "priceblock_dealprice"})

        if price_tag:
            return price_tag.text.strip().replace(",", "")
        else:
            return "Price not found"

if __name__ == "__main__":
    url = "https://www.amazon.in/Yamaha-F280-Acoustic-Guitar-Natural/dp/B08317Y4VP"
    device = PriceTracer(url=url)

    print("Product Title:", device.product_title())
    print("Product Price:", device.product_price())
