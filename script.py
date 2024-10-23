import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_directory_list(url):
    """Scrapes the directory list from the given URL and extracts the title, description, and link."""
    directory_items = []
    existing_titles = set()  # To track already scraped titles

    while True:
        print(f"Scraping: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve data from {url}")
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        directory_elements = soup.find_all('div', class_="e-con-inner")

        if not directory_elements:  # No more items to scrape
            print("No more items found. Ending scraping.")
            break

        new_items_found = False  # Flag to track if new items are found

        for item in directory_elements:
            title_element = item.find('h1', class_='elementor-heading-title elementor-size-default')
            description_element = item.find('p')
            link_element = item.find('a', class_='elementor-button-link')

            if title_element and description_element and link_element:
                title = title_element.text.strip()
                description = description_element.text.strip()
                link = link_element['href']

                if title not in existing_titles:  # Check for new items
                    existing_titles.add(title)  # Add to the set
                    directory_items.append({'title': title, 'description': description, 'link': link})
                    new_items_found = True  # Mark that we found new items
                    print(f"Added: Title: {title}, Description: {description}, Link: {link}")

        if not new_items_found:  # Break if no new items were found
            print("No new items found. Ending scraping.")
            break

        # Simulate scrolling by waiting before the next request
        time.sleep(2)  # Adjust the sleep time as needed

    return directory_items

def save_to_csv(directory_items, filename):
    """Saves the directory items to a CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['title', 'description', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(directory_items)

if __name__ == '__main__':
    url = 'https://growstartup.co/directory-list/'
    directory_items = scrape_directory_list(url)
    save_to_csv(directory_items, 'directory_list.csv')
    print('Data saved to directory_list.csv')
