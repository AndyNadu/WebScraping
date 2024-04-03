import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time

start_time = time.time()

url = "https://www.tiriacauto.ro/auto-rulate"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#titles = [title.text.strip() for title in soup.find_all('div', class_='title')]
#prices_raw = [price.text for price in soup.find_all('b', class_='orangeText')]

titles = [title.text.strip() for title in soup.find_all('div', class_='title')][:10]
prices_raw = [price.text for price in soup.find_all('b', class_='orangeText')][:10]

cleaned_prices = []
for price_tag in prices_raw:
    price_str = price_tag;
    cleaned_price = re.sub(r'[^\d.]', '', price_str)
    price = float(cleaned_price)
    cleaned_prices.append(price * 1000)

max_price_index = cleaned_prices.index(max(cleaned_prices))
max_price_title = titles[max_price_index]
max_price = cleaned_prices[max_price_index]

min_price_index = cleaned_prices.index(min(cleaned_prices))
min_price_title = titles[min_price_index]
min_price = cleaned_prices[min_price_index]

for title, price in zip(titles[:10], cleaned_prices[:10]):
    print(title, price)

elapsed_time = time.time() - start_time


plt.figure(figsize=(10, 6))
plt.bar(titles[:10], cleaned_prices[:10])
plt.xlabel('Titluri')
plt.ylabel('Preț (€)')
plt.title('Prețurile mașinilor rulate')
plt.xticks(rotation=45, ha='right')

plt.text(max_price_index, max_price, "Cea mai scumpă mașină:\n{} - {:.2f} €".format(max_price_title, max_price), ha='center', va='top')
plt.text(min_price_index, min_price, "Cea mai ieftină mașină:\n{} - {:.2f} €".format(min_price_title, min_price), ha='center', va='top')
plt.text(0.5, -0.1, "Timp de rulare: {:.2f} secunde".format(elapsed_time), ha='center', transform=plt.gca().transAxes)


plt.tight_layout()
plt.show()
