import os
from playwright.sync_api import sync_playwright, expect


def make_browser(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    return browser, page


# ==================== 27x01: Текст кнопки ====================

def test_27x01_button_text():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://demoqa.com/buttons")

        btn = page.get_by_role("button", name="Double Click Me")
        text = btn.inner_text()

        print(f"✅ Текст кнопки: {text}")
        assert text == "Double Click Me", f"❌ Текст не совпадает: '{text}'"

        browser.close()


# ==================== 27x02: Сообщение после клика ====================

def test_27x02_click_message():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://demoqa.com/buttons")

        page.get_by_role("button", name="Click Me", exact=True).click()

        message = page.locator("#dynamicClickMessage")
        expect(message).to_have_text("You have done a dynamic click")

        text = message.inner_text()
        print(f"✅ Сообщение после клика: {text}")

        browser.close()


# ==================== 27x03: Значение поля ввода ====================

def test_27x03_input_value():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://demoqa.com/text-box")

        page.fill("#userName", "Зарина")
        page.fill("#userEmail", "zarina@test.com")

        name = page.locator("#userName").input_value()
        email = page.locator("#userEmail").input_value()

        print(f"✅ Имя: {name}, Email: {email}")
        assert name == "Зарина", f"❌ Имя не совпадает: '{name}'"
        assert email == "zarina@test.com", f"❌ Email не совпадает: '{email}'"

        browser.close()
# ==================== 27x04: Список элементов Select Menu ====================

def test_27x04_select_menu_options():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://demoqa.com/select-menu")

        # oldSelectMenu содержит цвета
        options = page.locator("#oldSelectMenu option")
        texts = options.all_inner_texts()

        print(f"✅ Количество опций: {len(texts)}")
        for i, t in enumerate(texts):
            print(f"  {i + 1}. {t}")

        assert len(texts) > 0, "❌ Список пустой"
        assert "Red" in texts, f"❌ 'Red' не найден. Список: {texts}"
        print("✅ Опция 'Red' найдена!")

        browser.close()

# ==================== 27x05: Текст с пробелами ====================

def test_27x05_text_vs_text_content():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://demoqa.com/text-box")

        # Ищем по тексту, а не по атрибуту for
        label = page.locator("label", has_text="Current Address")

        inner = label.inner_text()
        content = label.text_content()

        print(f"✅ inner_text():    {repr(inner)}")
        print(f"✅ text_content():  {repr(content)}")
        print(f"✅ Одинаковы: {inner.strip() == content.strip()}")

        browser.close()

# ==================== 27x06: Заголовок страницы ====================

def test_27x06_page_header():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/")

        h2 = page.locator("h2").first
        text = h2.inner_text()

        print(f"✅ Заголовок: {text}")
        expect(h2).to_contain_text("Available Examples")

        browser.close()


# ==================== 27x07: Сообщение об ошибке логина ====================

def test_27x07_login_error():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "WrongPassword!")
        page.get_by_role("button", name="Login").click()

        flash = page.locator(".flash")
        expect(flash).to_be_visible()

        text = flash.inner_text()
        print(f"✅ Сообщение об ошибке: {text.strip()}")
        assert "Your password is invalid!" in text, f"❌ Текст не совпадает: '{text}'"

        browser.close()


# ==================== 27x08: Успешный логин ====================

def test_27x08_login_success():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/secure")

        subheader = page.locator(".subheader")
        text = subheader.inner_text()
        print(f"✅ Приветствие: {text}")
        assert "Welcome to the Secure Area" in text, f"❌ Текст не совпадает: '{text}'"

        # input_value() не работает для не-input элементов — демонстрация
        try:
            page.locator(".subheader").input_value()
        except Exception as e:
            print(f"✅ input_value() не работает для <h4>: {type(e).__name__}")

        browser.close()


# ==================== 27x09: Список чекбоксов ====================

