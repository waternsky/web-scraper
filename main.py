#!/usr/bin/env python

import requests
import json
from bs4 import BeautifulSoup
from functools import reduce
from collections import defaultdict


def summary(res: requests.Response) -> None:
    soup = BeautifulSoup(res.content, "html.parser")
    print("Title:", soup.title.get_text())
    with open("o.html", 'w') as f:
        f.write(soup.body.prettify())
    print("Consider checking o.html for relevant tags ...\n")


def campus_stats(res: requests.Response, ans: defaultdict) -> None:
    soup = BeautifulSoup(res.content, "html.parser")
    relevant_divs = soup.find_all("div", {
        "class": "bu-stat-inner js-bu-stat-inner"
    })
    val = {}
    for section in relevant_divs:
        title = section.find("h3", {
            "class": "bu-stat-title"
        }).get_text().strip()
        value = reduce(lambda s, t: s + t, map(lambda s: s.get_text(),
                       section.find_all("span", {
                        "class": "bu-stat-value-field"
                       })))
        val[title] = value
    ans["Campus Stats"] = val


def community_stats(res: requests.Response, ans: defaultdict) -> None:
    soup = BeautifulSoup(res.content, "html.parser")
    relevant_sections = soup.find_all("section", {
        "class": "stat-section"
    })
    for section in relevant_sections:
        header = section.find("h4", {
            "class": "stat-group-title"
        }).get_text().strip()
        labels = list(map(lambda s: s.get_text(), section.find_all("span", {
            "class": "stat-label"
        })))
        figures = list(map(lambda s: s.get_text(), section.find_all("span", {
            "class": "stat-figure"
        })))
        ans[header] = dict(zip(labels, figures))


def main() -> None:
    URL = "http://www.bu.edu/president/boston-university-facts-stats"
    res = requests.get(URL)
    print("Status code:", res.status_code)
    summary(res)

    ans = defaultdict(lambda: [])
    campus_stats(res, ans)
    community_stats(res, ans)

    json_ans = json.dumps(ans, indent=4)
    print(json_ans)


if __name__ == "__main__":
    main()
