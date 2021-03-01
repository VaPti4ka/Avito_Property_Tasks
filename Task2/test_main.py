import pytest
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
    event = PropertyPage()
    event.open_settings()
    event.open_empty_stations_option_list()

    # Выбираем станции в алфавитном списке
    stations = ['Деловой центр (МЦК)']
    event.select_station_for_alphabetically(stations)

    # Переключаемся на список по линиям и проверяем, что окрытых линий нет
    event.push_by_lines_button()
    assert len(event.search_elems(event.ALL_LINES_EXPANDED_LOCATOR)) == 0, "Есть раскрытые списки по линиям"

    # Проверяем, что выбранные станции сохранились
    assert event.get_selected_stations() == stations, "Выбранные станции не совпадают с заданными"

    event.driver.quit()


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

    event.select_station(["Улица 1905 года"], event.ALL_STATIONS_LOCATOR)
    value = event.search_elem(event.METRO_SEARCH_FIELD_LOCATOR).get_attribute('value')
    assert value == "", 'Поле для поисковой фразы не пустое'

    event.driver.quit()


def test_metro_select_field():
    station_list = ['Авиамоторная', 'Кузнецкий мост', 'Окская', 'Октябрьская', 'Петровский парк']
    event = PropertyPage()
    event.open_settings()

    metro_stations = event.search_elems(event.METRO_SELECT_VALUE_LOCATOR)

    # Станции не выбраны, ожидаемый результат - пустой список элементов
    assert metro_stations == []

    # Заходим в панель выбора станций, выбираем одну
    event.open_empty_stations_option_list()
    event.select_station_for_alphabetically(station_list[0:1])
    # Возвращаемся на экран "Уточнить"
    event.push_confirm_station_button()

    metro_stations = event.search_elems(event.METRO_SELECT_VALUE_LOCATOR)
    # Проверка, в поле выбора станций должно отобразиться название выбранной странции
    assert metro_stations[0].text == station_list[0]

    # Повторяем для 3-х выбранных станций
    event.open_complete_station_option_list()
    event.press_elem(event.DISCARD_BUTTON)
    event.select_station(station_list[0:3], event.ALL_STATIONS_LOCATOR)
    event.push_confirm_station_button()

    metro_stations = event.search_elems(event.METRO_SELECT_VALUE_LOCATOR)
    assert ("Выбрано " in metro_stations[0].text) and (" станци" in metro_stations[0].text)

    event.driver.quit()


def test_case_find_lefortovo_ads():
    stations = ['Таганская', 'Марксистская', 'Китай-город', 'Новокузнецкая', 'Третьяковская']

    event = PropertyPage()
    event.open_settings()
    event.open_empty_stations_option_list()

    # Выбрали станции
    event.select_station_for_alphabetically(stations)
    # Подтвердили выбор станций
    event.push_confirm_station_button()
    # Подтвердили настройки, попадаем на страницу результатов поиска
    event.push_confirm_setting_button()

    ad_stations_list = event.get_station_of_ad()

    for station_name in ad_stations_list:
        assert station_name in stations

    event.driver.quit()


if __name__ == '__main__':
    pass
