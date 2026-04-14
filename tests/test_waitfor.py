import time
from playwright.sync_api import expect, TimeoutError


# 🔹 29x01. Ожидание загрузки страницы
def test_29x01_load_state(page, context, base_url):
    import time

    start = time.time()
    page.goto(base_url)
    page.wait_for_load_state("load")
    load_time = time.time() - start

    assert page.title() != ""

    page2 = context.new_page()

    start = time.time()
    page2.goto(base_url)
    page2.wait_for_load_state("domcontentloaded")
    dom_time = time.time() - start

    print(load_time, dom_time)


# 🔹 29x02. Ожидание элемента
def test_29x02_wait_for_element(page, base_url):
    page.goto(f"{base_url}/dynamic_loading/1")
    page.click("text=Start")

    page.wait_for_selector("#finish", state="visible")
    expect(page.locator("#finish")).to_be_visible()


# 🔹 29x03. Ожидание исчезновения
def test_29x03_wait_for_disappear(page, base_url):
    page.goto(f"{base_url}/dynamic_loading/2")
    page.click("text=Start")

    start = time.time()
    page.wait_for_selector(".loader", state="hidden")
    print("wait:", time.time() - start)


def test_29x04_wait_for_url(login, context, base_url):
    assert "/secure" in login.url

    page = context.new_page()
    page.goto(f"{base_url}/login")
    page.fill("#username", "tomsmith")
    page.fill("#password", "wrongpassword")
    page.click("button[type='submit']")

    try:
        page.wait_for_url("**/secure", timeout=5000)
        assert False
    except Exception:
        pass


# 🔹 29x12. Комбинированные ожидания
def test_29x12_combined_waits(login):
    page = login

    start = time.time()
    page.wait_for_url("**/secure")
    url_time = time.time() - start

    start = time.time()
    page.wait_for_load_state("networkidle")
    net_time = time.time() - start

    start = time.time()
    expect(page.locator("#content")).to_contain_text("Welcome")
    expect_time = time.time() - start

    print(f"URL wait: {url_time:.4f}")
    print(f"networkidle: {net_time:.4f}")
    print(f"expect: {expect_time:.4f}")