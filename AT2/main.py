from ucimlrepo import fetch_ucirepo
from regression_train import run_regressions
from scipy.stats import zscore
import numpy as np
import pandas as pd


def clear_outliers(features, targets, zsc_trashold, logs):
    rows_to_remove = set()

    for feature in features:
        for value in features[feature].unique():
            rows_mask = features[feature] == value
            filtered_indices = features[rows_mask].index

            for target_i in range(2):
                target_values = targets.iloc[filtered_indices, target_i]
                zsc = zscore(target_values)

                for i, z in enumerate(zsc):
                    if abs(z) > zsc_trashold: 
                        outlier_index = filtered_indices[i]
                        rows_to_remove.add(outlier_index)

    log = f"Outliners removed (trashold {zsc_trashold}): {len(rows_to_remove)}"
    logs.append(log)
    return features.drop(index=rows_to_remove), targets.drop(index=rows_to_remove)


energy_efficiency = fetch_ucirepo(id=242) 
features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets
logs = []

run_regressions(features, targets, "./raw_data_train_result.csv")

for trashold in [2.5, 3]:
    features_cleared, targets_cleared = clear_outliers(features, targets, trashold, logs)
    run_regressions(features, targets, f"./trashold_{f"{trashold}".replace(".", "_")}_train_result.csv")

logs_string = '\r\n'.join(logs)
with open("report.txt", "w") as file:
        file.write(logs_string)
