import os
from playwright.sync_api import sync_playwright, expect


# ==================== Вспомогательные функции ====================

def make_browser(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    return browser, page


# ==================== 26x01: Главная страница ====================

def test_main_page():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/")

        title = page.title()
        assert "The Internet" in title, (
            f"❌ Заголовок страницы не содержит 'The Internet'. Текущий: '{title}'"
        )

        h1 = page.locator("h1").first.inner_text()
        assert h1 == "Welcome to the-internet", (
            f"❌ Тег <h1> не совпадает. Текущий: '{h1}'"
        )

        h2 = page.locator("h2").first.inner_text()
        assert h2 == "Available Examples", (
            f"❌ Тег <h2> не совпадает. Текущий: '{h2}'"
        )

        print(f"✅ Сайт доступен. Заголовок: {title}")
        print(f"h1: {h1}")
        print(f"h2: {h2}")

        browser.close()


# ==================== 26x02: Навигация ====================

def test_navigate_to_example():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/")
        page.get_by_text("Form Authentication").click()

        assert "/login" in page.url, (
            f"❌ URL не содержит '/login'. Текущий: '{page.url}'"
        )
        print(f"✅ Перешли в: Form Authentication | URL: {page.url}")

        browser.close()


# ==================== 26x03: Форма входа ====================

def test_login_form():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.get_by_role("button", name="Login").click()

        page.wait_for_url("**/secure")
        assert "/secure" in page.url, (
            f"❌ URL не содержит '/secure'. Текущий: '{page.url}'"
        )
        print(f"✅ Успешный вход! URL: {page.url}")

        page.get_by_role("link", name="Logout").click()
        page.wait_for_url("**/login")

        assert "/login" in page.url, (
            f"❌ URL не содержит '/login'. Текущий: '{page.url}'"
        )
        print(f"✅ Успешный выход! URL: {page.url}")

        browser.close()


# ==================== 26x04: Чекбоксы ====================

def test_checkboxes():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/checkboxes")

        checkbox1 = page.locator("input[type='checkbox']").nth(0)
        checkbox2 = page.locator("input[type='checkbox']").nth(1)

        assert not checkbox1.is_checked(), "❌ Checkbox 1 должен быть НЕ отмечен изначально"
        assert checkbox2.is_checked(), "❌ Checkbox 2 должен быть отмечен изначально"
        print("✅ Начальное состояние верно: Checkbox1=False, Checkbox2=True")

        checkbox1.check()
        checkbox2.uncheck()

        assert checkbox1.is_checked(), "❌ Checkbox 1 должен быть отмечен"
        assert not checkbox2.is_checked(), "❌ Checkbox 2 должен быть НЕ отмечен"

        print(f"✅ Checkbox 1: checked={checkbox1.is_checked()}")
        print(f"✅ Checkbox 2: checked={checkbox2.is_checked()}")

        browser.close()


# ==================== 26x05: Dropdown ====================

def test_dropdown():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/dropdown")
        dropdown = page.locator("#dropdown")

        assert dropdown.input_value() == "", (
            f"❌ Начальное значение должно быть пустым. Текущее: '{dropdown.input_value()}'"
        )
        print(f"✅ Начальное значение пустое")

        dropdown.select_option(label="Option 1")
        assert dropdown.input_value() == "1", "❌ Должно быть выбрано 'Option 1'"
        print("✅ Выбрано: Option 1")

        dropdown.select_option(label="Option 2")
        assert dropdown.input_value() == "2", "❌ Должно быть выбрано 'Option 2'"
        print("✅ Выбрано: Option 2")

        browser.close()


# ==================== 26x07: Поля ввода ====================

def test_inputs():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/inputs")
        field = page.locator("input[type='number']")

        field.fill("123")
        assert field.input_value() == "123", "❌ Значение должно быть 123"

        field.clear()
        assert field.input_value() == "", "❌ Поле должно быть пустым"

        field.fill("456")
        assert field.input_value() == "456", "❌ Значение должно быть 456"

        print(f"✅ Введено: {field.input_value()}")

        browser.close()


# ==================== 26x08: Hover ====================

def test_hover():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/hovers")

        first_figure = page.locator(".figure").first
        first_figure.hover()

        caption = first_figure.locator(".figcaption")
        expect(caption).to_be_visible()

        text = caption.inner_text()
        assert "name: user1" in text, (
            f"❌ Текст не содержит 'name: user1'. Текущий: '{text}'"
        )
        print(f"✅ Навели на изображение. Текст: {text.strip()}")

        browser.close()


# ==================== 26x09: JS Alert ====================

def test_js_alert():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/javascript_alerts")
        page.on("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Click for JS Alert").click()

        result = page.locator("#result").inner_text()
        assert "You successfully clicked an alert" in result, (
            f"❌ Сообщение не совпадает. Текущее: '{result}'"
        )
        print(f"✅ Alert принят. Сообщение: {result}")

        browser.close()


# ==================== 26x10: Загрузка файлов ====================

def test_file_upload():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        file_path = "test_upload.txt"
        with open(file_path, "w") as f:
            f.write("Hello Playwright")

        page.goto("https://the-internet.herokuapp.com/upload")
        page.set_input_files("#file-upload", file_path)
        page.click("#file-submit")

        uploaded = page.locator("#uploaded-files").inner_text()
        assert "test_upload.txt" in uploaded, (
            f"❌ Файл не найден в списке. Текущее: '{uploaded}'"
        )
        print(f"✅ Файл загружен: {uploaded.strip()}")

        os.remove(file_path)
        browser.close()


# ==================== 26x11: Динамическая загрузка ====================

def test_dynamic_loading():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
        page.get_by_role("button", name="Start").click()

        hello = page.locator("#finish")
        expect(hello).to_be_visible(timeout=10_000)

        text = hello.inner_text()
        assert "Hello World!" in text, (
            f"❌ Текст не совпадает. Текущий: '{text}'"
        )
        print(f"✅ Элемент появился: {text.strip()}")

        browser.close()


# ==================== 26x12: Финальный тест-сьют ====================

def run_full_test():
    results = {}
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser, page = make_browser(p)

        steps = [
            ("Form Authentication", _step_auth),
            ("Checkboxes",          _step_checkboxes),
            ("Dropdown",            _step_dropdown),
            ("Inputs",              _step_inputs),
            ("Hovers",              _step_hovers),
        ]

        for name, step_fn in steps:
            try:
                step_fn(page)
                page.screenshot(path=f"screenshots/{name.lower().replace(' ', '_')}.png")
                results[name] = "✅"
            except Exception as e:
                results[name] = f"❌ {e}"

        browser.close()

    print("\n📊 ОТЧЁТ:")
    for section, status in results.items():
        print(f"  {status} {section}")

    all_passed = all(v == "✅" for v in results.values())
    print("\n  Все тесты пройдены!" if all_passed else "\n  ❌ Есть упавшие тесты!")


def _step_auth(page):
    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/secure")
    page.get_by_role("link", name="Logout").click()
    page.wait_for_url("**/login")


def _step_checkboxes(page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = page.locator("input[type='checkbox']")
    checkboxes.nth(0).check()
    checkboxes.nth(1).uncheck()
    assert checkboxes.nth(0).is_checked()
    assert not checkboxes.nth(1).is_checked()


def _step_dropdown(page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.locator("#dropdown").select_option(label="Option 2")
    assert page.locator("#dropdown").input_value() == "2"


def _step_inputs(page):
    page.goto("https://the-internet.herokuapp.com/inputs")
    field = page.locator("input[type='number']")
    field.fill("999")
    assert field.input_value() == "999"


def _step_hovers(page):
    page.goto("https://the-internet.herokuapp.com/hovers")
    first_figure = page.locator(".figure").first
    first_figure.hover()
    expect(first_figure.locator(".figcaption")).to_be_visible()


def test_full_suite():
    run_full_test()