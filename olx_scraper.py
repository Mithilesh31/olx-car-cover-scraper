import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import random

def scrape_olx_car_covers(output_file='olx_car_covers.csv', max_pages=5):
    """
    Scrapes OLX.in for car cover listings and saves results to a CSV file.
    """
    base_url = "https://www.olx.in/items/q-car-cover"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_listings = []
    
    try:
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}...")
            url = f"{base_url}?page={page}" if page > 1 else base_url
            
            time.sleep(random.uniform(1, 3))  # Avoid blocking
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all('li', {'class': '_1DNjI'})
            
            if not listings:
                print("No more listings found.")
                break
                
            for listing in listings:
                title = listing.find('span', {'class': '_2poNJ'}).text.strip()
                price = listing.find('span', {'class': '_2Ks63'}).text.strip() if listing.find('span', {'class': '_2Ks63'}) else 'Price not listed'
                location = listing.find('span', {'class': '_2VQu4'}).text.strip() if listing.find('span', {'class': '_2VQu4'}) else 'Location not listed'
                link = listing.find('a')['href'] if listing.find('a') else 'No link'
                if not link.startswith('http'):
                    link = f"https://www.olx.in{link}"
                
                all_listings.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Save to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'price', 'location', 'link', 'scraped_at'])
            writer.writeheader()
            writer.writerows(all_listings)
            
        print(f"Successfully scraped {len(all_listings)} listings. Saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_olx_car_covers()
