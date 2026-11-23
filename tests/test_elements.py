import pytest
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


class TestPageElements:
    """Проверка наличия элементов на ключевых страницах"""
    
    def test_main_page_elements(self, driver, base_url):
        """
        Тест: На главной странице присутствуют все ключевые элементы
        Проверяем: лого, поиск, корзину, популярные товары, футер
        """
        page = MainPage(driver, base_url)
        page.open_main_page()
        
        # Проверяем 5+ элементов с явными ожиданиями
        assert page.is_element_present(page.LOGO), "Логотип отсутствует"
        assert page.is_element_present(page.SEARCH_INPUT), "Поле поиска отсутствует"
        assert page.is_element_present(page.CART_ICON), "Иконка корзины отсутствует"
        assert page.is_element_present(page.POPULAR_PRODUCTS), "Блок популярных товаров отсутствует"
        assert page.is_element_present(page.FOOTER), "Футер отсутствует"
        assert page.is_element_present(page.CONTACT_LINK), "Ссылка 'Контакты' отсутствует"
    
    def test_catalog_page_elements(self, driver, base_url):
        """
        Тест: В каталоге Art присутствуют все элементы
        Проверяем: заголовок категории, список товаров, пагинацию, сортировку, хлебные крошки
        """
        page = CatalogPage(driver, base_url)
        page.open_art_catalog()
        
        assert page.is_element_present(page.CATEGORY_TITLE), "Заголовок категории отсутствует"
        assert page.is_element_present(page.PRODUCT_LIST), "Список товаров отсутствует"
        assert page.is_element_present(page.PAGINATION), "Пагинация отсутствует"
        assert page.is_element_present(page.SORT_DROPDOWN), "Выпадающее меню сортировки отсутствует"
        assert page.is_element_present(page.BREADCRUMB), "Хлебные крошки отсутствуют"
        assert page.is_element_present(page.FILTERS_SECTION), "Секция фильтров отсутствует"
    
    def test_product_page_elements(self, driver, base_url):
        """
        Тест: На странице товара присутствуют все элементы
        Проверяем: название, цену, описание, кнопку "В корзину", изображения
        """
        page = ProductPage(driver, base_url)
        page.open_product()  # Откроем первый товар в каталоге Art
        
        assert page.is_element_present(page.PRODUCT_NAME), "Название товара отсутствует"
        assert page.is_element_present(page.PRODUCT_PRICE), "Цена товара отсутствует"
        assert page.is_element_present(page.ADD_TO_CART_BUTTON), "Кнопка 'В корзину' отсутствует"
        assert page.is_element_present(page.PRODUCT_IMAGES), "Изображения товара отсутствуют"
        assert page.is_element_present(page.PRODUCT_REFERENCE), "Артикул товара отсутствует"
    
    def test_admin_login_page_elements(self, driver, base_url):
        """
        Тест: На странице логина админки присутствуют все элементы
        Проверяем: форму логина, поля email/password, кнопку входа, лого
        """
        page = LoginPage(driver, base_url)
        page.open_login_page()
        
        assert page.is_element_present(page.LOGIN_FORM), "Форма логина отсутствует"
        assert page.is_element_present(page.EMAIL_INPUT), "Поле Email отсутствует"
        assert page.is_element_present(page.PASSWORD_INPUT), "Поле Password отсутствует"
        assert page.is_element_present(page.LOGIN_BUTTON), "Кнопка логина отсутствует"
        assert page.is_element_present(page.LOGO_IMAGE), "Логотип отсутствует"
        assert page.is_element_present(page.LANGUAGE_SELECTOR), "Селектор языка отсутствует"
    
    def test_registration_page_elements(self, driver, base_url):
        """
        Тест: На странице регистрации присутствуют все элементы
        Проверяем: поля ввода, чекбоксы, кнопку регистрации
        """
        page = RegistrationPage(driver, base_url)
        page.open_registration_page()
        
        assert page.is_element_present(page.FIRST_NAME_INPUT), "Поле 'Имя' отсутствует"
        assert page.is_element_present(page.LAST_NAME_INPUT), "Поле 'Фамилия' отсутствует"
        assert page.is_element_present(page.EMAIL_INPUT), "Поле 'Email' отсутствует"
        assert page.is_element_present(page.PASSWORD_INPUT), "Поле 'Пароль' отсутствует"
        assert page.is_element_present(page.GDPR_CHECKBOX), "Чекбокс GDPR отсутствует"
        assert page.is_element_present(page.SUBMIT_BUTTON), "Кнопка 'Сохранить' отсутствует"