from .decision_tree_regressor import DecisionTreeRegressorModel
from .decision_tree_classifier import DecisionTreeClassifierModel
from .deep_learning import DeepLearningModel
from .gradient_boosting_model import GradientBoostingModel

learn_models = {
    "Decision Tree Regressor": DecisionTreeRegressorModel,
    "Decision Tree Classifier": DecisionTreeClassifierModel,
    "Gradient Boosting": GradientBoostingModel,
}
