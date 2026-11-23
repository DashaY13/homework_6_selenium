from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Страница каталога (например, Art)"""
    
    # Локаторы
    CATEGORY_TITLE = (By.CSS_SELECTOR, "h1.h1")
    PRODUCT_LIST = (By.CSS_SELECTOR, "div#js-product-list")
    GRID_VIEW_BUTTON = (By.CSS_SELECTOR, "button#grid")
    LIST_VIEW_BUTTON = (By.CSS_SELECTOR, "button#list")
    PAGINATION = (By.CSS_SELECTOR, "nav.pagination")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "div#products-sort-order")
    PRODUCT_COUNT = (By.CSS_SELECTOR, "p#products-count")
    BREADCRUMB = (By.CSS_SELECTOR, "nav.breadcrumb")
    FILTERS_SECTION = (By.CSS_SELECTOR, "div#search_filters")
    FIRST_PRODUCT = (By.CSS_SELECTOR, "div.product:first-child")
    
    def open_art_catalog(self):
        """Открыть каталог Art"""
        self.open("/3-art")
    
    def get_all_product_prices(self):
        """Вернуть все цены в каталоге"""
        prices = self.driver.find_elements(By.CSS_SELECTOR, "span.price")
        return [price.text for price in prices if price.text]