from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage(ABC):
    """Базовый класс для всех страниц с общими методами"""
    
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)  # Явное ожидание до 10 секунд
    
    def open(self, url=""):
        """Открыть страницу"""
        self.driver.get(f"{self.base_url}{url}")
    
    def find(self, locator):
        """Найти элемент с явным ожиданием видимости"""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator),
                message=f"Элемент {locator} не стал видимым за 10 секунд"
            )
        except TimeoutException:
            # Можно сделать скриншот для отладки
            self.driver.save_screenshot(f"element_not_found_{locator[1]}.png")
            raise
    
    def find_clickable(self, locator):
        """Найти кликабельный элемент"""
        try:
            return self.wait.until(
                EC.element_to_be_clickable(locator),
                message=f"Элемент {locator} не стал кликабельным за 10 секунд"
            )
        except TimeoutException:
            self.driver.save_screenshot(f"element_not_clickable_{locator[1]}.png")
            raise
    
    def is_element_present(self, locator):
        """Проверить, что элемент присутствует (без ожидания видимости)"""
        try:
            self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_text(self, locator):
        """Получить текст элемента"""
        return self.find(locator).text