# Create sitemap_checker.py
import requests
from bs4 import BeautifulSoup


def check_sitemap_directly():
    sites = [
        ("The Daily Star", "https://www.thedailystar.net/sitemap.xml"),
        ("Prothom Alo", "https://www.prothomalo.com/sitemap.xml"),
        ("Dhaka Tribune", "https://www.dhakatribune.com/sitemap.xml"),
        ("Bangla Tribune", "https://www.banglatribune.com/sitemap.xml"),
        ("New Age", "https://www.newagebd.net/sitemap.xml"),
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for site_name, url in sites:
        print(f"\nChecking: {site_name}")
        print(f"URL: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                # Print first 500 chars to see structure
                content = response.content[:1000]
                print(f"First 1000 chars:\n{content.decode('utf-8', errors='ignore')}")

                # Try to parse
                soup = BeautifulSoup(response.content, 'xml')

                # Check what tags exist
                print(f"\nRoot tag: {soup.find().name if soup.find() else 'None'}")

                # Check for sitemapindex or urlset
                if soup.find('sitemapindex'):
                    print("✓ This is a SITEMAP INDEX (contains links to other sitemaps)")
                    sitemaps = soup.find_all('sitemap')
                    print(f"  Contains {len(sitemaps)} child sitemaps")
                    for i, sitemap in enumerate(sitemaps[:3]):
                        loc = sitemap.find('loc')
                        if loc:
                            print(f"  {i + 1}. {loc.text}")

                elif soup.find('urlset'):
                    print("✓ This is a regular URL sitemap")
                    urls = soup.find_all('url')
                    print(f"  Contains {len(urls)} URLs")
                    for i, url_tag in enumerate(urls[:3]):
                        loc = url_tag.find('loc')
                        if loc:
                            print(f"  {i + 1}. {loc.text}")

                else:
                    print("✗ Unknown sitemap format")
                    # Print all tags to understand structure
                    all_tags = set([tag.name for tag in soup.find_all()])
                    print(f"  Found tags: {all_tags}")

            else:
                print(f"✗ Failed with status: {response.status_code}")

        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    check_sitemap_directly()