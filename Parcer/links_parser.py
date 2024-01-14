import requests
from bs4 import BeautifulSoup


def return_result(url):
    index = -1
    result = {}
    url = 'https://langeek.co/en/vocab'
    list_of_urls = []
    names_of_subjects_group = []
    soap = BeautifulSoup(requests.get(url).content, 'html.parser')
    div_groups = soap.find_all(
        class_="[&_h3]:tw-text-[1.5rem] [&_h3]:md:tw-text-[1.75rem] [&_h6]:tw-leading-[1.6rem] [&_h6]:tw-text-[#092550] [&_h3]:tw-text-primary-dark lg:tw-mx-4 sm:tw-mx-1 tw-mx-0 tw-mt--2 tw-mb-6 tw-overflow-hidden tw-hidden sm:tw-flex md:tw-flex-nowrap tw-flex-wrap tw-justify-center tw-items-stretch row"
    )
    for set in div_groups:
        name_of_set = set.find(
            class_="tw-mb-6 sm:tw-mb-0"
        )
        names_of_subjects_group.append(name_of_set.text)
    urls = soap.find_all(class_=
                         'tw-rounded-[30vmin] tw-border-transparent tw-text-base tw-bottom-0 tw-right-[.8rem] tw-font-text-bold tw-self-end tw-inline tw-my-6 tw-py-2 tw-mr-2 btn btn-primary btn-lg')
    for el in urls:
        tmp_url = el.get('href')
        list_of_urls.append('https://langeek.co' + tmp_url)
    for url in list_of_urls:
        index += 1
        subject_url = {}
        urls_of_subjects = []
        names_of_subjects = []
        soap = BeautifulSoup(requests.get(url).content, 'html.parser')
        names = soap.find_all(
            class_='tw-font-text-bold tw-text-black-1 tw-m-0 tw-text-lg tw-transition-all tw-duration-300')
        case = soap.find(
            class_='tw-w-full tw-mx-0 tw-px-0 lg:tw-py-4 sm:tw-py-1 tw-py-0 tw-flex tw-flex-wrap tw-flex-row tw-items-start sm:tw-mx-auto tw-justify-center')
        paths = case.find_all(class_='hover:tw-no-underline')

        for path in paths:
            if path.get('href') != None:
                url = 'https://langeek.co' + path.get('href')
                urls_of_subjects.append(url)
        for name in names:
            names_of_subjects.append(name.text)
        for i in range(len(urls_of_subjects)):
            subject_url[names_of_subjects[i]] = urls_of_subjects[i]
        result[names_of_subjects_group[index]] = subject_url
    return result