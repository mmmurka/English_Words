import requests
import json
from bs4 import BeautifulSoup
from links_parser import return_result

dictionary = return_result('https://langeek.co/en/vocab')
words_list = {}
for group, dicti in dictionary.items():
    result = {}
    for i in dicti:
        tmp = {}
        page = requests.get(dicti[i])
        soup = BeautifulSoup(page.content, "html.parser")
        html_category = soup.find_all(
            class_="tw-font-text-bold tw-text-black-1 tw-text-base tw-mb-0 tw-transition-all tw-duration-300")
        headers = soup.find_all(class_="tw-w-full tw-relative tw-basis-full lg:tw-basis-1/2")

        for el in headers:

            dictionary = {}
            header = el.find(
                class_='tw-font-text-bold tw-text-black-1 tw-text-base tw-mb-0 tw-transition-all tw-duration-300').text
            urlka = 'https://langeek.co/'
            urlka += el.find(class_='hover:tw-no-underline').get('href')

            page = requests.get(urlka)
            soup = BeautifulSoup(page.content, "html.parser")
            words = soup.find_all(class_="tw-text-[1.75rem] sm:tw-text-[2rem] tw-font-text-bold")
            definitions = soup.find_all(class_='ReviewCardFron_wordTranslation__qn3g5')
            for index in range(len(words)):
                dictionary[words[index].text] = definitions[index].text
                tmp[header] = dictionary
        result[i] = tmp
    words_list[group] = result
with open('../database/data/words_list.json', 'w') as outfile:
    json.dump(words_list, outfile)
