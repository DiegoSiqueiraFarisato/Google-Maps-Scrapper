import logging
import argparse
import os
import platform
import time
from dataclasses import dataclass, asdict
from typing import List, Optional
from urllib.parse import urlparse

import pandas as pd
from playwright.sync_api import sync_playwright, Page


NON_OFFICIAL_WEBSITE_DOMAINS = {
    "facebook.com",
    "fb.com",
    "instagram.com",
    "wa.me",
    "api.whatsapp.com",
    "chat.whatsapp.com",
    "linktr.ee",
    "bio.link",
    "beacons.ai",
    "taplink.cc",
    "link.me",
    "tiktok.com",
    "youtube.com",
    "x.com",
    "thefork.com",
    "thefork.it",
    "twitter.com",
    "linkedin.com",
    "google.com",
    "maps.app.goo.gl",
    "goo.gl",
}


@dataclass
class Place:
    name: str = ""
    address: str = ""
    website: str = ""
    website_type: str = "none"
    phone_number: str = ""
    reviews_count: Optional[int] = None
    reviews_average: Optional[float] = None
    store_shopping: str = "No"
    in_store_pickup: str = "No"
    store_delivery: str = "No"
    place_type: str = ""
    opens_at: str = ""
    introduction: str = ""


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def extract_text(page: Page, xpath: str) -> str:
    try:
        locator = page.locator(xpath)
        if locator.count() > 0:
            return locator.inner_text().strip()
    except Exception as e:
        logging.warning(f"Failed to extract text for xpath {xpath}: {e}")
    return ""


def normalize_website(website: str) -> str:
    website = (website or "").strip()

    if not website:
        return ""

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    return website


def get_website_domain(website: str) -> str:
    website = normalize_website(website)

    if not website:
        return ""

    try:
        domain = urlparse(website).netloc.lower()
    except Exception:
        return ""

    return domain.removeprefix("www.")


def classify_website(website: str) -> str:
    website = normalize_website(website)

    if not website:
        return "none"

    domain = get_website_domain(website)

    if not domain:
        return "unknown"

    for allowed in NON_OFFICIAL_WEBSITE_DOMAINS:
        if domain == allowed or domain.endswith("." + allowed):
            return "social_or_profile"

    return "official_website"


def is_non_official_website(website: str) -> bool:
    return classify_website(website) != "official_website"


def extract_place(page: Page) -> Place:
    name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
    website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
    phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
    reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
    reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
    info1 = '//div[@class="LTs0Rc"][1]'
    info2 = '//div[@class="LTs0Rc"][2]'
    info3 = '//div[@class="LTs0Rc"][3]'
    opens_at_xpath = '//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'
    opens_at_xpath2 = '//div[@class="MkV9"]//span[@class="ZDu9vd"]//span[2]'
    place_type_xpath = '//div[@class="LBgpqf"]//button[@class="DkEaL "]'
    intro_xpath = '//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'

    place = Place()
    place.name = extract_text(page, name_xpath)
    place.address = extract_text(page, address_xpath)
    place.website = extract_text(page, website_xpath)
    place.phone_number = extract_text(page, phone_number_xpath)
    place.place_type = extract_text(page, place_type_xpath)
    place.introduction = extract_text(page, intro_xpath) or "None Found"
    place.website_type = classify_website(place.website)

    reviews_count_raw = extract_text(page, reviews_count_xpath)
    if reviews_count_raw:
        try:
            temp = (
                reviews_count_raw
                .replace("\xa0", "")
                .replace("(", "")
                .replace(")", "")
                .replace(",", "")
            )
            place.reviews_count = int(temp)
        except Exception as e:
            logging.warning(f"Failed to parse reviews count: {e}")

    reviews_avg_raw = extract_text(page, reviews_average_xpath)
    if reviews_avg_raw:
        try:
            temp = reviews_avg_raw.replace(" ", "").replace(",", ".")
            place.reviews_average = float(temp)
        except Exception as e:
            logging.warning(f"Failed to parse reviews average: {e}")

    for info_xpath in [info1, info2, info3]:
        info_raw = extract_text(page, info_xpath)
        if info_raw:
            temp = info_raw.split("·")
            if len(temp) > 1:
                check = temp[1].replace("\n", "").lower()

                if "shop" in check:
                    place.store_shopping = "Yes"
                if "pickup" in check:
                    place.in_store_pickup = "Yes"
                if "delivery" in check:
                    place.store_delivery = "Yes"

    opens_at_raw = extract_text(page, opens_at_xpath)
    if opens_at_raw:
        opens = opens_at_raw.split("⋅")
        if len(opens) > 1:
            place.opens_at = opens[1].replace("\u202f", "")
        else:
            place.opens_at = opens_at_raw.replace("\u202f", "")
    else:
        opens_at2_raw = extract_text(page, opens_at_xpath2)
        if opens_at2_raw:
            opens = opens_at2_raw.split("⋅")
            if len(opens) > 1:
                place.opens_at = opens[1].replace("\u202f", "")
            else:
                place.opens_at = opens_at2_raw.replace("\u202f", "")

    return place


