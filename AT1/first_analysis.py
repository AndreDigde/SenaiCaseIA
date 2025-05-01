from ucimlrepo import fetch_ucirepo
import matplotlib.pyplot as plt

energy_efficiency = fetch_ucirepo(id=242) 

features = energy_efficiency.data.features 
targets = energy_efficiency.data.targets 

for feature in features:
    for target in targets:
        plt.figure(figsize=(12, 8))
        plt.scatter(features[feature], targets[target], alpha=0.1)
        plt.title(f'Relação: {feature} vs {target}')
        plt.xlabel(feature)
        plt.ylabel(target)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"./feature_vs_target_plots/{feature}_vs_{target}")
        plt.clf()
        plt.close()

for feature in features:
    for feature_c in features:
        if feature != feature_c:
            plt.figure(figsize=(12, 8))
            plt.scatter(features[feature], features[feature_c], alpha=0.1)
            plt.title(f'Relação: {feature} vs {feature_c}')
            plt.xlabel(feature)
            plt.ylabel(feature_c)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"./feature_vs_feature_plots/{feature}_vs_{feature_c}")
            plt.clf()
            plt.close()

