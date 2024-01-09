import requests
from bs4 import BeautifulSoup

urls_for_openai = []
names_for_openai = []
dicti = {}
url = 'https://langeek.co/en/vocab'
list_of_urls = []


def return_dicti(url):
    soap = BeautifulSoup(requests.get(url).content, 'html.parser')
    urls = soap.find_all(class_=
                         'tw-rounded-[30vmin] tw-border-transparent tw-text-base tw-bottom-0 tw-right-[.8rem] tw-font-text-bold tw-self-end tw-inline tw-my-6 tw-py-2 tw-mr-2 btn btn-primary btn-lg')
    for el in urls:
        urlka = el.get('href')
        list_of_urls.append('https://langeek.co' + urlka)
    for url in list_of_urls:
        soap = BeautifulSoup(requests.get(url).content, 'html.parser')
        names = soap.find_all(
            class_='tw-font-text-bold tw-text-black-1 tw-m-0 tw-text-lg tw-transition-all tw-duration-300')
        case = soap.find(
            class_='tw-w-full tw-mx-0 tw-px-0 lg:tw-py-4 sm:tw-py-1 tw-py-0 tw-flex tw-flex-wrap tw-flex-row tw-items-start sm:tw-mx-auto tw-justify-center')
        pathes = case.find_all(class_='hover:tw-no-underline')
        for path in pathes:
            if path.get('href') != None:
                url = 'https://langeek.co' + path.get('href')
                urls_for_openai.append(url)
        for name in names:
            names_for_openai.append(name.text)
    for i in range(len(urls_for_openai)):
        dicti[names_for_openai[i]] = urls_for_openai[i]
    return dicti
