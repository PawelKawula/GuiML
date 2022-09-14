#!/usr/bin/env python3

import pandas as pd


def get_table(filename):
    csv = pd.read_csv(filename)
    csv = csv.iloc[:, :10].append(csv["SalePrice"]).dropna()
    print(csv.columns)


get_table("train.csv")
