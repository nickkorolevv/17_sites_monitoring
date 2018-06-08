import os
import sys
import datetime
import whois
import requests


def load_urls4check(path):
    with open(path, "r", encoding="utf-8") as file_with_urls:
        url_list = file_with_urls.read().split()
        return url_list


def is_server_respond_ok(url_list):
    for url in url_list:
        try:
            response_from_url = requests.get(url)
            yield response_from_url.ok
        except requests.ConnectionError:
            return None


def is_domains_paid(url_list, paid_days, server_respond_ok):
    today = datetime.datetime.today()
    for url in url_list:
        expiration_date = get_domain_expiration_date(url)
        if expiration_date is None:
            return None
        if expiration_date - today >= datetime.timedelta(paid_days):
            yield url, True, server_respond_ok
        else:
            return None, None, None


def get_domain_expiration_date(url):
    domain = whois.whois(url)
    expiration_date = domain.expiration_date
    if type(expiration_date) == list:
        return expiration_date[0]
    else:
        return expiration_date


def print_site_health(url_and_site_paid):
    for url, site_paid, server_respond in url_and_site_paid:
        is_paid = "Да" if site_paid else "Нет"
        is_respond_ok = "Да" if server_respond else "Нет"
        print("Сайт: ", url)
        print("Код состояния сервера 200: ", is_respond_ok)
        print("Проплачено на месяц вперед: ", is_paid)


if __name__ == "__main__":
    if len(sys.argv[1]) > 1:
        filepath = sys.argv[1]
    else:
        exit("Путь не введен")
    if not(os.path.exists(filepath)):
        exit("Файла нет в директории")
    paid_days = 30
    url_list = load_urls4check(filepath)
    server_respond_ok = is_server_respond_ok(url_list)
    url_and_site_paid = is_domains_paid(url_list, paid_days, server_respond_ok)
    print_site_health(url_and_site_paid)
