from ucimlrepo import fetch_ucirepo
from eval_models import clear_outliers
from regression_train import train_regression, shuffle_and_split_data, save_results
from sklearn.gaussian_process import GaussianProcessRegressor
import pickle
import os

energy_efficiency = fetch_ucirepo(id=242) 
features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets
features.drop("X8", axis=1)
results = []
features_cleared, targets_cleared = clear_outliers(features, targets, 2.5, [])
x_train, x_test, y_train, y_test = shuffle_and_split_data(features, targets)
model = train_regression(GaussianProcessRegressor(), "trainned_model", 0, x_train, x_test, y_train, y_test, results)
results_path = "./results/trainned_model.csv"

if os.path.exists(results_path):
        os.remove(results_path)

save_results([["train_label, mse, rmse, mae, r2"], results], "./results/trainned_model.csv")
pickle.dump(model, open("t_model.pkl", 'wb'))
