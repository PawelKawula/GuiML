#!/usr/bin/env python

from learning.defined_models import learn_models


class SettingsModel:
    def __init__(self, learn_models=learn_models):
        self.learn_models = learn_models
