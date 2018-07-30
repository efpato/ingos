# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui import Button, Link
from page_object.ui.jquery import Textbox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from elements import MultySelectTextbox, SearchTextbox, Slider, VariantsSlider


class KaskoCalcPage(PageObject):
    URL = "https://www.ingos.ru/ru/private/auto/kasko/calc/"
    car_fmt = "div[ng-model='vm.cxCarModel'] input[placeholder='{}']".format
    dvr_fmt = "div[ng-model='d.cxDriverModel'] input[placeholder='{}']".format

    city = SearchTextbox(css="div[city='vm.regCity.city']")
    car_brand = MultySelectTextbox(css=car_fmt("Марка автомобиля"))
    car_year = MultySelectTextbox(css=car_fmt("Год выпуска"))
    car_model = MultySelectTextbox(css=car_fmt("Модель"))
    car_transmission_type = MultySelectTextbox(css=car_fmt("Коробка передач"))
    car_engine_type = MultySelectTextbox(css=car_fmt("Тип двигателя"))
    car_modification = MultySelectTextbox(css=car_fmt("Тип кузова"))
    car_engine_model = MultySelectTextbox(css=car_fmt("Двигатель"))
    car_is_new = MultySelectTextbox(css=car_fmt(
        "Дата покупки первым собственником"))
    antitheft_system = MultySelectTextbox(css=car_fmt(
        "Противоугонный комплекс"))
    car_autostart = MultySelectTextbox(css=car_fmt("Автозапуск"))
    is_credit_car = MultySelectTextbox(css=car_fmt("Автомобиль в кредите ?"))
    add_driver = Link(link_text="+ Добавить водителя")
    driver_age = MultySelectTextbox(css=dvr_fmt("Возраст водителя"))
    driver_experience = MultySelectTextbox(css=dvr_fmt("Стаж водителя"))
    driver_sex = MultySelectTextbox(css=dvr_fmt("Пол водителя"))
    driver_is_married = MultySelectTextbox(css=dvr_fmt("Состояние в браке"))
    driver_has_children = MultySelectTextbox(css=dvr_fmt("Дети"))
    car_start_using_date = Textbox(
        css="div[ng-model='vm.CarParams.StartUsingDate'] input")
    car_price = Slider(css="div[ng-model='vm.SumSlider.value'] input")
    car_price2 = Textbox(css="input[name='price']")
    calculate = Button(css="button[ng-model='vm.isSubmitting']")
    variants = VariantsSlider(css="div[ng-model='kcc.selectedVariantNumber']")

    def car_mileage(self, value):
        if value is None:
            return

        value = str(value).strip().lower()
        if not value:
            return

        self.webdriver.execute_script(
            """
            var e = $("input[ng-model='vm.cxFormInputValue']");
            e.val({0}).change();
            e.next().next().click();
            """.format(value))

    def wait_for_calculate(self, timeout=180):
        WebDriverWait(self.webdriver, timeout).until(
            EC.visibility_of_element_located((
                By.ID, "kaskoCalculationCoverTypeSelect")),
            'Calculation timeout is expired!')
