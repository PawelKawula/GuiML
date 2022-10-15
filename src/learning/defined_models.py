from .decision_tree_regressor import DecisionTreeRegressorModel
from .deep_learning import DeepLearningModel
from .gradient_boosting_model import GradientBoostingModel

learn_models = {
    "Decision Tree Regressor": DecisionTreeRegressorModel,
    "Gradient Boosting": GradientBoostingModel,
}
