import re
import csv
from os import path, remove


def log_error(error_name, errors, url):
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(f"{errors}: Unable to find an element in: {url}")
        file.write("\n")
        file.write(str(error_name))
        file.write("\n")


def parser_link(url):
    """ Cleans an url"""
    try:
        return re.search(r"(https://m.facebook.com/groups/\w.+?/permalink/\d.+?/)",
                         url).group(0)
    except AttributeError:
        return url


def save_as_csv(data):
    with open("data.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Group_name, Publisher_name, Description, Collected at
        writer.writerow(["name",
                         "published_at",
                         "group_name",
                         "description",
                         "url",
                         "collected_at"])
        writer.writerows(data)


def clean_log():
    if path.exists("log.txt"):
        remove("log.txt")
