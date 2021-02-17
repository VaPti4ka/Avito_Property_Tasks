from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as es

import time


class Page:

    def __init__(self):
        """
            Фичу проверяем в мобильной версии, для этого настраиваем
        """
        # Указываем с какого девайся просматривается сайт
        mobile_emulation = {"deviceName": "iPhone X"}
        # Говорим о том, что будем использовать мобильную версию
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        # Создаем driver с настройками
        self.driver = webdriver.Chrome(options=chrome_options)

    def load_page(self, page_url):
        self.driver.get(page_url)

    def search_elem(self, locator):
        return self.driver.find_element(*locator)

    def get_page_url(self):
        return self.driver.current_url

    def press_elem(self, locator):
        elem = self.driver.find_element(*locator)
        elem.click()
        return elem


class PropertyPage(Page):
    PAGE_LINK = "https://m.avito.ru/moskva/kommercheskaya_nedvizhimost?cd=1"
    SETTINGS_BUTTON_LOCATOR = (By.XPATH, "//div[@data-marker = 'search-bar/filter']")
    EMPTY_STATION_LIST_BUTTON_LOCATOR = (By.XPATH, "//div[@data-marker = 'metro-select/withoutValue']")
    COMPLETE_STATION_LIST_BUTTON_LOCATOR = (By.XPATH, "//div[@data-marker = 'metro-select/withValue']")
    CONFIRM_STATION_SELECTION_BUTTON_LOCATOR = (By.XPATH, "//button[@data-marker = 'metro-select-dialog/apply']")
    EXIT_FROM_STATION_SELECTION_BUTTON_LOCATOR = (By.XPATH, "//button[@data-marker='metro-select-dialog/back']")

    def __init__(self):
        super().__init__()

        # Сразу переходим на страницу поиска
        self.load_page(self.PAGE_LINK)

    """
        
        В функциях, где нажимается кнопка, добавленны ожидания подгрузки wait_element(self, locator) элементов
        Необходимо, тк часто происходит, что страница не успевает загрузиться до автоматического нажатия
        
    """
    def wait_element(self, locator):
        WebDriverWait(self.driver, 50).until(es.visibility_of_element_located(locator))

    def open_settings(self):
        self.wait_element(self.SETTINGS_BUTTON_LOCATOR)
        self.press_elem(self.SETTINGS_BUTTON_LOCATOR)

    def open_empty_station_option_list(self):
        self.wait_element(self.EMPTY_STATION_LIST_BUTTON_LOCATOR)
        self.press_elem(self.EMPTY_STATION_LIST_BUTTON_LOCATOR)

    def open_complete_station_option_list(self):
        self.wait_element(self.COMPLETE_STATION_LIST_BUTTON_LOCATOR)
        self.press_elem(self.COMPLETE_STATION_LIST_BUTTON_LOCATOR)

    def confirm_station_selection(self):
        self.wait_element(self.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR)
        self.press_elem(self.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR)

    def exit_from_station_selection(self):
        self.wait_element(self.EXIT_FROM_STATION_SELECTION_BUTTON_LOCATOR)
        self.press_elem(self.EXIT_FROM_STATION_SELECTION_BUTTON_LOCATOR)


if __name__ == '__main__':
    case = PropertyPage()
    case.open_settings()
    case.open_empty_station_option_list()

    # Чтобы окно само закрывалось через паузу
    time.sleep(20)
    case.driver.quit()