def scrape_places(
    search_for: str,
    total: int,
    no_official_website: bool = False,
) -> List[Place]:
    setup_logging()
    places: List[Place] = []

    with sync_playwright() as p:
        if platform.system() == "Windows":
            browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            browser = p.chromium.launch(
                executable_path=browser_path,
                headless=False,
            )
        else:
            browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        try:
            page.goto(
                "https://www.google.com/maps/@32.9817464,70.1930781,3.67z?",
                timeout=60000,
            )
            page.wait_for_timeout(1000)

            page.locator(
                "//form[contains(@jsaction,'searchboxFormSubmit')]//input[@name='q']"
            ).fill(search_for)

            page.keyboard.press("Enter")

            page.wait_for_selector(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            )

            page.hover(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            )

            previously_counted = 0

            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_selector(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                )

                found = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()

                logging.info(f"Currently found: {found}")

                if found >= total:
                    break

                if found == previously_counted:
                    logging.info("Arrived at all available results")
                    break

                previously_counted = found

            listings = page.locator(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            ).all()[:total]

            listings = [listing.locator("xpath=..") for listing in listings]

            logging.info(f"Total listings to process: {len(listings)}")

            for idx, listing in enumerate(listings):
                try:
                    listing.click()

                    page.wait_for_selector(
                        '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]',
                        timeout=10000,
                    )

                    time.sleep(1.5)

                    place = extract_place(page)

                    if not place.name:
                        logging.warning(
                            f"No name found for listing {idx + 1}, skipping."
                        )
                        continue

                    if no_official_website and not is_non_official_website(
                        place.website
                    ):
                        logging.info(
                            f"Skipping '{place.name}': "
                            f"official website found ({place.website})."
                        )
                        continue

                    places.append(place)

                except Exception as e:
                    logging.warning(
                        f"Failed to extract listing {idx + 1}: {e}"
                    )

        finally:
            browser.close()

    return places


def save_places_to_csv(
    places: List[Place],
    output_path: str = "result.csv",
    append: bool = False,
):
    df = pd.DataFrame([asdict(place) for place in places])

    if df.empty:
        logging.warning("No data to save. DataFrame is empty.")
        return

    file_exists = os.path.isfile(output_path)
    mode = "a" if append else "w"
    header = not (append and file_exists)

    df.to_csv(output_path, index=False, mode=mode, header=header)

    logging.info(
        f"Saved {len(df)} places to {output_path} (append={append})"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--search",
        type=str,
        help="Search query for Google Maps",
    )

    parser.add_argument(
        "-t",
        "--total",
        type=int,
        help="Total number of results to scrape",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="result.csv",
        help="Output CSV file path",
    )

    parser.add_argument(
        "--append",
        action="store_true",
        help="Append results to the output file instead of overwriting",
    )

    parser.add_argument(
        "--no-official-website",
        action="store_true",
        help=(
            "Keep only places without a website or with social/profile "
            "links such as Facebook, Instagram, WhatsApp or Linktree"
        ),
    )

    args = parser.parse_args()

    search_for = args.search or "turkish stores in toronto Canada"
    total = args.total or 1
    append = args.append

    places = scrape_places(
        search_for=search_for+".csv",
        total=total,
        no_official_website=args.no_official_website,
    )

    save_places_to_csv(
        places=places,
        output_path=search_for+".csv",
        append=append,
    )


if __name__ == "__main__":
    main()