from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

app = Flask(__name__)

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
                items_found.append({
                    'Title': f"Failed to retrieve data for keyword: {keyword} in {location}",
                    'Date': '',
                    'Link': '',
                    'Price': '',
                    'Location': location
                })
            time.sleep(1)
    return pd.DataFrame(items_found)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        locations = request.form['locations'].split(',')
        keywords = request.form['keywords'].split(',')
        results_df = search_craigslist(locations, keywords)
        return render_template('index.html', tables=[results_df.to_html(classes='data', header="true")])
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
