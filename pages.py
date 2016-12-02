# -*- coding: utf-8 -*-

import logging
from functools import wraps

from page_object import PageObject, PageElements
from page_object.elements import Button, Link, Select
from selenium.webdriver.support.wait import WebDriverWait

from elements import Label, Input


WAIT_TIMEOUT = 20


def safe(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        logging.debug("==> %s (args=%s, kwargs=%s)",
                      fn.__name__, args, kwargs)
        try:
            fn(*args, **kwargs)
        except:
            logging.warning("%s --> autoselect", fn.__name__)

    return wrapped


class KaskoCalcPage(PageObject):
    URL = "https://www.ingos.ru/ru/private/auto/kasko/calc/"

    car_brand = Select(xpath="//div[@id='CarBrandsPanel']/div/select")

    # Параметры автомобиля
    car_is_new = Label(css="label[for='isCarNew-Y']")
    car_is_mileage = Label(css="label[for='isCarNew-N']")
    car_mileage = Input(css="input#carMileage")
    car_using_start_date = Input(css="input#KaskoCarUsingStartDate")
    car_night_parking_type_1 = Label(css="label[for='night1']")
    car_night_parking_type_2 = Label(css="label[for='night2']")
    is_credit_car_yes = Label(css="label[for='credit-y']")
    is_credit_car_no = Label(css="label[for='credit-n']")
    car_autostart_yes = Label(css="label[for='auto-y']")
    car_autostart_no = Label(css="label[for='auto-n']")
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

    variants = PageElements(css="ul#KaskoVariants li")
    variant_info = PageElements(css="ul#kaskoCalculationVariantInfo li")

    # Расчет скидки
    discount_sizepj = Label(css="label[for='TP_DISCOUNTSIZEPJ']")

    calculate = Button(id="calculateButton")

    @property
    def car_min_price(self):
        return int(self.webdriver.execute_script(
            "return $('input#KaskoMinCarPrice').val();"))

    @property
    def car_max_price(self):
        return int(self.webdriver.execute_script(
            "return $('input#KaskoMaxCarPrice').val();"))

    def city(self, value):
        def predicat(driver):
            return driver.find_element_by_id("ui-id-1").value_of_css_property(
                "display") == "block" and len(driver.find_elements_by_xpath(
                    "//ul[@id='ui-id-1']/li")) > 0

        self.webdriver.find_element_by_id(
            "kaskoCityIsn").send_keys(value)

        WebDriverWait(self.webdriver, 10).until(
            predicat, "Cities list timeout expired")

        self.webdriver.find_elements_by_xpath(
            "//ul[@id='ui-id-1']/li")[0].click()

    def _label(self, panel_id, value):
        return Label(xpath=('//div[@id="%s"]/ul/li/div/'
                            'label[contains(text(), "%s")]' %
                            (panel_id, value))).__get__(self, self.__class__)

    def _label_avg(self, panel_id):
        labels = PageElements(xpath="//div[@id='%s']/ul/li/div/label" %
                              panel_id).__get__(self, self.__class__)
        index = int(round((len(labels) / 2.0)))
        return labels[index]

    @safe
    def car_model(self, value):
        self._label("CarModelsPanel", value).click()

    @safe
    def car_year(self, value):
        if value:
            value = int(value)

            labels = PageElements(
                xpath=('//div[@id="CarManifacturingYearsPanel"]'
                       '/ul/li/div/label')).__get__(self, self.__class__)
            years = [int(label.text) for label in labels]

            for i, year in enumerate(years):
                if value == year:
                    labels[i].click()
                    return

            min_year = min(years)
            max_year = max(years)
            if value < min_year:
                labels[years.index(min_year)].click()
            elif value > max_year:
                labels[years.index(max_year)].click()
            else:
                raise ValueError("Couldn't resolve year: %s" % value)

    @safe
    def car_engine_model(self):
        self._label_avg("CarEngineModelsPanel").click()

    @safe
    def car_modification(self):
        self._label_avg("CarModificationsPanel").click()

    @safe
    def car_transmission_type(self, value):
        self._label("CarTransmissionTypesPanel", value).click()

    def is_credit_car(self, value):
        if value:
            value = str(value).strip()
            if value.lower() == "да":
                self.is_credit_car_yes.click()
            elif value.lower() == "нет":
                self.is_credit_car_no.click()
            else:
                raise RuntimeError(
                    'Invalid value for "is_credit_car": "%s"' % value)

    def car_night_parking_type(self, value):
        if value:
            value = str(value).strip()
            if value == "Охраняемая стоянка / Гараж":
                self.car_night_parking_type_1.click()
            elif value == "Иное":
                self.car_night_parking_type_2.click()
            else:
                raise RuntimeError(
                    'Invalid value for "car_night_parking_type": "%s"' % value)

    def car_autostart(self, value):
        if value:
            value = str(value).strip()
            if value.lower() == "да":
                self.car_autostart_yes.click()
            elif value.lower() == "нет":
                self.car_autostart_no.click()
            else:
                raise RuntimeError(
                    'Invalid value for "car_autostart": "%s"' % value)

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
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until(
            lambda driver: driver.find_element_by_id(
                "carAdditionalDataSpinner").value_of_css_property(
                    "display") == "none",
            "Loader timeout expired")

    def wait_calculation(self):
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until(
            lambda driver: driver.find_element_by_id(
                "spinnerStep1").value_of_css_property("display") == "none",
            "Calculation timeout expired")

    @property
    def has_franchise(self):
        return self.webdriver.execute_script(
            """
            return (function () {{
                var o = $('input#kaskoIncludeFranchise1');
                return o.is(':visible') && o.is(':checked');
            }})();
            """)

    @property
    def franchise_value(self):
        return self.webdriver.execute_script(
            """
            return $("select#KaskoFranchise1Limits option").filter(
                ':selected').text();
            """)

    @property
    def result(self):
        return self.webdriver.find_element_by_id(
            "kaskoBottomResultProductDescription").text.split(':')[1]

    @property
    def errors(self):
        errors = self.webdriver.find_elements_by_xpath(
            "//ul[@class='errors-list']/li")
        return "\n".join([error.text for error in errors])
