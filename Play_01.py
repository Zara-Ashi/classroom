from playwright.sync_api import sync_playwright


def main_page(url: str, browser_type: str = "chromium", headless: bool = False) -> dict:

    with sync_playwright() as p:

        browser_launcher = getattr(p, browser_type)
        browser = browser_launcher.launch(headless=headless)

        page = browser.new_page()
        page.goto(url)

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

        result = {
            "url": url,
            "browser": browser_type,
            "title": title,
            "h1": h1,
            "h2": h2,
            "success": True,
        }

        browser.close()
        return result


def navigate_to_example(example_name: str, browser_type: str = "chromium", headless: bool = False) -> str:

    with sync_playwright() as p:

        browser_launcher = getattr(p, browser_type)
        browser = browser_launcher.launch(headless=headless)

        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/")

        page.get_by_text(example_name).click()

        current_url = page.url

        browser.close()
        return current_url


def login_form(browser_type: str = "chromium", headless: bool = False) -> str:

    with sync_playwright() as p:

        browser_launcher = getattr(p, browser_type)
        browser = browser_launcher.launch(headless=headless)

        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")

        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")

        page.get_by_role("button", name="Login").click()

        current_url = page.url

        assert "/secure" in current_url, (
            f"❌ URL не содержит '/secure'. Текущий: '{current_url}'"
        )

        browser.close()
        return current_url


if __name__ == "__main__":
    data = main_page(url="https://the-internet.herokuapp.com/", browser_type="chromium", headless=False)
    print(f"✅ Сайт доступен. Заголовок: {data['title']}")
    print(f"h1: {data['h1']}")
    print(f"h2: {data['h2']}")

    url = navigate_to_example("Form Authentication")
    assert "/login" in url, f"❌ URL не содержит '/login'. Текущий: '{url}'"
    print(f"✅ Перешли в: Form Authentication | URL: {url}")

    login_url = login_form()
    print(f"✅ Успешный вход! URL: {login_url}")