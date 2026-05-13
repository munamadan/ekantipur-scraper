import json
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


BASE_URL = "https://ekantipur.com"


def clean(value):
    if not value:
        return None
    text = " ".join(value.split())
    return text or None


def abs_url(url):
    if not url:
        return None
    return urljoin(BASE_URL, url)


def extract_entertainment(page):
    """Read the entertainment listing and return article dictionaries."""
    page.goto(f"{BASE_URL}/entertainment", wait_until="domcontentloaded")
    page.wait_for_timeout(1500)

    cards = page.query_selector_all(".category-main-wrapper .category")
    items = []

    for card in cards:
        title_el = card.query_selector("h2 a")
        if not title_el:
            continue

        title = clean(title_el.text_content())
        if not title:
            continue

        img = card.query_selector("img")
        image_url = None
        if img:
            image_url = img.get_attribute("src") or img.get_attribute("data-src")

        author_el = card.query_selector(".author-name a")
        author = clean(author_el.text_content()) if author_el else None
        category_el = card.query_selector(".category-name a")
        category = clean(category_el.text_content()) if category_el else None

        items.append(
            {
                "title": title,
                "image_url": abs_url(image_url),
                "category": category or "मनोरञ्जन",
                "author": author,
            }
        )

        if len(items) == 5:
            break

    return items


def extract_cartoon_of_day(page):
    """Read the homepage cartoon block and return one cartoon dictionary."""
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
