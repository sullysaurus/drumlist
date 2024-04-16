import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def search_craigslist(locations, keywords):
    items_found = []
    for location in locations:
        base_url = f"https://{location}.craigslist.org/search/msa"
        for keyword in keywords:
            params = {'query': keyword, 'sort': 'rel'}
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                postings = soup.find_all('li', class_='result-row')
                for post in postings:
                    title = post.find('a', class_='result-title').text
                    date = post.find('time', class_='result-date')['datetime']
                    link = post.find('a', class_='result-title')['href']
                    price_tag = post.find('span', class_='result-price')
                    price = price_tag.text if price_tag else 'N/A'
                    items_found.append({
                        'Title': title,
                        'Date': date,
                        'Link': link,
                        'Price': price,
                        'Location': location
                    })
            else:
                st.error(f"Failed to retrieve data for keyword: {keyword} in {location}")
            time.sleep(1)
    return pd.DataFrame(items_found)

st.title('Craigslist Musical Instrument Scraper')

# User inputs
location_input = st.text_input('Enter locations (comma-separated, e.g., newyork, losangeles):')
keyword_input = st.text_input('Enter keywords (comma-separated, e.g., Ludwig, Guitar):')

# Button to start scraping
if st.button('Scrape Craigslist'):
    if location_input and keyword_input:
        locations = location_input.split(',')
        keywords = keyword_input.split(',')
        results_df = search_craigslist(locations, keywords)
        st.dataframe(results_df)
    else:
        st.warning('Please enter both locations and keywords to proceed.')

