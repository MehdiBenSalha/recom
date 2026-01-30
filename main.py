from patient import Patient
from medical_team import MedicalTeam
import matplotlib.pyplot as plt
import numpy as np

n_runs = 10
n_days = 100

all_curves = []
best_treatments = []
total_successes = []

for run in range(n_runs):
    patient = Patient()
    team = MedicalTeam(n_treatments=10, screen_trials=3, retest_trials=5, fallback_top_k=3)

    successes = 0
    curve = []

    for day in range(n_days):
        t = team.select_treatment()
        r = patient.apply_treatment(t)
        team.update(t, r)

        successes += r
        curve.append(successes)

    all_curves.append(curve)
    best_treatments.append(team.best_treatment)
    total_successes.append(successes)

    print(f"Run {run+1}: succès={successes}, best_treatment={team.best_treatment}")

# moyenne des courbes (moyenne point par point)
avg_curve = np.mean(all_curves, axis=0)

print("\nMoyenne succès total:", np.mean(total_successes))
print("Best treatments choisis:", best_treatments)

# plot
plt.figure()
plt.plot(range(1, n_days + 1), avg_curve)
plt.xlabel("Jour")
plt.ylabel("Succès cumulés moyens")
plt.title(f"Succès cumulés moyens sur {n_runs} expériences")
plt.grid(True)
plt.show()
