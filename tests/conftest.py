import pytest
from playwright.sync_api import sync_playwright

BASE = "https://the-internet.herokuapp.com"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def login(page):
    page.goto(f"{BASE}/login")
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button[type='submit']")
    page.wait_for_url("**/secure")
    return page