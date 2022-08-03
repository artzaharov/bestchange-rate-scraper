import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def get_html(url):
	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	response = requests.get(url, headers=headers)
	if response.ok:
		return response.text
	else:
		print('Невозможно получить данные с сайта!')


def get_data(html, idx):
	soup = BeautifulSoup(html, 'lxml')
	try:
		if idx < 4:
			best_rate = soup.find('table', id='content_table').find_all('td', class_='bi')[1].text.strip().split(' ')[0]
		else:
			best_rate = soup.find('table', id='content_table').find('div', class_='fs').text.strip().split(' ')[0]
	except Exception as ex:
		print(ex)

	return(best_rate)


def write_json(data):
	current_date = datetime.now().strftime('%Y.%m.%d_%H-%S')
	with open(f'rates_{current_date}.json', 'w') as file:
		json.dump(data, file, indent=4)


def main():
	all_rates = {}
	pairs = {
		'USDT to RUB': 'https://www.bestchange.ru/tether-trc20-to-visa-mastercard-rub.html',
		'USDT to UAH': 'https://www.bestchange.ru/tether-trc20-to-visa-mastercard-uah.html',
		'USDT to KZT': 'https://www.bestchange.ru/tether-trc20-to-visa-mastercard-kzt.html',
		'USDT to BYN': 'https://www.bestchange.ru/tether-trc20-to-visa-mastercard-byr.html',
		'RUB to USDT': 'https://www.bestchange.ru/visa-mastercard-rub-to-tether-trc20.html',
		'UAH to USDT': 'https://www.bestchange.ru/visa-mastercard-uah-to-tether-trc20.html',
		'KZT to USDT': 'https://www.bestchange.ru/visa-mastercard-kzt-to-tether-trc20.html',
		'BYN to USDT': 'https://www.bestchange.ru/visa-mastercard-byr-to-tether-trc20.html'
	}

	idx = 0
	for pair, url in pairs.items():
		best_rate = get_data(get_html(url), idx)
		all_rates[pair] = best_rate
		print(pair, best_rate)
		idx += 1

	try:
		write_json(all_rates)
	except Exception as ex:
		print(ex)

	print('Все готово!')


if __name__ == '__main__':
	main()
