from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
from time import sleep

username = input('Введите свой логин в Проза.ру: ')
password = input('Введите свой пароль в Проза.ру: ')


def get_authors_online():
    '''
    Get all the authors that are currently online
    '''
    html = requests.get('https://proza.ru/authors/online.html').text
    bs = BeautifulSoup(html, 'html.parser')
    authors_online = bs.find('td').find_all('li')
    authors_urls = []
    for i in authors_online:
        authors_urls.append(i.find('a').attrs['href'])
    return authors_urls


def login_into_website(username, password):
    '''
    Get logged in under the provided username and password
    passed into input() functions and then iterate through the list of authors
    '''
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://proza.ru/login')
        username_locator = page.locator(
            "xpath=/html/body/div/table/tbody/tr/td/index/form/div/table/\
                tbody/tr/td/table/tbody/tr/td/div[2]/table/tbody/tr[1]/td\
                    [2]/input")
        password_locator = page.locator(
            "xpath=/html/body/div/table/tbody/tr/td/index/form/div/table/\
                tbody/tr/td/table/tbody/tr/td/div[2]/table/tbody/tr[2]/td\
                    [2]/input")
        button_submit = page.locator(
            "xpath=/html/body/div/table/tbody/tr/td/index/form/div/table/\
                tbody/tr/td/table/tbody/tr/td/div[2]/table/tbody/tr[3]/td\
                    [2]/input")
        username_locator.fill(username)
        sleep(1)
        password_locator.fill(password)
        sleep(1)
        button_submit.click()
        sleep(2)

        for i in get_authors_online():
            page.goto('https://proza.ru' + i)
            sleep(1)
            page.goto('https://proza.ru/authors/online.html')
            sleep(1)


def main():
    login_into_website(username, password)


if __name__ == '__main__':
    main()
