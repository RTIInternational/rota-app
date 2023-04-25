import os

from playwright.sync_api import sync_playwright

PROD_URL = os.environ["PROD_URL"]

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto(PROD_URL, wait_until="networkidle")
    # Note that Steamlit Cloud puts the app in a `streamlitApp` iframe,
    # so be sure to select that frame first. This is different than running the
    # test locally (where the frame does not exist)
    page.frame_locator('iframe[title="streamlitApp"]').get_by_role(
        "textbox", name="Input Offense"
    ).fill("BURGLARY - OVERNIGHT ACCOMMODATION, PERSON PRESENT")
    page.frame_locator('iframe[title="streamlitApp"]').get_by_role(
        "textbox", name="Input Offense"
    ).press("Enter")

    assert (
        page.frame_locator('iframe[title="streamlitApp"]')
        .get_by_role("row", name="BURGLARY")
        .get_by_role("cell", name="100", exact=True)
        .text_content()
        == "100"
    )

    browser.close()
