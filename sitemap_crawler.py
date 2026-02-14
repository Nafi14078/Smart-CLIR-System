import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


class AdvancedSitemapCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/xml, text/xml, */*",
            "Accept-Language": "en-US,en;q=0.9,bn;q=0.8"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def parse_sitemap_index(self, sitemap_url: str) -> List[str]:
        """Parse sitemap index to get child sitemap URLs"""
        try:
            print(f"  Parsing sitemap index: {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            sitemap_tags = soup.find_all('sitemap')

            child_sitemaps = []
            for sitemap in sitemap_tags:
                loc = sitemap.find('loc')
                if loc and loc.text:
                    child_sitemaps.append(loc.text.strip())

            print(f"    Found {len(child_sitemaps)} child sitemaps")
            return child_sitemaps

        except Exception as e:
            print(f"    Error parsing sitemap index: {e}")
            return []

    def parse_sitemap_urls(self, sitemap_url: str) -> List[Dict]:
        """Parse actual sitemap to get URLs"""
        try:
            response = self.session.get(sitemap_url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            url_tags = soup.find_all('url')

            urls_data = []
            for url_tag in url_tags:
                loc = url_tag.find('loc')
                if loc and loc.text:
                    url_data = {
                        'url': loc.text.strip(),
                        'lastmod': '',
                        'changefreq': '',
                        'priority': ''
                    }

                    lastmod = url_tag.find('lastmod')
                    if lastmod and lastmod.text:
                        url_data['lastmod'] = lastmod.text.strip()

                    changefreq = url_tag.find('changefreq')
                    if changefreq and changefreq.text:
                        url_data['changefreq'] = changefreq.text.strip()

                    priority = url_tag.find('priority')
                    if priority and priority.text:
                        url_data['priority'] = priority.text.strip()

                    urls_data.append(url_data)

            return urls_data

        except Exception as e:
            print(f"    Error parsing sitemap {sitemap_url}: {e}")
            return []

    def get_all_urls_from_sitemap(self, base_sitemap_url: str, max_urls=5000) -> List[Dict]:
        """Get all URLs from sitemap hierarchy"""
        print(f"\n🔍 Getting URLs from sitemap: {base_sitemap_url}")

        # Step 1: Check if it's a sitemap index
        try:
            response = self.session.get(base_sitemap_url, timeout=15)
            soup = BeautifulSoup(response.content, 'xml')

            # Check if it's a sitemap index
            if soup.find('sitemapindex'):
                print("  Detected: Sitemap Index")
                child_sitemaps = self.parse_sitemap_index(base_sitemap_url)

                all_urls = []
                for child_sitemap in child_sitemaps:
                    print(f"  Processing child sitemap: {child_sitemap}")
                    urls = self.parse_sitemap_urls(child_sitemap)
                    all_urls.extend(urls)

                    # Check if we have enough
                    if len(all_urls) >= max_urls:
                        all_urls = all_urls[:max_urls]
                        break

                    time.sleep(0.5)  # Be polite

                return all_urls

            # If it's a regular sitemap
            elif soup.find('urlset'):
                print("  Detected: Regular Sitemap")
                return self.parse_sitemap_urls(base_sitemap_url)[:max_urls]

            else:
                print("  Unknown sitemap format")
                return []

        except Exception as e:
            print(f"  Error: {e}")
            return []

    def filter_article_urls(self, urls_data: List[Dict], site_config: Dict) -> List[Dict]:
        """Filter URLs to get only article pages"""
        filtered = []

        for url_data in urls_data:
            url = url_data['url'].lower()

            # Skip non-HTML pages
            if any(ext in url for ext in ['.jpg', '.png', '.gif', '.pdf', '.mp4', '.zip', '.css', '.js']):
                continue

            # Skip admin/login/author pages
            if any(pattern in url for pattern in
                   ['/author/', '/user/', '/admin/', '/login', '/register', '/wp-admin', '/feed', '/rss']):
                continue

            # Site-specific filtering
            site_name = site_config['name']

            if 'daily star' in site_name.lower():
                # Daily Star patterns
                if any(pattern in url for pattern in
                       ['/news/', '/sports/', '/entertainment/', '/business/', '/opinion/']):
                    if not any(pattern in url for pattern in ['/category/', '/tag/']):
                        filtered.append(url_data)

            elif 'prothom alo' in site_name.lower():
                # Prothom Alo patterns
                if '/article/' in url or any(
                        pattern in url for pattern in ['/sports/', '/entertainment/', '/opinion/', '/politics/']):
                    filtered.append(url_data)

            elif 'dhaka tribune' in site_name.lower():
                # Dhaka Tribune patterns
                if '/article/' in url or any(
                        pattern in url for pattern in ['/news/', '/sports/', '/business/', '/opinion/']):
                    filtered.append(url_data)

            elif 'bangla tribune' in site_name.lower():
                # Bangla Tribune patterns
                if any(pattern in url for pattern in ['/news/', '/article/', '/sports/', '/entertainment/']):
                    filtered.append(url_data)

            elif 'new age' in site_name.lower():
                # New Age patterns
                if '/article/' in url or any(pattern in url for pattern in ['/news/', '/sports/', '/entertainment/']):
                    filtered.append(url_data)

            else:
                # Generic filtering
                if any(pattern in url for pattern in ['/article/', '/news/', '/story/', '/post/', '/blog/']):
                    filtered.append(url_data)

        return filtered


# Site-specific configurations
SITE_CONFIGS = {
    'english': [
        {
            'name': 'The Daily Star',
            'base_url': 'https://www.thedailystar.net',
            'sitemap_url': 'https://www.thedailystar.net/sitemap.xml',
            'language': 'en',
            'output_file': 'data/raw/english/dailystar_sitemap.json',
            'max_articles': 1500,
            'description': 'Leading English newspaper in Bangladesh'
        },
        {
            'name': 'Dhaka Tribune',
            'base_url': 'https://www.dhakatribune.com',
            'sitemap_url': 'https://www.dhakatribune.com/sitemap.xml',
            'language': 'en',
            'output_file': 'data/raw/english/dhakatribune_sitemap.json',
            'max_articles': 1200,
            'description': 'English daily newspaper'
        },
        {
            'name': 'New Age',
            'base_url': 'https://www.newagebd.net',
            'sitemap_url': 'https://www.newagebd.net/sitemap.xml',
            'language': 'en',
            'output_file': 'data/raw/english/newage_sitemap.json',
            'max_articles': 1000,
            'description': 'English newspaper'
        },
        {
            'name': 'Daily Sun',
            'base_url': 'https://www.daily-sun.com',
            'sitemap_url': 'https://www.daily-sun.com/sitemap.xml',  # May not exist
            'language': 'en',
            'output_file': 'data/raw/english/dailysun_sitemap.json',
            'max_articles': 800,
            'description': 'English tabloid'
        },
        {
            'name': 'The New Nation',
            'base_url': 'https://www.dailynewnation.com',
            'sitemap_url': 'https://www.dailynewnation.com/sitemap.xml',  # May not exist
            'language': 'en',
            'output_file': 'data/raw/english/newnation_sitemap.json',
            'max_articles': 700,
            'description': 'English newspaper'
        }
    ],
    'bangla': [
        {
            'name': 'Prothom Alo',
            'base_url': 'https://www.prothomalo.com',
            'sitemap_url': 'https://www.prothomalo.com/sitemap.xml',
            'language': 'bn',
            'output_file': 'data/raw/bangla/prothomalo_sitemap.json',
            'max_articles': 1500,
            'description': 'Largest circulated Bangla newspaper'
        },
        {
            'name': 'Bangla Tribune',
            'base_url': 'https://www.banglatribune.com',
            'sitemap_url': 'https://www.banglatribune.com/sitemap.xml',
            'language': 'bn',
            'output_file': 'data/raw/bangla/banglatribune_sitemap.json',
            'max_articles': 1200,
            'description': 'Bangla online newspaper'
        },
        {
            'name': 'BD News 24',
            'base_url': 'https://bangla.bdnews24.com',
            'sitemap_url': 'https://bangla.bdnews24.com/sitemap.xml',  # May not exist
            'language': 'bn',
            'output_file': 'data/raw/bangla/bdnews24_sitemap.json',
            'max_articles': 1000,
            'description': 'Bangla news portal'
        },
        {
            'name': 'Kaler Kantho',
            'base_url': 'https://www.kalerkantho.com',
            'sitemap_url': 'https://www.kalerkantho.com/sitemap.xml',  # May not exist
            'language': 'bn',
            'output_file': 'data/raw/bangla/kalerkantho_sitemap.json',
            'max_articles': 800,
            'description': 'Bangla newspaper'
        },
        {
            'name': 'Dhaka Post',
            'base_url': 'https://www.dhakapost.com',
            'sitemap_url': 'https://www.dhakapost.com/sitemap.xml',  # May not exist
            'language': 'bn',
            'output_file': 'data/raw/bangla/dhakapost_sitemap.json',
            'max_articles': 700,
            'description': 'Bangla news portal'
        }
    ]
}


def extract_article_content(soup, url, language):
    """Extract article content from page"""
    try:
        # Title
        title = ""

        # Try meta tags first
        meta_title = soup.find('meta', property='og:title') or soup.find('meta', attrs={'name': 'title'})
        if meta_title and meta_title.get('content'):
            title = meta_title.get('content').strip()

        # Try h1 tags
        if not title:
            h1_tags = soup.find_all('h1')
            for h1 in h1_tags:
                h1_text = h1.get_text().strip()
                if h1_text and len(h1_text) > 10:
                    title = h1_text
                    break

        # Try title tag as last resort
        if not title and soup.title:
            title = soup.title.get_text().strip()

        if not title:
            return None

        # Content - try multiple selectors
        content_selectors = [
            'article', 'div.story-content', 'div.article-body', '.entry-content',
            'main', 'div[class*="content"]', 'div[class*="story"]', '.details'
        ]

        content_text = ""
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                # Get paragraphs
                paragraphs = content_div.find_all(['p', 'h2', 'h3'])
                text_parts = []
                for p in paragraphs:
                    text = p.get_text().strip()
                    if text and len(text) > 20:
                        text_parts.append(text)

                if text_parts:
                    content_text = "\n\n".join(text_parts)
                    break

        # If still no content, try to get main text
        if not content_text:
            main_content = soup.find('main') or soup.find('article')
            if main_content:
                content_text = main_content.get_text().strip()

        if not content_text:
            return None

        # Date
        date = ""
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="publish_date"]',
            'time',
            '.publish-date',
            '.date',
            '.article-date'
        ]

        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                if date_elem.get('content'):
                    date = date_elem.get('content')
                elif date_elem.get('datetime'):
                    date = date_elem.get('datetime')
                else:
                    date = date_elem.get_text().strip()
                if date:
                    break

        # Clean text
        title = re.sub(r'\s+', ' ', title).strip()
        content_text = re.sub(r'\s+', ' ', content_text).strip()

        # Token count
        if language == 'en':
            token_count = len(content_text.split())
            if token_count < 100:
                return None
        else:
            token_count = len(content_text)
            if token_count < 300:
                return None

        return {
            'title': title,
            'body': content_text,
            'url': url,
            'date': date,
            'language': language,
            'token_count': token_count
        }

    except Exception as e:
        print(f"    Extraction error: {e}")
        return None


def crawl_site(site_config, crawler):
    """Crawl a single site using sitemap"""
    print(f"\n{'=' * 70}")
    print(f"SITE: {site_config['name']}")
    print(f"Language: {site_config['language'].upper()}")
    print(f"{'=' * 70}")

    # Get URLs from sitemap
    print("\nStep 1: Getting URLs from sitemap...")
    all_urls = crawler.get_all_urls_from_sitemap(
        site_config['sitemap_url'],
        max_urls=site_config['max_articles'] * 2  # Get extra for filtering
    )

    print(f"  Total URLs found: {len(all_urls)}")

    # Filter for articles
    print("\nStep 2: Filtering for article URLs...")
    article_urls = crawler.filter_article_urls(all_urls, site_config)
    print(f"  Article URLs after filtering: {len(article_urls)}")

    # Limit to max articles
    article_urls = article_urls[:site_config['max_articles']]
    print(f"  Will crawl: {len(article_urls)} articles")

    # Crawl articles
    print(f"\nStep 3: Crawling articles...")
    articles = []

    for idx, url_data in enumerate(article_urls):
        try:
            if idx % 50 == 0:
                print(f"  Progress: {idx}/{len(article_urls)}")

            url = url_data['url']
            print(f"    [{idx + 1}] {url[:80]}...")

            response = crawler.session.get(url, timeout=20)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.content, 'html.parser')

            article = extract_article_content(soup, url, site_config['language'])

            if article:
                article[
                    'doc_id'] = f"{site_config['language']}_{site_config['name'].lower().replace(' ', '_')}_{idx:06d}"
                article['site'] = site_config['name']
                article['lastmod'] = url_data.get('lastmod', '')
                articles.append(article)

                print(f"      ✓ {article['title'][:50]}...")
                print(f"      ✓ Tokens: {article['token_count']}")

            # Save progress every 50 articles
            if len(articles) > 0 and len(articles) % 50 == 0:
                with open(site_config['output_file'], 'w', encoding='utf-8') as f:
                    json.dump(articles, f, ensure_ascii=False, indent=2)
                print(f"      💾 Saved {len(articles)} articles")

            time.sleep(0.3)  # Polite delay

        except Exception as e:
            print(f"      ✗ Error: {e}")
            time.sleep(1)

    # Final save
    with open(site_config['output_file'], 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {site_config['name']}: {len(articles)} articles saved")
    return len(articles)


def main():
    """Main function to crawl all sites"""
    print("=" * 80)
    print("ADVANCED SITEMAP CRAWLER FOR CLIR SYSTEM")
    print("=" * 80)

    # Create directories
    os.makedirs('data/raw/english', exist_ok=True)
    os.makedirs('data/raw/bangla', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/utils', exist_ok=True)

    crawler = AdvancedSitemapCrawler()

    # Ask user what to crawl
    print("\nChoose option:")
    print("1. Crawl ALL sites")
    print("2. Crawl only ENGLISH sites")
    print("3. Crawl only BANGLA sites")
    print("4. Crawl specific site")

    try:
        choice = int(input("\nEnter choice (1-4): "))
    except:
        choice = 1

    total_articles = 0
    start_time = time.time()

    if choice == 1:
        # Crawl all
        for site_config in SITE_CONFIGS['english']:
            count = crawl_site(site_config, crawler)
            total_articles += count
            time.sleep(5)

        for site_config in SITE_CONFIGS['bangla']:
            count = crawl_site(site_config, crawler)
            total_articles += count
            time.sleep(5)

    elif choice == 2:
        # English only
        for site_config in SITE_CONFIGS['english']:
            count = crawl_site(site_config, crawler)
            total_articles += count
            time.sleep(5)

    elif choice == 3:
        # Bangla only
        for site_config in SITE_CONFIGS['bangla']:
            count = crawl_site(site_config, crawler)
            total_articles += count
            time.sleep(5)

    elif choice == 4:
        # Specific site
        print("\nAvailable sites:")
        for i, site in enumerate(SITE_CONFIGS['english'] + SITE_CONFIGS['bangla']):
            print(f"{i + 1}. {site['name']} ({site['language']})")

        try:
            site_num = int(input("\nEnter site number: ")) - 1
            all_sites = SITE_CONFIGS['english'] + SITE_CONFIGS['bangla']
            if 0 <= site_num < len(all_sites):
                count = crawl_site(all_sites[site_num], crawler)
                total_articles = count
        except:
            print("Invalid choice")

    # Merge data
    print("\n" + "=" * 80)
    print("MERGING DATA")
    print("=" * 80)

    # Merge English
    english_articles = []
    for site_config in SITE_CONFIGS['english']:
        if os.path.exists(site_config['output_file']):
            with open(site_config['output_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                english_articles.extend(data)
                print(f"✓ {site_config['name']}: {len(data)} articles")

    # Merge Bangla
    bangla_articles = []
    for site_config in SITE_CONFIGS['bangla']:
        if os.path.exists(site_config['output_file']):
            with open(site_config['output_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                bangla_articles.extend(data)
                print(f"✓ {site_config['name']}: {len(data)} articles")

    # Remove duplicates
    def remove_duplicates(articles):
        seen_urls = set()
        unique = []
        for article in articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique.append(article)
        return unique

    english_articles = remove_duplicates(english_articles)
    bangla_articles = remove_duplicates(bangla_articles)

    # Save merged files
    with open('data/processed/english_docs.json', 'w', encoding='utf-8') as f:
        json.dump(english_articles, f, ensure_ascii=False, indent=2)

    with open('data/processed/bangla_docs.json', 'w', encoding='utf-8') as f:
        json.dump(bangla_articles, f, ensure_ascii=False, indent=2)

    end_time = time.time()
    duration = (end_time - start_time) / 60  # minutes

    print(f"\n📊 FINAL RESULTS:")
    print(f"   English articles: {len(english_articles)}")
    print(f"   Bangla articles:  {len(bangla_articles)}")
    print(f"   Total: {len(english_articles) + len(bangla_articles)}")

    print(f"\n⏱️  Time taken: {duration:.1f} minutes")

    print(f"\n🎯 REQUIREMENTS (2,500 per language):")
    print(f"   English: {len(english_articles)}/2,500 ({(len(english_articles) / 2500 * 100):.1f}%)")
    print(f"   Bangla:  {len(bangla_articles)}/2,500 ({(len(bangla_articles) / 2500 * 100):.1f}%)")

    if len(english_articles) >= 2500 and len(bangla_articles) >= 2500:
        print("\n✅ SUCCESS! Requirements met!")
    else:
        print("\n⚠️  Need more articles. Consider:")
        print("   - Running crawler again with more URLs")
        print("   - Adding more sites")
        print("   - Using RSS feeds as supplement")

    print(f"\n📁 Files saved:")
    print(f"   English: data/processed/english_docs.json")
    print(f"   Bangla:  data/processed/bangla_docs.json")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()