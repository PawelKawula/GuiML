try:
    import tomllib as tomli
except ModuleNotFoundError:
    import tomli
from learning.defined_models import learn_models
import learning.defined_models

for cl in learn_models.values():
    cl.load_default()
