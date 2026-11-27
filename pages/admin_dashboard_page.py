from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    """
    PageObject для дашборда администратора PrestaShop
    """
    
    # Локаторы для элементов дашборда
    DASHBOARD_TITLE = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_ICON = (By.CSS_SELECTOR, "a#header_logout")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.logout")
    CATALOG_MENU = (By.ID, "subtab-AdminCatalog")
    PRODUCTS_LINK = (By.ID, "subtab-AdminProducts")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input#bo_query")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button#bo_search_submit")
    
    # Локаторы для бокового меню
    SIDEBAR = (By.ID, "nav-sidebar")
    DASHBOARD_LINK = (By.LINK_TEXT, "Dashboard")
    ORDERS_LINK = (By.LINK_TEXT, "Orders")
    CUSTOMERS_LINK = (By.LINK_TEXT, "Customers")
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
    
    def wait_for_page_load(self):
        """Дождаться загрузки дашборда"""
        self.wait.until(
            EC.presence_of_element_located(self.DASHBOARD_TITLE)
        )
    
    def navigate_to_products(self):
        """
        Перейти в раздел управления товарами
        :return: AdminProductListPage
        """
        from pages.admin_product_page import AdminProductListPage
        
        # Сначала раскрываем меню Catalog
        catalog_menu = self.find_clickable(self.CATALOG_MENU)
        catalog_menu.click()
        
        # Ждем появления подменю и кликаем на Products
        self.wait.until(
            EC.visibility_of_element_located(self.PRODUCTS_LINK)
        )
        products_link = self.find_clickable(self.PRODUCTS_LINK)
        products_link.click()
        
        # Возвращаем страницу списка товаров
        product_list = AdminProductListPage(self.driver, self.base_url)
        product_list.wait_for_page_load()
        return product_list
    
    def logout(self):
        """
        Выполнить выход из админки
        :return: AdminLoginPage
        """
        from pages.admin_login_page import AdminLoginPage
        
        # Находим и кликаем по иконке пользователя
        user_icon = self.find_clickable(self.USER_ICON)
        user_icon.click()
        
        # Кликаем по кнопке logout
        logout_btn = self.find_clickable(self.LOGOUT_BUTTON)
        logout_btn.click()
        
        # Возвращаем страницу логина
        login_page = AdminLoginPage(self.driver, self.base_url)
        login_page.wait_for_page_load()
        return login_page
    
    def is_logged_in(self):
        """Проверить, что мы в админке (залогинены)"""
        return self.is_element_present(self.DASHBOARD_TITLE)