from ucimlrepo import fetch_ucirepo
from regression_train import run_regressions, clear_outliers
from scipy.stats import zscore


_RESULTS_PATH = "./results"

energy_efficiency = fetch_ucirepo(id=242) 
features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets
iterations = 100
logs = []

run_regressions(features, targets, f"{_RESULTS_PATH}/raw_data_train_result.csv", iterations)
run_regressions(features.drop("X1", axis=1), targets, f"{_RESULTS_PATH}/drop_x1_train_result.csv", iterations)
run_regressions(features.drop("X6", axis=1), targets, f"{_RESULTS_PATH}/drop_x6_train_result.csv", iterations)
run_regressions(features.drop("X8", axis=1), targets, f"{_RESULTS_PATH}/drop_x8_train_result.csv", iterations)

for threshold in [2.5, 3]:
    features_cleared, targets_cleared, outliers_report = clear_outliers(features, targets, threshold)
    logs.append(outliers_report)
    run_regressions(features_cleared, targets_cleared, f"{_RESULTS_PATH}/threshold_{f"{threshold}".replace(".", "_")}_train_result.csv", iterations)
    run_regressions(features_cleared.drop("X1", axis=1), targets_cleared, f"{_RESULTS_PATH}/threshold_{f"{threshold}".replace(".", "_")}_drop_x1_train_result.csv", iterations)
    run_regressions(features_cleared.drop("X6", axis=1), targets_cleared, f"{_RESULTS_PATH}/threshold_{f"{threshold}".replace(".", "_")}_drop_x6_train_result.csv", iterations)
    run_regressions(features_cleared.drop("X8", axis=1), targets_cleared, f"{_RESULTS_PATH}/threshold_{f"{threshold}".replace(".", "_")}_drop_x8_train_result.csv", iterations)

logs_string = "\r\n".join(logs)
with open("outlier_report.txt", "w") as file:
        file.write(logs_string)
