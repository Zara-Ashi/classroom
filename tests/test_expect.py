import re
from playwright.sync_api import sync_playwright, expect


def make_browser(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    return browser, page


# ==================== 28x01: Появление сообщения ====================

def test_28x01_dynamic_loading_1():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
        page.get_by_role("button", name="Start").click()

        hello = page.locator("#finish")
        expect(hello).to_be_visible(timeout=10_000)
        expect(hello).to_have_text("Hello World!")

        print(f"✅ Появилось: {hello.inner_text()}")

        browser.close()


# ==================== 28x02: Исчезновение спиннера ====================

def test_28x02_dynamic_loading_2():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
        page.get_by_role("button", name="Start").click()

        spinner = page.locator("#loading")
        expect(spinner).to_be_hidden(timeout=10_000)

        hello = page.locator("#finish")
        expect(hello).to_be_visible()
        expect(hello).to_have_text("Hello World!")

        print(f"✅ Спиннер исчез. Текст: {hello.inner_text()}")

        browser.close()



# ==================== 28x05: Состояние кнопок ====================

def test_28x05_add_remove_elements():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/add_remove_elements/")

        # Нажимаем "Add Element" 3 раза
        add_btn = page.get_by_role("button", name="Add Element")
        add_btn.click()
        add_btn.click()
        add_btn.click()

        delete_buttons = page.get_by_role("button", name="Delete")
        expect(delete_buttons).to_have_count(3)
        print(f"✅ Кнопок Delete: {delete_buttons.count()}")

        # Удаляем первую
        delete_buttons.first.click()

        expect(delete_buttons).to_have_count(2)
        print(f"✅ После удаления кнопок Delete: {delete_buttons.count()}")

        browser.close()


# ==================== 28x06: URL и заголовок после навигации ====================

def test_28x06_url_and_title():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://playwright.dev/python/")

        page.get_by_role("link", name="Docs").first.click()

        expect(page).to_have_url(re.compile(r".*/docs/.*"), timeout=10_000)
        expect(page).to_have_title(re.compile(r".*Installation.*"))

        print(f"✅ URL: {page.url}")
        print(f"✅ Title: {page.title()}")

        browser.close()