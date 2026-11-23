import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def pytest_addoption(parser):
    """Добавляем кастомные опции командной строки"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Выбор браузера: chrome, firefox или edge"
    )
    parser.addoption(
        "--base_url",
        action="store",
        default="http://localhost",
        help="Базовый URL PrestaShop (например: http://localhost:8080)"
    )


@pytest.fixture
def base_url(request):
    """Фикстура, возвращающая базовый URL из параметров командной строки"""
    return request.config.getoption("--base_url")


@pytest.fixture
def driver(request):
    """Фикстура для запуска браузера с возможностью выбора"""
    browser_name = request.config.getoption("--browser")
    
    driver = None
    
    if browser_name == "chrome":
        options = ChromeOptions()
        # Добавляем опции для стабильной работы (опционально)
        options.add_argument("--start-maximized")  # Открыть на весь экран
        options.add_argument("--disable-notifications")  # Отключить уведомления
        options.add_argument("--no-sandbox")  # Для работы в контейнерах
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Браузер '{browser_name}' не поддерживается")
    
    # Устанавливаем неявное ожидание на случай, если явное не сработает
    driver.implicitly_wait(5)
    
    # Возвращаем driver для использования в тестах
    yield driver
    
    # После завершения теста закрываем браузер
    driver.quit()