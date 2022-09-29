#!/usr/bin/env python

from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def predict(self, xs):
        pass
