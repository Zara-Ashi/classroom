import time
from playwright.sync_api import sync_playwright, expect, TimeoutError

BASE = "https://the-internet.herokuapp.com"


# 29x01. Ожидание загрузки страницы
def test_29x01_load_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        start = time.time()
        page.goto(BASE)
        page.wait_for_load_state("load")
        load_time = time.time() - start

        assert page.title() != ""

        page2 = browser.new_page()
        start = time.time()
        page2.goto(BASE)
        page2.wait_for_load_state("domcontentloaded")
        dom_time = time.time() - start

        print(f"load: {load_time:.4f}")
        print(f"domcontentloaded: {dom_time:.4f}")

        browser.close()


#29x02. Ожидание элемента
def test_29x02_wait_for_element():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto(f"{BASE}/dynamic_loading/1")
        page.click("text=Start")

        page.wait_for_selector("#finish", state="visible")
        text = page.locator("#finish").inner_text()

        assert "Hello World!" in text
        expect(page.locator("#finish")).to_be_visible()

        browser.close()


#29x03. Ожидание исчезновения
def test_29x03_wait_for_disappear():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto(f"{BASE}/dynamic_loading/2")
        page.click("text=Start")

        start = time.time()
        page.wait_for_selector(".loader", state="hidden")
        duration = time.time() - start

        text = page.locator("#finish").inner_text()
        assert "Hello World!" in text

        print(f"wait time: {duration:.4f}")

        browser.close()


#29x04. Ожидание URL
def test_29x04_wait_for_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # успешный логин
        page = browser.new_page()
        page.goto(f"{BASE}/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button[type='submit']")
        page.wait_for_url("**/secure")
        assert "/secure" in page.url

        # неуспешный логин
        page2 = browser.new_page()
        page2.goto(f"{BASE}/login")
        page2.fill("#username", "tomsmith")
        page2.fill("#password", "wrongpassword")
        page2.click("button[type='submit']")

        try:
            page2.wait_for_url("**/secure", timeout=5000)
            assert False
        except TimeoutError:
            pass

def test_29x12_combined_waits():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE}/login")

        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")

        page.click("button[type='submit']")

        start_url = time.time()
        page.wait_for_url("**/secure")
        url_time = time.time() - start_url

        start_net = time.time()
        page.wait_for_load_state("networkidle")
        net_time = time.time() - start_net

        welcome_locator = page.locator("#content")
        start_expect = time.time()
        expect(welcome_locator).to_contain_text("Welcome")
        expect_time = time.time() - start_expect

        print(f"URL wait: {url_time:.4f}")
        print(f"networkidle wait: {net_time:.4f}")
        print(f"expect wait: {expect_time:.4f}")

        browser.close()