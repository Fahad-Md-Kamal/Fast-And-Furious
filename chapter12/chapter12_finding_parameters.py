from sklearn.datasets import load_digits
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

digits = load_digits()

data = digits.data
targets = digits.target

# Create the grid fo parameters
param_grid = {
    "C": [1, 10, 100, 1000],
    "kernel": ["linear", "poly", "rbf", "sigmoid"]
}
grid = GridSearchCV(SVC(), param_grid)

grid.fit(data, targets)

print("Best Params", grid.best_params_)
print("Best Score", grid.best_score_)