import time
from playwright.sync_api import expect, TimeoutError


# 🔹 загрузка главной страницы и сравнение load vs domcontentloaded
def test_page_load_states(page, base_url):
    start = time.time()
    page.goto(base_url)
    page.wait_for_load_state("load")
    load_time = time.time() - start

    assert page.title() != ""

    page2 = page.context.new_page()

    start = time.time()
    page2.goto(base_url)
    page2.wait_for_load_state("domcontentloaded")
    dom_time = time.time() - start

    print(f"load: {load_time:.4f}")
    print(f"domcontentloaded: {dom_time:.4f}")


# 🔹 ожидание появления элемента после динамической загрузки
def test_wait_for_element_visible(page, base_url):
    page.goto(f"{base_url}/dynamic_loading/1")
    page.click("text=Start")

    page.wait_for_selector("#finish", state="visible")
    expect(page.locator("#finish")).to_be_visible()


# 🔹 ожидание исчезновения loader и появления результата
def test_wait_for_loader_to_disappear(page, base_url):
    page.goto(f"{base_url}/dynamic_loading/2")
    page.click("text=Start")

    start = time.time()
    page.wait_for_selector(".loader", state="hidden")
    print("wait:", time.time() - start)


# 🔹 проверка успешного и неуспешного логина через wait_for_url
def test_login_redirect_success_and_failure(login, context, base_url):
    # проверка успешного логина
    assert "/secure" in login.url

    # проверка неуспешного логина
    page = context.new_page()
    page.goto(f"{base_url}/login")
    page.fill("#username", "tomsmith")
    page.fill("#password", "wrongpassword")
    page.click("button[type='submit']")

    try:
        page.wait_for_url("**/secure", timeout=5000)
        assert False
    except TimeoutError:
        pass


# 🔹 комбинированные ожидания после логина
def test_combined_wait_strategies(login):
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