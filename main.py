import requests
import bs4
import fake_headers
import unicodedata
import json

headers_gen = fake_headers.Headers(browser='chrome', os='win')
response = requests.get(
    url='https://spb.hh.ru/search/vacancy?ored_clusters=true&hhtmFrom=vacancy_search_list&search_field=description'
        '&enable_snippets=false&L_save_area=true&area=1&area=2&text=python+flask+django',
    headers=headers_gen.generate())
html_data = response.text
soup = bs4.BeautifulSoup(html_data, 'lxml')
articles = soup.find_all('div', class_='serp-item')
parsed_vacancy = []
for article in articles:
    vacancy_name = article.find('a').text
    company_name = article.find('a', class_="bloko-link bloko-link_kind-tertiary").text
    href = article.find('a', class_='serp-item__title')['href']
    if article.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}):
        money = article.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).text
    else:
        money = 'Salary is not specified'
    city = article.find('div', {'data-qa': "vacancy-serp__vacancy-address"}, class_="bloko-text" ).text
    parsed_vacancy.append({
        "Название вакансии": unicodedata.normalize('NFKD', vacancy_name),
        "Ссылка на вакансию": href,
        "Название компании": unicodedata.normalize('NFKD', company_name),
        "Название города": unicodedata.normalize('NFKD', city),
        "Вилка зп": unicodedata.normalize('NFKD', money)})

print(parsed_vacancy)

with open('parsed_vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(parsed_vacancy, file, ensure_ascii=False)


