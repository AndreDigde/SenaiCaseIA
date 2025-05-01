from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import os


_RESULT_RAW_PATH = "./raw_data_train_result.csv"

def shuffle_and_split_data(features, targets):
    return train_test_split(features, targets, test_size=0.2, shuffle=True)


def save_results(train_label, mse, rmse, mae, r2):
    rows = []

    if not os.path.exists(_RESULT_RAW_PATH):
            rows.append("train_label, mse, rmse, mae, r2")
    
    rows.append(f"{train_label}, {mse}, {rmse}, {mae}, {r2}")
    with open(_RESULT_RAW_PATH, "a") as file:
            for row in rows:
                file.write(f'{row}\r\n')


def train_linear_regression(train_index ,x_train, x_test, y_train, y_test):
    model = LinearRegression()
    model.fit(x_train, y_train)
    pred_result = model.predict(x_test)
    mse = mean_squared_error(y_test, pred_result)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, pred_result)
    r2 = r2_score(y_test, pred_result)
    save_results(f"LinearRegression_{train_index}", mse, rmse, mae, r2)


def train_SVR(train_index ,x_train, x_test, y_train, y_test):
    model = MultiOutputRegressor(SVR())
    model.fit(x_train, y_train)
    pred_result = model.predict(x_test)
    mse = mean_squared_error(y_test, pred_result)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, pred_result)
    r2 = r2_score(y_test, pred_result)
    save_results(f"SVR_{train_index}", mse, rmse, mae, r2)


def train_SGD_regression(train_index ,x_train, x_test, y_train, y_test):
    model = MultiOutputRegressor(SGDRegressor())
    model.fit(x_train, y_train)
    pred_result = model.predict(x_test)
    mse = mean_squared_error(y_test, pred_result)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, pred_result)
    r2 = r2_score(y_test, pred_result)
    save_results(f"SGD_{train_index}", mse, rmse, mae, r2)


def train_MLP_regression(train_index ,x_train, x_test, y_train, y_test):
    model = MLPRegressor()
    model.fit(x_train, y_train)
    pred_result = model.predict(x_test)
    mse = mean_squared_error(y_test, pred_result)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, pred_result)
    r2 = r2_score(y_test, pred_result)
    save_results(f"MLP_{train_index}", mse, rmse, mae, r2)


def train_random_forest_regression(train_index ,x_train, x_test, y_train, y_test):
    model = RandomForestRegressor()
    model.fit(x_train, y_train)
    pred_result = model.predict(x_test)
    mse = mean_squared_error(y_test, pred_result)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, pred_result)
    r2 = r2_score(y_test, pred_result)
    save_results(f"RandomForest_{train_index}", mse, rmse, mae, r2)


energy_efficiency = fetch_ucirepo(id=242) 
features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets

if os.path.exists(_RESULT_RAW_PATH):
    os.remove(_RESULT_RAW_PATH)

for index in range(10):
    x_train, x_test, y_train, y_test = shuffle_and_split_data(features, targets)
    train_linear_regression(index, x_train, x_test, y_train, y_test)
    train_SVR(index, x_train, x_test, y_train, y_test)
    train_SGD_regression(index, x_train, x_test, y_train, y_test)
    train_MLP_regression(index, x_train, x_test, y_train, y_test)
    train_random_forest_regression(index, x_train, x_test, y_train, y_test)
