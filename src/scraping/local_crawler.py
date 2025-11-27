"""
Local Crawler: Crawls the Clio Awards website to gather data.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

class ClioCrawler:
    def __init__(self, base_url="https://clios.com", output_dir="data/raw"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited = set()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.netloc == urlparse(self.base_url).netloc
        
    def crawl(self, start_url, max_pages=50):
        queue = [start_url]
        count = 0
        
        print(f"Starting crawl from {start_url}...")
        
        while queue and count < max_pages:
            url = queue.pop(0)
            if url in self.visited:
                continue
                
            try:
                print(f"Crawling: {url}")
                response = requests.get(url, headers=self.headers)
                if response.status_code != 200:
                    print(f"Failed to fetch {url}: {response.status_code}")
                    continue
                    
                self.visited.add(url)
                
                # Save HTML
                filename = f"page_{count}.html"
                with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(response.text)
                    
                # Save Metadata
                meta = {
                    'url': url,
                    'filename': filename,
                    'timestamp': time.time()
                }
                with open(os.path.join(self.output_dir, f"meta_{count}.json"), 'w', encoding='utf-8') as f:
                    json.dump(meta, f, indent=2)
                
                count += 1
                
                # Extract links
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    if self.is_valid_url(next_url) and next_url not in self.visited:
                        queue.append(next_url)
                        
                time.sleep(1)  # Polite delay
                
            except Exception as e:
                print(f"Error crawling {url}: {e}")
                
        print("Crawl completed successfully.")

if __name__ == "__main__":
    crawler = ClioCrawler()
    crawler.crawl("https://clios.com/awards/winners")
