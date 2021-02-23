# import pytest
from parser_main import PropertyPage


def test_select_station_button():
    event = PropertyPage()
    event.load_page(event.PAGE_LINK)
    event.open_settings()
    event.open_empty_stations_option_list()

    stations = ['Деловой центр (МЦК)', 'Международная', 'Улица академика Янгеля']
    event.select_station_for_alphabetically(stations)

    event.wait_element(event.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR)
    button_text = event.search_elem(event.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR).text

    assert (("Выбрать " in button_text) and (" станц" in button_text))

    event.load_page(event.PAGE_LINK)


def test_alphabetic_by_lines_switch():
    event = PropertyPage()
    event.load_page(event.PAGE_LINK)
    event.open_settings()
    event.open_empty_stations_option_list()

    # Переключаем на выбор по алфавиту
    event.push_alphabetically_button()

    stations = ['Деловой центр (МЦК)', 'Международная', 'Улица академика Янгеля']

    # Выбираем несколько станций
    event.select_station_for_alphabetically(stations)

    # Получаем список выбранных станций на данный момент
    selected_stations_list = event.get_selected_stations()
    # Делаем проверку, что изначальных список станций и те, что выбраны сейчас, совпадают
    assert stations == selected_stations_list, "Выбранные станции отличаются от ожидаемых\n" \
                                               "Ожидалось:\t" + str(stations) + \
                                               "Получили:\t" + str(selected_stations_list)

    # Переключаемся на вкладку "По линиям"
    event.push_by_lines_button()

    # Повторяем проверку выбранных станций
    selected_stations_list = event.get_selected_stations()
    # Делаем проверку, что изначальных список станций и те, что выбраны сейчас, совпадают
    assert stations == selected_stations_list, "Выбранные станции отличаются от ожидаемых\n" \
                                               "Ожидалось:\t" + str(stations) + \
                                               "Получили:\t" + str(selected_stations_list)


if __name__ == '__main__':
    """
        6 тестов - проверка критериев приема от PO
    """
    # 1 Переключение между выбором по-алфавиту и по-линии не сбрасывает выбор
    test_alphabetic_by_lines_switch()

    # 2 При выборе станций снизу выезжает плавающая кнопка "Выбрать N станций"
    test_select_station_button()

    # 3 При выборе станции из алфавитного списка, выбор дублируется внутри линии, при этом линия не разворачивается

    # 4 Кнопка "Сбросить" появляется только при выбранных станциях

    # 5 При выборе станции через поисковую строку, поиск закрывается (выдается список всех станций)

    # 6 На экране "Уточнить", примененный фильтр отображается с формулировкой "Выбрано n станций"
    # При выборе одной станции выводится ее название - считается правильным поведением
