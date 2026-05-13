import json

from playwright.sync_api import sync_playwright


BASE_URL = "https://ekantipur.com"


def extract_entertainment(page):
    return []


def extract_cartoon_of_day(page):
    return {"title": None, "image_url": None, "author": None}


def main():
    data = {
        "entertainment_news": [],
        "cartoon_of_the_day": {"title": None, "image_url": None, "author": None},
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        data["entertainment_news"] = extract_entertainment(page)
        data["cartoon_of_the_day"] = extract_cartoon_of_day(page)
        browser.close()

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
