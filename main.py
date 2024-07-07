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
    for section in relevant_divs:
        title = section.find("h3", {
            "class": "bu-stat-title"
        }).get_text().strip()
        value = reduce(lambda s, t: s + t, map(lambda s: s.get_text(),
                       section.find_all("span", {
                        "class": "bu-stat-value-field"
                       })))
        ans["Campus Stats"].append({title: value})


def main() -> None:
    URL = "http://www.bu.edu/president/boston-university-facts-stats"
    res = requests.get(URL)
    print("Status code:", res.status_code)
    summary(res)

    ans = defaultdict(lambda: [])
    campus_stats(res, ans)

    json_ans = json.dumps(ans)
    print(json_ans)


if __name__ == "__main__":
    main()
