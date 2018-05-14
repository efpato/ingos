# -*- coding: utf-8 -*-

from time import sleep

from page_object import PageElement, PageElementWrapper
from page_object.ui import Textbox
from selenium.common.exceptions import TimeoutException


AVG = '_avg_'


class MultySelectTextboxWrapper(PageElementWrapper):
    def enter_avg(self):
        self._el.parent.execute_script(
            """
            $("{0}").click();
            setTimeout(function () {{
                $("{0}").click();
                setTimeout(function () {{
                    var li = $("{0}")
                        .parent()
                        .parent()
                        .next()
                        .find('li');
                    var index = Math.floor(li.length / 2);
                    li[index].click();
                }}, 1000);
            }}, 1000);
            """.format(self._locator[1]))
        sleep(2.1)

    def enter_text(self, text):
        self._el.parent.execute_script(
            """
            $("{0}").click();
            setTimeout(function () {{
                $("{0}").val("{1}").change();
                setTimeout(function () {{
                    $("{0}")
                    .parent()
                    .parent()
                    .next()
                    .find('li')
                    .filter(function () {{
                        return $.trim($(this).text()).toLowerCase() == "{1}";
                    }})
                    .click();
                }}, 1000);
            }}, 1000);
            """.format(self._locator[1], text))
        sleep(2.1)


class MultySelectTextbox(PageElement):
    def __get__(self, instance, owner):
        return MultySelectTextboxWrapper(
            self.find(instance.webdriver), self._locator)

    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip().lower()
        if not value:
            return

        try:
            el = self.__get__(instance, instance.__class__)
        except TimeoutException:
            return

        if value == AVG:
            el.enter_avg()
        else:
            el.enter_text(value)


class SearchTextbox(PageElement):
    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__)
        instance.webdriver.execute_script(
            """
            $("{0} input").val("{1}").change();
            setTimeout(function () {{
                $("{0} div.search-select__field > div").click();
                setTimeout(function () {{
                    $("{0} div.search-select__dropdown li").first().click();
                }}, 1000);
            }}, 1000);
            """.format(self._locator[1], value))
        sleep(2.1)


class Slider(Textbox):
    def __set__(self, instance, value):
        super().__set__(instance, value)
        instance.webdriver.execute_script(
            """
            $("{}").blur();
            """.format(self._locator[1]))


class VariantsSliderWrapper(PageElementWrapper):
    @property
    def total(self):
        return self._el.find_element_by_xpath(
            ".//span[contains(@class, 'value-slider__primary-value')]").text

    @property
    def description(self):
        return self._el.find_element_by_xpath(
            ".//span[contains(@class, 'value-slider__secondary-value')]").text

    @property
    def variants(self):
        return self._el.parent.execute_script(
            """
            return $("{}").scope().$parent.kcc.calculationResults;
            """.format(self._locator[1]))


class VariantsSlider(PageElement):
    def __get__(self, instance, owner):
        return VariantsSliderWrapper(
            self.find(instance.webdriver), self._locator)
