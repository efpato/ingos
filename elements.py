# -*- coding: utf-8 -*-

from page_object import PageElement


class Input(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            value = str(value).strip()
            if value:
                self.__get__(instance, instance.__class__)
                instance.webdriver.execute_script(
                    """$("{0}").val("{1}").change();"""
                    .format(self._locator[1], value))
