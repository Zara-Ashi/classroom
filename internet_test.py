from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_main_page():
    # Настройка браузера
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # 1. Открываем сайт
        driver.get("https://the-internet.herokuapp.com/")

        # 2. Проверяем заголовок страницы (title)
        page_title = driver.title
        assert "the-internet" in page_title, (
            f"❌ Ошибка: заголовок страницы не содержит 'the-internet'. "
            f"Текущий заголовок: '{page_title}'"
        )

        # 3. Находим заголовок <h1> на странице
        h1_element = driver.find_element(By.TAG_NAME, "h1")
        h1_text = h1_element.text

        assert "Available Examples" in h1_text, (
            f"❌ Ошибка: заголовок <h1> не содержит 'Available Examples'. "
            f"Текущий текст: '{h1_text}'"
        )

        # 4. Выводим результат в консоль
        print(f"✅ Сайт доступен. Заголовок: {page_title}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_main_page()