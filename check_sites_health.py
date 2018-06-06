import os
import sys
import datetime
import whois
import requests


def load_urls4check(path):
    with open(path, "r", encoding="utf-8") as file_with_urls:
        url_list = file_with_urls.read().split()
        return url_list


def is_server_respond_ok(url):
    try:
        response_from_url = requests.get(url)
        return response_from_url.ok
    except requests.ConnectionError:
        return None


def is_domain_paid(url_list, paid_days):
    today = datetime.datetime.today()
    for url in url_list:
        expiration_date = get_domain_expiration_date(url)
        if expiration_date is None:
            return None
        if expiration_date - today >= datetime.timedelta(paid_days):
            yield url, True
        else:
            return None, None


def get_domain_expiration_date(url):
    domain = whois.whois(url)
    expiration_date = domain.expiration_date
    if type(expiration_date) == list:
        return expiration_date[0]
    else:
        return expiration_date


def print_site_health(url_and_site_paid):
    for url, site_paid in url_and_site_paid:
        is_paid = "Да" if site_paid else "Нет"
        server_respond = is_server_respond_ok(url)
        is_respond_ok = "Да" if server_respond else "Нет"
        print(
            "Сайт: ", url,
            "Код состояния сервера 200: ", is_respond_ok,
            "Проплачено на месяц вперед: ", is_paid
        )


if __name__ == "__main__":
    if len(sys.argv[1]) > 1:
        filepath = sys.argv[1]
    else:
        exit("Путь не введен")
    if not(os.path.exists(filepath)):
        exit("Файла нет в директории")
    paid_days = 30
    url_list = load_urls4check(filepath)
    url_and_site_paid = is_domain_paid(url_list, paid_days)
    print_site_health(url_and_site_paid)
