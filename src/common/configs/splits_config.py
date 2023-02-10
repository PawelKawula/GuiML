from collections import Mapping

from common.configs.config import Config, ReadOnlyConfig


class SplitsConfig(Config):
    def set_validation_split_method(self, method):
        self._set_value("validation_split_method", method)

    def set_pct(self, pct):
        self._set_value("pct", pct)

    def set_ins(self, ins):
        self._set_value("ins", ins)

    def set_out(self, out):
        self._set_value("out", out)

    def set_render(self, render):
        self._set_value("render", render)


class ReadOnlySplitsConfig(ReadOnlyConfig):
    def get_validation_split_method(self):
        return self._get_value("validation_split_method")

    def get_pct(self):
        return self._get_value("pct")

    def get_ins(self):
        return self._get_value("ins")

    def get_ins(self):
        return self._get_value("ins")

    def get_out(self):
        return self._get_value("out")

    def get_render(self):
        return self._get_value("render")
