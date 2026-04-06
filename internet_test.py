import pytest
from playwright.sync_api import Page, expect


def test_main_page(page: Page):
    """Тест 1: Проверка главной страницы."""

    # 1. Открываем сайт
    page.goto("https://the-internet.herokuapp.com/")

    # 2. Проверяем заголовок вкладки (title)
    expect(page).to_have_title("The Internet")
    print(f"✅ Сайт доступен. Заголовок: {page.title()}")

    # 3. Проверяем заголовок <h1>
    expect(page.locator("h1")).to_have_text("Available Examples")
    print("✅ Заголовок <h1> корректен: 'Available Examples'")


def test_form_login(page: Page):
    """Тест 2: Вход через форму аутентификации."""

    # 1. Переходим на страницу входа
    page.goto("https://the-internet.herokuapp.com/login")
    print(f"📄 Открыта страница: {page.url}")

    # 2. Вводим username
    page.fill("#username", "tomsmith")
    print("✍️  Введён username: tomsmith")

    # 3. Вводим password
    page.fill("#password", "SuperSecretPassword!")
    print("✍️  Введён password: SuperSecretPassword!")

    # 4. Кликаем по кнопке Login
    page.click("button[type='submit']")
    print("🖱️  Клик по кнопке Login")

    # 5. Проверяем URL (Playwright ждёт автоматически)
    expect(page).to_have_url("https://the-internet.herokuapp.com/secure")

    path = "/" + page.url.rstrip("/").split("/")[-1]
    print(f"✅ Успешный вход! URL: {path}")