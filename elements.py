# -*- coding: utf-8 -*-

from page_object import PageElement


class ButtonElement(object):
    def __init__(self, webelement):
        self.el = webelement

    def click(self):
        self.el.parent.execute_script("arguments[0].click();", self.el)


class Input(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            value = str(value).strip()
            if value:
                self.__get__(instance, instance.__class__)
                instance.webdriver.execute_script(
                    """$("{0}").val("{1}").change();"""
                    .format(self._locator[1], value))


class Label(PageElement):
    def __get__(self, instance, owner):
        return ButtonElement(super().__get__(instance, owner))
