import copy
from typing import Self

from VegansDeluxe.core.Translator.Translator import translator


class LocalizedString:
    def __init__(self, key: str, format_queue=None):
        if format_queue is None:
            format_queue = []

        self.key = key
        self.__format_queue: list[callable] = format_queue

    def __str__(self):
        return self.localize()

    def localize(self, code: str = ""):
        if code and code not in translator.locales:
            print(f"Warning: no [{code}] locale in translator. Defaulting to [{translator.default_locale}].")
            code = translator.default_locale
        string = translator.get_string(self.key, code)
        if string is None and code != translator.default_locale:
            print(f"Warning: string [{self.key}] not found in [{code}]. Defaulting to [{translator.default_locale}].")
            string = self.localize(translator.default_locale)
        if string is None:
            print(f"Warning: string [{self.key}] not found in default locale [{translator.default_locale}]. "
                  f"Defaulting to raw key.")
            string = self.key
        for format_func in self.__format_queue:
            string = format_func(string)

        return string

    def format(self, *args, **kwargs) -> Self:
        def format_func(string: str):
            return string.format(*args, **kwargs)
        self_copy = self.copy()
        self_copy.__format_queue.append(format_func)
        return self_copy

    def copy(self) -> Self:
        return LocalizedString(self.key, self.__format_queue)


ls = LocalizedString
