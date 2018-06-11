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


def is_domains_paid(url, paid_days):
    today = datetime.datetime.today()
    expiration_date = get_domain_expiration_date(url)
    if expiration_date is None:
        return None
    if expiration_date - today >= datetime.timedelta(paid_days):
        return bool(expiration_date - today >= datetime.timedelta(paid_days))


def create_output_generator(url_list):
    for url in url_list:
        domains_paid = is_domains_paid(url, paid_days)
        response_ok = is_server_respond_ok(url)
        yield url, response_ok, domains_paid


def get_domain_expiration_date(url):
    domain = whois.whois(url)
    expiration_date = domain.expiration_date
    if type(expiration_date) == list:
        return expiration_date[0]
    else:
        return expiration_date


def print_site_health(url_response_ok_and_domains_paid):
    for url, site_paid, server_respond in url_response_ok_and_domains_paid:
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
    url_response_ok_and_domains_paid = create_output_generator(url_list)
    print_site_health(url_response_ok_and_domains_paid)
