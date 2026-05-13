import json
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE_URL = "https://ekantipur.com"


def clean(value: str | None) -> str | None:
    if not value:
        return None
    text = " ".join(value.split())
    return text or None


def abs_url(url: str | None) -> str | None:
    if not url:
        return None
    return urljoin(BASE_URL, url)


def first_text(root, selectors: list[str]) -> str | None:
    for selector in selectors:
        el = root.query_selector(selector)
        if el:
            return clean(el.text_content())
    return None


def first_attr(root, selectors: list[str], attr: str) -> str | None:
    for selector in selectors:
        el = root.query_selector(selector)
        if el:
            value = el.get_attribute(attr)
            if value:
                return clean(value)
    return None


def extract_entertainment(page) -> list[dict]:
    page.goto(f"{BASE_URL}/entertainment", wait_until="domcontentloaded")
    page.wait_for_timeout(1500)

    cards = page.query_selector_all(".category-main-wrapper .category")
    items: list[dict] = []

    for card in cards:
        title = first_text(card, ["h2 a", "h2", "h3 a", "h3", "a[title]"])
        if not title:
            title = first_attr(card, ["a[title]"], "title")
        if not title:
            continue

        image_url = first_attr(card, [".category-image img", "img"], "src")
        if not image_url:
            image_url = first_attr(card, [".category-image img", "img"], "data-src")

        category = first_text(card, [".category-name a", ".tag", ".meta a"])
        if not category:
            category = "मनोरञ्जन"

        author = first_text(card, [".author-name a", ".author", ".byline", ".author-name"])

        items.append(
            {
                "title": title,
                "image_url": abs_url(image_url),
                "category": category,
                "author": author,
            }
        )

        if len(items) >= 5:
            break

    return items


def extract_cartoon_of_day(page) -> dict:
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)

    section = page.locator(
        "section:has(h4 a[href*='/cartoon']), section:has-text('व्यंग्यचित्र'), section:has-text('कार्टुन')"
    ).first

    if section.count() == 0:
        return {"title": None, "image_url": None, "author": None}

    title = section.locator(".swiper-slide img").first.get_attribute("alt")
    image_url = section.locator(".swiper-slide img").first.get_attribute("src")
    if not image_url:
        image_url = section.locator(".swiper-slide img").first.get_attribute("data-src")
    author = None
    for selector in [".author-name a", ".author", ".byline"]:
        loc = section.locator(selector).first
        if loc.count() > 0:
            author = clean(loc.text_content())
            if author:
                break

    return {
        "title": clean(title),
        "image_url": abs_url(image_url),
        "author": clean(author),
    }


def main() -> None:
    data = {"entertainment_news": [], "cartoon_of_the_day": {"title": None, "image_url": None, "author": None}}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            data["entertainment_news"] = extract_entertainment(page)
        except PlaywrightTimeoutError:
            data["entertainment_news"] = []

        try:
            data["cartoon_of_the_day"] = extract_cartoon_of_day(page)
        except PlaywrightTimeoutError:
            data["cartoon_of_the_day"] = {"title": None, "image_url": None, "author": None}

        browser.close()

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
