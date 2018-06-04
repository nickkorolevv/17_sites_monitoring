import os
import sys
import datetime
import whois
import requests


PAID_DAYS = 30


def load_urls4check(path):
    with open(path, "r", encoding="utf-8") as file_with_urls:
        url_list = file_with_urls.read().split()
        return url_list


def is_server_respond_with_200(url):
    try:
        response_from_url = requests.get(url)
        return response_from_url.ok
    except requests.ConnectionError:
        return None


def is_site_paid(url_list):
    today = datetime.datetime.today()
    for url in url_list:
        if get_domain_expiration_date(url) - today >= datetime.timedelta(PAID_DAYS):
            yield url, True
        else:
            return None


def get_domain_expiration_date(url):
    domain = whois.whois(url)
    expiration_date = domain.expiration_date
    if type(expiration_date) == list:
        return expiration_date[0]
    else:
        return expiration_date


def print_site_health(url_and_site_paid):
    for url, site_paid in url_and_site_paid:
        if site_paid:
            site_paid = "Да"
        else:
            site_paid = "Нет"
        server_respond = is_server_respond_with_200(url)
        if server_respond:
            server_respond = "Да"
        else:
            server_respond = "Нет"
        print(
            "Сайт: ", url,
            "Код состояния сервера 200: ", server_respond,
            "Проплачено на месяц вперед: ", site_paid
        )


if __name__ == "__main__":
    if len(sys.argv[1]) > 1:
        filepath = sys.argv[1]
    else:
        exit("Директория не введена")
    if not(os.path.exists(filepath)):
        exit("Файла нет в директории")
    url_list = load_urls4check(filepath)
    url_and_site_paid = is_site_paid(url_list)
    print_site_health(url_and_site_paid)
