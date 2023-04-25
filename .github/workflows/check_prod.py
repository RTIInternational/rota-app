import os

from playwright.sync_api import sync_playwright

PROD_URL = os.environ.get("PROD_URL")

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto(f"https://rti-rota.streamlit.app/")
    page.get_by_role("textbox", name="Input Offense").fill(
        "BURGLARY - OVERNIGHT ACCOMMODATION, PERSON PRESENT"
    )
    page.get_by_role("textbox", name="Input Offense").press("Enter")
    assert page.get_by_test_id("glide-cell-1-0").text_content() == "BURGLARY"
    assert page.get_by_test_id("glide-cell-2-0").text_content() == "100"
    browser.close()
