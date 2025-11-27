"""
Clean Raw Data: Processes raw HTML files into structured JSONL format.
"""

import os
import json
from bs4 import BeautifulSoup
import re

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_metadata(soup, url):
    title = soup.title.string if soup.title else "Untitled"
    
    # Heuristic for page type
    page_type = "page"
    if "winner" in url or "award" in url:
        page_type = "winners"
    elif "jury" in url or "judge" in url:
        page_type = "jury"
    elif "event" in url:
        page_type = "events"
        
    # Extract year if present
    year = None
    year_match = re.search(r'20\d{2}', title)
    if year_match:
        year = int(year_match.group(0))
        
    return {
        "title": clean_text(title),
        "page_type": page_type,
        "year": year
    }

def process_files(input_dir="data/raw", output_file="data/cleaned/clios_clean.jsonl"):
    print("Starting data cleaning...")
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
        
    processed_count = 0
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_dir):
            if not filename.endswith(".html"):
                continue
                
            filepath = os.path.join(input_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                    
                # Get text
                text = soup.get_text()
                cleaned_content = clean_text(text)
                
                if len(cleaned_content) < 100:
                    continue  # Skip empty/short pages
                    
                # Get metadata (try to find corresponding meta json)
                meta_filename = filename.replace("page_", "meta_").replace(".html", ".json")
                meta_path = os.path.join(input_dir, meta_filename)
                
                url = "#"
                if os.path.exists(meta_path):
                    with open(meta_path, 'r', encoding='utf-8') as mf:
                        meta_data = json.load(mf)
                        url = meta_data.get('url', '#')
                
                metadata = extract_metadata(soup, url)
                
                record = {
                    "url": url,
                    "content": cleaned_content,
                    "content_length": len(cleaned_content),
                    **metadata
                }
                
                outfile.write(json.dumps(record) + "\n")
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    print(f"Successfully cleaned {processed_count} documents.")

if __name__ == "__main__":
    process_files()
