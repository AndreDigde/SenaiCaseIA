from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import os


_RESULT_RAW_PATH = "./raw_data_train_result.csv"

energy_efficiency = fetch_ucirepo(id=242) 
features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets


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


for index in range(10):
    x_train, x_test, y_train, y_test = shuffle_and_split_data(features, targets)
    train_linear_regression(index, x_train, x_test, y_train, y_test)
