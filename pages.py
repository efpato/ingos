# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.elements import Button, Link, Select
from selenium.webdriver.support.wait import WebDriverWait

from elements import Input


Label = Link


class KaskoCalcPage(PageObject):
    URL = "https://www.ingos.ru/ru/private/auto/kasko/calc/"

    city_mos = Link(id="kaskoCityMos")
    city_sp = Link(id="kaskoCitySP")
    city_nn = Link(id="kaskoCityNN")
    city = Input(id="kaskoCityIsn")

    # Параметры автомобиля
    car_is_new = Label(css="label[for='isCarNew-Y']")
    car_is_mileage = Label(css="label[for='isCarNew-N']")
    car_mileage = Input(css="input#carMileage")
    car_using_start_date = Input(css="input#KaskoCarUsingStartDate")
    car_price = Input(css="input#KaskoAvgCarPrice")
    antitheft_included = Label(css="label[for='antitheft1']")
    antitheft_other = Label(css="label[for='antitheft2']")
    antitheft_system_models = Select(css="select#KaskoAntitheftSystemModels")
    insure_additional_equipment = Label(
        css="label[for='KaskoInsureAdditionalEquipment']")
    audio_equipment_sum = Input(css="input#AudioEquipmentSum")
    other_equipment_sum = Input(css="input#OtherEquipmentSum")

    # Данные о лицах, допущенных к управлению
    multi_drive = Label(css="label[for='tp_MultiDrive']")
    multi_drive_light = Label(css="label[for='tp_MultiDriveLight']")
    add_usage_driver = Link(id="cmdAddUsageDriverTemplate")

    # Параметры страхового полиса
    date_begin = Input(css="input#KaskoAgrDateBeg")

    # Расчет скидки
    discount_sizepj = Label(css="label[for='TP_DISCOUNTSIZEPJ']")

    calculate = Button(id="calculateButton")

    def _label(self, panel_id, value):
        return Label(xpath=("//div[@id='%s']/ul/li/div/"
                            "label[contains(text(), '%s')]" %
                            (panel_id, value))).__get__(self, self.__class__)

    def car_brand(self, value):
        return self._label("CarBrandsPanel", value)

    def car_model(self, value):
        return self._label("CarModelsPanel", value)

    def car_year(self, value):
        return self._label("CarManifacturingYearsPanel", value)

    def car_engine_model(self, value):
        return self._label("CarEngineModelsPanel", value)

    def car_modification(self, value):
        return self._label("CarModificationsPanel", value)

    def car_transmission_type(self, value):
        return self._label("CarTransmissionTypesPanel", value)

    def is_credit_car(self, value):
        return self._label("CarIsCreditCarPanel", value)

    def car_night_parking_type(self, value):
        return self._label("CarNightParkingTypePanel", value)

    def car_autostart(self, value):
        return self._label("CarAutostartPanel", value)

    def driver_age(self, index, value):
        return Input(css="input#KaskoDriverAge%d" % index).__set__(
            self, value)

    def driver_experience_years(self, index, value):
        return Input(css="input#KaskoDriverExperienceYears%d" % index).__set__(
            self, value)

    def driver_sex_male(self, index):
        return Label(xpath=("//input[@name='KaskoDrivers[%d].Sex' "
                            "and @value='1']/../label") %
                     index).__get__(self, self.__class__)

    def driver_sex_female(self, index):
        return Label(xpath=("//input[@name='KaskoDrivers[%d].Sex' "
                            "and @value='2']/../label") %
                     index).__get__(self, self.__class__)

    def driver_has_children_yes(self, index):
        return Label(xpath=("//input[@name='KaskoDrivers[%d].HasChildren' "
                            "and @value='1']/../label") %
                     index).__get__(self, self.__class__)

    def driver_has_children_no(self, index):
        return Label(xpath=("//input[@name='KaskoDrivers[%d].HasChildren' "
                            "and @value='2']/../label") %
                     index).__get__(self, self.__class__)

    def driver_is_married_yes(self, index):
        return Label(xpath=("//input[@name='KaskoDrivers[%d].IsMarried' "
                            "and @value='0']/../label") %
                     index).__get__(self, self.__class__)

    def driver_is_married_no(self, index):
        return Label(xpath=("//input[@name='KaskoDrivers[%d].IsMarried' "
                            "and @value='1']/../label") %
                     index).__get__(self, self.__class__)

    def wait_hide_loader(self):
        WebDriverWait(self.webdriver, 10).until(
            lambda driver: "none" == driver.find_element_by_id(
                "carAdditionalDataSpinner").value_of_css_property("display"),
            "Loader timeout expired")

    def wait_calculation(self):
        WebDriverWait(self.webdriver, 10).until(
            lambda driver: "none" == driver.find_element_by_id(
                "spinnerStep1").value_of_css_property("display"),
            "Calculation timeout expired")

    @property
    def result(self):
        value = self.webdriver.find_element_by_id(
            "kaskoBottomResultProductDescription").text.split(':')[1]
        return float(value.replace(' ', '').replace(',', '.'))

    @property
    def errors(self):
        errors = self.webdriver.find_elements_by_xpath(
            "//ul[@class='errors-list']/li")
        return "\n".join([error.text for error in errors])
