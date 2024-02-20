import optuna

def objective(trial):
    x = trial.suggest_float('x', -30, 30)
    return (x - 2) ** 2

study = optuna.create_study()
study.optimize(objective, n_trials=1000)

study.best_params