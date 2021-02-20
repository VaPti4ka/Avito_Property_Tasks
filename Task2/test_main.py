import pytest
from parser_main import PropertyPage


def test_select_station_button(event):
    event.load_page(event.PAGE_LINK)
    event.open_settings()
    event.open_empty_stations_option_list()

    stations = ['Деловой центр (МЦК)', 'Международная', 'Улица академика Янгеля']
    event.select_station_for_alphabetically(stations)

    event.wait_element(event.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR)
    button_text = event.search_elem(event.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR).text

    assert (("Выбрать " in button_text) and (" станц" in button_text))

    event.load_page(event.PAGE_LINK)


def test_alphabetic_lines_switch(event):
    event.load_page(event.PAGE_LINK)
    event.open_settings()
    event.event.open_empty_stations_option_list()

    # Переключаем на выбор по алфавиту
    event.push_alphabetically_button()

    stations = ['Деловой центр (МЦК)', 'Международная', 'Улица академика Янгеля']


if __name__ == '__main__':
    test_case = PropertyPage()

    """
        6 тестов - проверка критериев приема от PO
    """
    # 1


    # 2
    test_select_station_button(test_case)

    # 3


    # 4


    # 5


    # 6
