#!/usr/bin/env python


from .decision_tree import DecisionTreeModel
from .deep_learning import DeepLearningModel
from .gradient_boosting_model import GradientBoostingModel

learn_models = {
    "Decision Tree": DecisionTreeModel,
    "Deep Learning": DeepLearningModel,
    "Gradient Boosting": GradientBoostingModel,
}
