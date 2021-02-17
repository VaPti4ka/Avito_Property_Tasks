from selenium import webdriver


class Page:

    def __init__(self, driver):
        self.driver = driver

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

    def __init__(self, driver):
        super().__init__(driver)

        # Сразу переходим на страницу поиска
        self.load_page(self.PAGE_LINK)
