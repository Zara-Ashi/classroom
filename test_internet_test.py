from playwright.sync_api import sync_playwright


def test_main_page():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
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


def test_navigate_to_example():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/")

        page.get_by_text("Form Authentication").click()
        current_url = page.url

        assert "/login" in current_url, (
            f"❌ URL не содержит '/login'. Текущий: '{current_url}'"
        )
        print(f"✅ Перешли в: Form Authentication | URL: {current_url}")

        browser.close()


def test_login_form():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")

        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.get_by_role("button", name="Login").click()

        page.wait_for_url("**/secure")
        assert "/secure" in page.url, (
            f"❌ URL не содержит '/secure'. Текущий: '{page.url}'"
        )
        print(f"✅ Успешный вход! URL: {page.url}")

        # Выход — используем get_by_role("link") чтобы не попасть на <h4>
        page.get_by_role("link", name="Logout").click()
        page.wait_for_url("**/login")

        assert "/login" in page.url, (
            f"❌ URL не содержит '/login'. Текущий: '{page.url}'"
        )
        print(f"✅ Успешный выход! URL: {page.url}")

        browser.close()


def test_checkboxes():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Переходим в раздел Checkboxes
        page.goto("https://the-internet.herokuapp.com/checkboxes")

        # 2. Находим оба чекбокса
        checkboxes = page.locator("input[type='checkbox']")
        checkbox1 = checkboxes.nth(0)
        checkbox2 = checkboxes.nth(1)

        # 3. Проверяем начальное состояние
        assert not checkbox1.is_checked(), "❌ Checkbox 1 должен быть НЕ отмечен изначально"
        assert checkbox2.is_checked(),     "❌ Checkbox 2 должен быть отмечен изначально"
        print("✅ Начальное состояние верно: Checkbox1=False, Checkbox2=True")

        # 4. Отмечаем Checkbox 1
        checkbox1.check()

        # 5. Снимаем Checkbox 2
        checkbox2.uncheck()

        # 6. Проверяем финальное состояние
        assert checkbox1.is_checked(),     "❌ Checkbox 1 должен быть отмечен"
        assert not checkbox2.is_checked(), "❌ Checkbox 2 должен быть НЕ отмечен"

        # 7. Выводим результат
        print(f"✅ Checkbox 1: checked={checkbox1.is_checked()}")
        print(f"✅ Checkbox 2: checked={checkbox2.is_checked()}")

        browser.close()


def test_dropdown():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()


        page.goto("https://the-internet.herokuapp.com/dropdown")


        dropdown = page.locator("#dropdown")


        initial = dropdown.input_value()
        assert initial == "", (
            f"❌ Начальное значение должно быть пустым. Текущее: '{initial}'"
        )
        print(f"✅ Начальное значение пустое: '{initial}'")


        dropdown.select_option(label="Option 1")


        selected = dropdown.input_value()
        assert selected == "1", (
            f"❌ Должно быть выбрано 'Option 1'. Текущее: '{selected}'"
        )
        print(f"✅ Выбрано: Option 1")


        dropdown.select_option(label="Option 2")


        selected = dropdown.input_value()
        assert selected == "2", (
            f"❌ Должно быть выбрано 'Option 2'. Текущее: '{selected}'"
        )


        print(f"✅ Выбрано: Option 2")

        browser.close()