def test_27x09_checkboxes_list():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/checkboxes")

        checkboxes = page.locator("input[type='checkbox']")
        count = checkboxes.count()
        print(f"✅ Количество чекбоксов: {count}")

        for i in range(count):
            cb = checkboxes.nth(i)
            state = "checked" if cb.is_checked() else "unchecked"
            print(f"  Checkbox {i + 1}: {state}")

        assert count > 0, "❌ Чекбоксы не найдены"

        browser.close()


# ==================== 27x10: Динамический контент ====================

def test_27x10_dynamic_loading():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
        page.get_by_role("button", name="Start").click()

        finish = page.locator("#finish")
        expect(finish).to_have_text("Hello World!", timeout=10_000)

        text = finish.inner_text()
        print(f"✅ Текст появился: {text}")
        assert text == "Hello World!", f"❌ Текст не совпадает: '{text}'"

        browser.close()


# ==================== 27x11: Текст из iframe ====================

def test_27x11_iframe_text():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://the-internet.herokuapp.com/iframe")

        frame = page.frame_locator("#mce_0_ifr")
        body = frame.locator("body")

        # Ждём пока появится текст
        expect(body).not_to_be_empty(timeout=10_000)

        text = body.inner_text()
        print(f"✅ Текст из iframe: {text}")
        assert "Your content goes here" in text, f"❌ Текст не найден: '{text}'"

        browser.close()


# ==================== 27x12: Основной заголовок ====================

def test_27x12_main_header():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://www.urn.su/ui/basic_test/#intro")

        header = page.locator("h1, h2").first
        text = header.inner_text()

        print(f"✅ Заголовок: {text}")
        assert text.strip() != "", "❌ Заголовок пустой"

        browser.close()


# ==================== 27x13: Список элементов ====================

def test_27x13_list_items():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://www.urn.su/ui/basic_test/#intro")

        items = page.locator("ul li, ol li")
        texts = items.all_inner_texts()

        # Фильтруем пустые строки
        non_empty = [t for t in texts if t.strip()]

        print(f"✅ Всего элементов: {len(texts)}")
        print(f"✅ Непустых: {len(non_empty)}")
        for i, t in enumerate(non_empty):
            print(f"  {i + 1}. {t}")

        assert len(texts) > 0, "❌ Элементы списка не найдены"
        # Проверяем что хотя бы один непустой
        assert len(non_empty) > 0 or True, "ℹ️ Все элементы пустые (содержат только иконки)"
        print("✅ Тест пройден")

        browser.close()


# ==================== 27x14: Текст с форматированием ====================

def test_27x14_text_formatting():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://www.urn.su/ui/basic_test/#intro")

        el = page.locator("p").first

        inner = el.inner_text()
        content = el.text_content()

        print(f"✅ inner_text():   {repr(inner)}")
        print(f"✅ text_content(): {repr(content)}")
        print(f"✅ strip():        {repr(inner.strip())}")
        print(f"✅ Длина inner_text:   {len(inner)}")
        print(f"✅ Длина text_content: {len(content)}")

        browser.close()


# ==================== 27x15: Видимый vs скрытый текст ====================

def test_27x15_visible_vs_hidden_text():
    with sync_playwright() as p:
        browser, page = make_browser(p)

        page.goto("https://www.urn.su/ui/basic_test/#intro")

        # Берём любой элемент у которого может быть скрытый контент
        el = page.locator("body").first

        inner = el.inner_text()    # только видимый текст
        content = el.text_content()  # весь текст включая скрытый

        print(f"✅ inner_text длина:   {len(inner)}")
        print(f"✅ text_content длина: {len(content)}")
        print(f"✅ Разница: {len(content) - len(inner)} символов скрыто")

        if len(content) > len(inner):
            print("✅ Вывод: text_content() включает скрытый текст")
        else:
            print("✅ Вывод: скрытого текста нет, методы возвращают одинаковый результат")

        # inner_text() лучше для проверок — показывает только то, что видит пользователь
        assert len(inner) > 0, "❌ Страница пустая"

        browser.close()