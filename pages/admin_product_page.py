from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import random
import string


class AdminProductListPage(BasePage):
    """
    PageObject для страницы списка товаров в админке
    """
    
    # Локаторы
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.h1")
    NEW_PRODUCT_BUTTON = (By.CSS_SELECTOR, "a#page-header-desc-configuration-add")
    PRODUCT_TABLE = (By.ID, "table-product")
    PRODUCT_ROWS = (By.CSS_SELECTOR, "table#table-product tbody tr")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    DELETE_BUTTON = (By.CSS_SELECTOR, "a.delete")
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, "button.confirm")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input#product_name")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button#submit_search")
    RESET_BUTTON = (By.CSS_SELECTOR, "button#submit_reset")
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
    
    def wait_for_page_load(self):
        """Дождаться загрузки страницы списка товаров"""
        self.wait.until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
    
    def click_add_new_product(self):
        """
        Нажать кнопку 'Добавить новый товар'
        :return: AdminProductFormPage
        """
        from pages.admin_product_page import AdminProductFormPage
        
        new_product_btn = self.find_clickable(self.NEW_PRODUCT_BUTTON)
        new_product_btn.click()
        
        product_form = AdminProductFormPage(self.driver, self.base_url)
        product_form.wait_for_page_load()
        return product_form
    
    def search_product(self, product_name):
        """
        Поиск товара по названию
        :param product_name: Название товара
        """
        search_input = self.find(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(product_name)
        
        search_btn = self.find_clickable(self.SEARCH_BUTTON)
        search_btn.click()
        
        # Ждем результаты поиска
        self.wait.until(
            EC.presence_of_element_located(self.PRODUCT_TABLE)
        )
    
    def get_product_count(self):
        """Получить количество товаров в таблице"""
        products = self.driver.find_elements(*self.PRODUCT_ROWS)
        return len(products)
    
    def delete_first_product(self):
        """
        Удалить первый товар из списка
        :return: True если успешно, False если нет
        """
        try:
            # Находим кнопку удаления первого товара
            delete_btn = self.find_clickable(self.DELETE_BUTTON)
            delete_btn.click()
            
            # Подтверждаем удаление в диалоговом окне
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON)
            )
            confirm_btn.click()
            
            # Ждем сообщения об успехе
            self.wait.until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
            
        except TimeoutException:
            return False
    
    def is_success_message_displayed(self):
        """Проверить, отображается ли сообщение об успехе"""
        return self.is_element_present(self.SUCCESS_MESSAGE)
    
    def get_success_message_text(self):
        """Получить текст сообщения об успехе"""
        if self.is_success_message_displayed():
            return self.find(self.SUCCESS_MESSAGE).text
        return None
    
    @staticmethod
    def generate_random_product_name(prefix="TestProduct"):
        """Сгенерировать случайное имя товара"""
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return f"{prefix}_{random_string}"


class AdminProductFormPage(BasePage):
    """
    PageObject для формы создания/редактирования товара
    """
    
    # Локаторы
    PRODUCT_NAME_INPUT = (By.ID, "name")
    PRODUCT_PRICE_INPUT = (By.ID, "price")
    PRODUCT_QUANTITY_INPUT = (By.ID, "quantity")
    PRODUCT_DESCRIPTION_INPUT = (By.ID, "description_short")
    PRODUCT_LONG_DESCRIPTION_INPUT = (By.ID, "description")
    STATUS_TOGGLE = (By.CSS_SELECTOR, "label.switch-label")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button#product_form_submit_btn")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "a#product_form_cancel_btn")
    CATEGORY_SELECTOR = (By.ID, "id_category_default")
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
    
    def wait_for_page_load(self):
        """Дождаться загрузки формы товара"""
        self.wait.until(
            EC.presence_of_element_located(self.PRODUCT_NAME_INPUT)
        )
    
    def fill_product_form(self, name, price="100.00", quantity="10", description="Test description"):
        """
        Заполнить форму создания товара
        :param name: Название товара
        :param price: Цена
        :param quantity: Количество
        :param description: Краткое описание
        """
        # Вводим название
        name_input = self.find(self.PRODUCT_NAME_INPUT)
        name_input.clear()
        name_input.send_keys(name)
        
        # Вводим цену
        price_input = self.find(self.PRODUCT_PRICE_INPUT)
        price_input.clear()
        price_input.send_keys(price)
        
        # Вводим количество
        quantity_input = self.find(self.PRODUCT_QUANTITY_INPUT)
        quantity_input.clear()
        quantity_input.send_keys(quantity)
        
        # Вводим описание
        desc_input = self.find(self.PRODUCT_DESCRIPTION_INPUT)
        desc_input.clear()
        desc_input.send_keys(description)
    
    def save_product(self):
        """
        Сохранить товар
        :return: AdminProductListPage
        """
        from pages.admin_product_page import AdminProductListPage
        
        save_btn = self.find_clickable(self.SAVE_BUTTON)
        save_btn.click()
        
        # Ждем возврата к списку товаров
        product_list = AdminProductListPage(self.driver, self.base_url)
        product_list.wait_for_page_load()
        return product_list
    
    def create_product(self, name, price="150.00", quantity="20", description="Auto created product"):
        """
        Создать товар (заполнить форму и сохранить)
        :param name: Название товара
        :param price: Цена
        :param quantity: Количество
        :param description: Описание
        :return: AdminProductListPage
        """
        self.fill_product_form(name, price, quantity, description)
        return self.save_product()