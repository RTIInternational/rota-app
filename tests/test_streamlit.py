from subprocess import Popen
import re
from playwright.sync_api import Page, expect
from time import sleep
import pytest

# Code to use playwright locally outside of a test
# from playwright.sync_api import sync_playwright
# with sync_playwright() as pw:
#     browser = pw.chromium.launch()
#     page = browser.new_page()
#     page.goto(f"http://localhost:55554")
#     print(page.title())
#     browser.close()


@pytest.fixture(scope="session")
def streamlit_app_session():
    """This fixture will last an entire test session.
    That means the changes made in a test will accumulate within the app.
    If you have a test that is dependent on specific state when it starts,
    don't use this but use a 'function' scoped fixture instead.
    """
    PORT = 55554
    streamlit_process = Popen(
        [
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            str(PORT),
            "--server.headless",
            "true",
        ]
    )
    # If you don't wait for the app to start, you'll get ERR_CONNECTION_REFUSED
    sleep(2)
    yield (streamlit_process, PORT)
    streamlit_process.kill()


def test_single_input(page: Page, streamlit_app_session):
    _, port = streamlit_app_session
    page.goto(f"http://localhost:{port}")
    page.get_by_role("textbox", name="Input Offense").fill(
        "BURGLARY - OVERNIGHT ACCOMMODATION, PERSON PRESENT"
    )
    page.get_by_role("textbox", name="Input Offense").press("Enter")

    assert (
        page.get_by_role("row", name="BURGLARY")
        .get_by_role("cell", name="100", exact=True)
        .text_content()
        == "100"
    )
