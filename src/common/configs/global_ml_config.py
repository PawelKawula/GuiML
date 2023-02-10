from learning.defined_models import learn_models
from common.file_handler import get_columns_from_csv
from common.configs.config import Config, ReadOnlyConfig
from learning.defined_models import learn_models


class GlobalMlConfig(Config):
    def set_filename(self, filename):
        self._set_value("filename", filename)

    def set_df(self, df):
        self._set_value("df", df)

    def set_tdf(self, tdf):
        self._set_value("tdf", tdf)

    def get_tdf(self):
        return self._get_value("tdf")

    def get_df(self):
        return self._get_value("df")


class ReadOnlyGlobalMlConfig(ReadOnlyConfig):
    def get_filename(self):
        return self._get_value("filename")

    def get_tdf(self):
        return self._get_value("tdf")

    def get_df(self):
        return self._get_value("df")

    def is_column_categorical(self, column):
        return column in self.get_tdf().cat_names

    def get_column_categories(self, column):
        df = self.get_df()
        if not self.is_column_categorical(column):
            return ["None"]
        ret = list(df[column].value_counts().index)
        print(column, "categories:", ret)
        return ret

    def get_xs_column_to_type_dict(self):
        tdf = self.get_tdf()[~self.get_tdf().items.isnull().any(axis=1)]
        res = {c: type(v) for c, v in tdf.iloc[0].items()}
        print(res)
        return res

    def get_item_from_tdf(self, y, col):
        return self.get_tdf().decode().loc[y, col]

    def get_learn_models(self):
        return learn_models
