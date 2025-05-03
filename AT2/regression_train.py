from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import zscore
import numpy as np
import os


_EMPTY_CSV_LINE = ",,,,"
_LR_STRING = "LinearRegression"
_SVR_STRING = "SVR"
_GPR_STRING = "GaussianProcessRegressor"
_MLPR_STRING = "MLPRegressor"
_RFR_STRING = "RandomForestRegressor"


def clear_outliers(features, targets, zsc_threshold):
    rows_to_remove = set()

    for feature in features:
        for value in features[feature].unique():
            rows_mask = features[feature] == value
            filtered_indices = features[rows_mask].index

            for target_i in range(2):
                target_values = targets.iloc[filtered_indices, target_i]
                zsc = zscore(target_values)

                for i, z in enumerate(zsc):
                    if abs(z) > zsc_threshold: 
                        outlier_index = filtered_indices[i]
                        rows_to_remove.add(outlier_index)

    log = f"Outliers removed (threshold {zsc_threshold}): {len(rows_to_remove)}"
    return features.drop(index=rows_to_remove), targets.drop(index=rows_to_remove), log


def shuffle_and_split_data(features, targets):
    return train_test_split(features, targets, test_size=0.2, shuffle=True)


def model_evaluation(y_predicted, y_test):
    mse = mean_squared_error(y_test, y_predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_predicted)
    r2 = r2_score(y_test, y_predicted)
    return mse, rmse, mae, r2


def trains_eval_mean(train_name, results):
    means = [train_name]

    for index in range(1, 5):
        means.append(float(np.mean([row[index] for row in results])))
    
    return means


def trains_eval_std(train_name, results):
    std = [train_name]

    for index in range(1, 5):
        std.append(float(np.std([row[index] for row in results])))
    
    return std


def save_results(results_set, results_path):
    file_string = ""

    for results in results_set:
        for result in results:
            for value in result:
                file_string = f"{file_string}{value}" if type(value) == str else f"{file_string},{value:.5f}"
            
            file_string = f"{file_string}\r\n"

    with open(results_path, "a") as file:
        file.write(file_string)


def train_regression(model, train_name, train_index, x_train, x_test, y_train, y_test, results):
    model.fit(x_train, y_train)
    pred_result = model.predict(x_test)
    mse, rmse, mae, r2 = model_evaluation(pred_result, y_test)
    results.append([f"{train_name}_{train_index}", mse, rmse, mae, r2])
    return model


def run_regressions(features, targets, results_path, iterations):
    lr_results = []
    svr_results = []
    gpr_results = []
    mlpr_results = []
    rfr_results = []

    for index in range(iterations):
        x_train, x_test, y_train, y_test = shuffle_and_split_data(features, targets)
        train_regression(LinearRegression(), _LR_STRING, index, x_train, x_test, y_train, y_test, lr_results)
        train_regression(MultiOutputRegressor(SVR()), _SVR_STRING, index, x_train, x_test, y_train, y_test, svr_results)
        train_regression(GaussianProcessRegressor(), _GPR_STRING, index, x_train, x_test, y_train, y_test, gpr_results)
        train_regression(MLPRegressor(), _MLPR_STRING, index, x_train, x_test, y_train, y_test, mlpr_results)
        train_regression(RandomForestRegressor(), _RFR_STRING, index, x_train, x_test, y_train, y_test, rfr_results)

    if os.path.exists(results_path):
        os.remove(results_path)

    save_results([["train_label, mse, rmse, mae, r2"], lr_results, svr_results, gpr_results, mlpr_results, rfr_results, [_EMPTY_CSV_LINE]], results_path)
    save_results([["train_label, mse_mean, rmse_mean, mae_mean, r2_mean"], 
                    [trains_eval_mean(_LR_STRING, lr_results)],
                    [trains_eval_mean(_SVR_STRING, svr_results)],
                    [trains_eval_mean(_GPR_STRING, gpr_results)],
                    [trains_eval_mean(_MLPR_STRING, mlpr_results)],
                    [trains_eval_mean(_RFR_STRING, rfr_results)],
                    [_EMPTY_CSV_LINE]], results_path)
    save_results([["train_label, mse_std, rmse_std, mae_std, r2_std"], 
                    [trains_eval_std(_LR_STRING, lr_results)],
                    [trains_eval_std(_SVR_STRING, svr_results)],
                    [trains_eval_std(_GPR_STRING, gpr_results)],
                    [trains_eval_std(_MLPR_STRING, mlpr_results)],
                    [trains_eval_std(_RFR_STRING, rfr_results)]], results_path)
