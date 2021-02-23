# import pytest
from parser_main import PropertyPage


def test_select_station_button():
    event = PropertyPage()
    event.open_settings()
    event.open_empty_stations_option_list()

    stations = ['Деловой центр (МЦК)', 'Международная', 'Улица академика Янгеля']
    event.select_station_for_alphabetically(stations)

    event.wait_element(event.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR)
    button_text = event.search_elem(event.CONFIRM_STATION_SELECTION_BUTTON_LOCATOR).text

    assert (("Выбрать " in button_text) and (" станц" in button_text))

    event.driver.quit()


def test_alphabetic_by_lines_switch():
    event = PropertyPage()
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

    event.driver.quit()


def test_select_in_lines():
    pass


def test_discard_button():
    event = PropertyPage()
    event.open_settings()
    event.open_empty_stations_option_list()

    # Проверяем включена ли кнопка
    status = event.get_discard_button_status()
    assert status is False, 'Кнопка "Сбросить" активна, когда нет выбранных станций'

    # Выбираем станцию
    event.select_station_for_alphabetically(['Коломенская'])

    # Проверяем, появилась ли возможность нажать кнопку
    status = event.get_discard_button_status()
    assert status is True, 'Кнопка "Сбросить" не активна, когда ест выбранные странциии'

    event.driver.quit()


def test_search():
    event = PropertyPage()
    event.open_settings()
    event.open_empty_stations_option_list()

    # Ищем станцию через строку поиска
    station_request = "1905"
    event.search_station(station_request)
    search_field = event.search_elem(event.METRO_SEARCH_FIELD_LOCATOR)
    assert search_field.get_attribute('value') == station_request, \
        'Поле для поисковой фразы пустое, должно содержать "{}"'.format(station_request)

    event.select_station(["Улица 1905 года"])
    value = event.search_elem(event.METRO_SEARCH_FIELD_LOCATOR).get_attribute('value')
    assert value == "", 'Поле для поисковой фразы не пустое'

    event.driver.quit()


def test_metro_select_field():
    pass


if __name__ == '__main__':
    """
        6 тестов - проверка критериев приема от PO
    """
    # 1 Переключение между выбором по-алфавиту и по-линии не сбрасывает выбор
    # test_alphabetic_by_lines_switch()

    # 2 При выборе станций снизу выезжает плавающая кнопка "Выбрать N станций"
    # test_select_station_button()

    # 3 При выборе станции из алфавитного списка, выбор дублируется внутри линии, при этом линия не разворачивается
    # test_select_in_lines()

    # 4 Кнопка "Сбросить" появляется только при выбранных станциях
    # Кнопка есть всегда, критерий приема изменен на "Кнопка активируется..."
    # test_discard_button()

    # 5 При выборе станции через поисковую строку, поиск закрывается (выдается список всех станций)
    test_search()

    # 6 На экране "Уточнить", примененный фильтр отображается с формулировкой "Выбрано n станций"
    # При выборе одной станции выводится ее название - считается правильным поведением
    # test_metro_select_field()
