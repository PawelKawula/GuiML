from learning.defined_models import learn_models
from common.file_handler import get_columns_from_csv
from common.configs.config import Config, ReadOnlyConfig
from learning.defined_models import learn_models


class GlobalMlConfig(Config):
    def set_filename(self, filename):
        self._set_value("filename", filename)

    def set_tdf(self, tdf):
        self._set_value("tdf", tdf)


class ReadOnlyGlobalMlConfig(ReadOnlyConfig):
    def get_filename(self):
        return self._get_value("filename")

    def get_tdf(self):
        return self._get_value("tdf")

    def get_learn_models(self):
        return learn_models
