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
    parser.addoption(
        "--admin_email",
        action="store",
        default="admin@admin.com",
        help="Email администратора для логина"
    )
    parser.addoption(
        "--admin_password",
        action="store",
        default="admin123",
        help="Пароль администратора"
    )


@pytest.fixture
def base_url(request):
    """Фикстура, возвращающая базовый URL"""
    return request.config.getoption("--base_url")


@pytest.fixture
def admin_email(request):
    """Фикстура для email администратора"""
    return request.config.getoption("--admin_email")


@pytest.fixture
def admin_password(request):
    """Фикстура для пароля администратора"""
    return request.config.getoption("--admin_password")


@pytest.fixture
def driver(request):
    """Фикстура для запуска браузера"""
    browser_name = request.config.getoption("--browser")
    
    driver = None
    
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
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
    
    # Устанавливаем неявное ожидание
    driver.implicitly_wait(5)
    
    # Возвращаем driver для использования в тестах
    yield driver
    
    # После завершения теста закрываем браузер
    driver.quit()