from ucimlrepo import fetch_ucirepo
from eval_models import clear_outliers
from regression_train import train_regression, shuffle_and_split_data, save_results
from sklearn.gaussian_process import GaussianProcessRegressor
import pickle
import os

_RESULTS_PATH = "./results/trainned_model.csv"

energy_efficiency = fetch_ucirepo(id=242) 
features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets
results = []
features_cleared, targets_cleared = clear_outliers(features, targets, 2.5, [])
x_train, x_test, y_train, y_test = shuffle_and_split_data(features, targets)
model = train_regression(GaussianProcessRegressor(), "trainned_model", 0, x_train, x_test, y_train, y_test, results)

if os.path.exists(_RESULTS_PATH):
        os.remove(_RESULTS_PATH)

save_results([["train_label, mse, rmse, mae, r2"], results], _RESULTS_PATH)
pickle.dump(model, open("t_model.pkl", 'wb'))
