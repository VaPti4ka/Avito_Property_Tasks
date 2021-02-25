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
        # Указываем с какого девайса просматривается сайт
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

    def search_elems(self, locator):
        return self.driver.find_elements(*locator)

    def get_page_url(self):
        return self.driver.current_url

    def press_elem(self, locator):
        elem = self.driver.find_element(*locator)
        elem.click()
        return elem

    def go_page_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")


class PropertyPage(Page):
    PAGE_LINK = "https://m.avito.ru/moskva/kommercheskaya_nedvizhimost?cd=1"
    SETTINGS_BUTTON_LOCATOR = (By.XPATH, "//div[@data-marker = 'search-bar/filter']")
    EMPTY_STATION_LIST_BUTTON_LOCATOR = (By.XPATH, "//div[@data-marker = 'metro-select/withoutValue']")
    COMPLETE_STATION_LIST_BUTTON_LOCATOR = (By.XPATH, "//div[@data-marker = 'metro-select/withValue']")
    CONFIRM_STATION_SELECTION_BUTTON_LOCATOR = (By.XPATH, "//button[@data-marker = 'metro-select-dialog/apply']")
    EXIT_FROM_STATION_SELECTION_BUTTON_LOCATOR = (By.XPATH, "//div[@class='css-c98ymr']")
    ALL_STATIONS_XPATH = (By.XPATH, "//label[@data-marker='metro-select-dialog/stations/item']/span/span")
    ALL_LINES_HIDDEN_XPATH = (By.XPATH, '//div[@data-marker="metro-select-dialog/lines"]/div/button/span')
    ALL_LINES_EXPANDED_XPATH = (By.XPATH, '//div[@data-marker="metro-select-dialog/lines/expanded"]/div/button/span')
    ALL_STATIONS_IN_LINE_XPATH = (By.XPATH, '//div[@data-marker="metro-select-dialog/lines/expanded"]//'
                                            'label[@data-marker="metro-select-dialog/lines/station"]/span/span')

    ALPHABETICALLY_STATION_SELECT_BUTTON = \
        (By.XPATH, "//button[@data-marker='metro-select-dialog/tabs/button(stations)']")

    ALL_SELECTED_STATION_LOCATOR = (By.XPATH, '//div[@class = "css-8yg80d"]')

    BY_LINES_STATION_SELECT_BUTTON = \
        (By.XPATH, '//button[@data-marker = "metro-select-dialog/tabs/button(lines)"]')

    DISCARD_BUTTON = (By.XPATH, "//button[@data-marker='metro-select-dialog/reset']")
    METRO_SEARCH_FIELD_LOCATOR = (By.XPATH, '//input[@data-marker="metro-select-dialog/search"]')
    METRO_SELECT_VALUE_LOCATOR = (By.XPATH, '//span[@data-marker = "metro-select/value"]')

    def __init__(self):
        super().__init__()

        self.load_page(self.PAGE_LINK)

    """
        
        В функциях, где нажимается кнопка, добавленны ожидания подгрузки wait_element(self, locator) элементов
        Необходимо, тк часто происходит, что страница не успевает загрузиться до автоматического нажатия
        
    """

    def wait_element(self, locator):
        WebDriverWait(self.driver, 50).until(es.visibility_of_element_located(locator))

    # def get_stations_dict(self):
    #     self.push_alphabetically_button()
    #     stations = self.search_elems(self.ALL_STATIONS_XPATH)
    #
    #     stations_dict = {}
    #     # Пробегаемся по полученному списку, для каждой станции получаем название и добавляем в глобальный словарь
    #     for station in stations:
    #         station_label = station.text
    #         stations_dict[station_label] = station
    #
    #     return stations_dict

    def open_settings(self):
        self.wait_element(self.SETTINGS_BUTTON_LOCATOR)
        self.press_elem(self.SETTINGS_BUTTON_LOCATOR)

    def open_empty_stations_option_list(self):
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

    def select_station(self, stations_list, locator):
        for station in stations_list:
            xpath = locator[1]
            xpath += '[contains(text(), \'{station_name}\')]'.format(station_name=station)
            self.press_elem((By.XPATH, xpath))

    def push_alphabetically_button(self):
        self.wait_element(self.ALPHABETICALLY_STATION_SELECT_BUTTON)
        self.go_page_top()
        self.press_elem(self.ALPHABETICALLY_STATION_SELECT_BUTTON)

    def select_station_for_alphabetically(self, station_list):
        self.push_alphabetically_button()
        self.select_station(station_list, self.ALL_STATIONS_XPATH)

    def push_by_lines_button(self):
        self.wait_element(self.BY_LINES_STATION_SELECT_BUTTON)
        self.go_page_top()
        self.press_elem(self.BY_LINES_STATION_SELECT_BUTTON)

    def expand_line(self, line):
        xpath = self.ALL_LINES_HIDDEN_XPATH
        xpath += '[contains(text(), "{line_name}")]'.format(line_name=line)
        self.wait_element((By.XPATH, xpath))
        self.press_elem((By.XPATH, xpath))
        return xpath

    # request -> [(line1, (station1, station2)), (line2, (station3, station4, station5))]
    def select_station_by_lines(self, request):
        self.push_by_lines_button()
        for line in request:
            self.expand_line(line[0])
            self.select_station(line[1], self.ALL_STATIONS_IN_LINE_XPATH)

    def get_selected_stations(self):
        return [station.text for station in self.search_elems(self.ALL_SELECTED_STATION_LOCATOR)]

    def get_discard_button_status(self):
        button = self.search_elem(self.DISCARD_BUTTON)
        return button.is_enabled()

    def search_station(self, request):
        self.wait_element(self.METRO_SEARCH_FIELD_LOCATOR)
        search_field = self.search_elem(self.METRO_SEARCH_FIELD_LOCATOR)
        search_field.click()
        search_field.send_keys(request)


if __name__ == '__main__':
    case = PropertyPage()
    case.open_settings()
    case.open_empty_stations_option_list()
    stations = ['Деловой центр (МЦК)', 'Международная', 'Улица академика Янгеля']
    case.select_station_for_alphabetically(stations)
    selected_stations = case.get_selected_stations()
    pass

    time.sleep(20)
    case.driver.quit()
