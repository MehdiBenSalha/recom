from patient import Patient
from bayesian_team import BayesianMedicalTeam

patient = Patient()
team = BayesianMedicalTeam(n_treatments=10, seed=42)

successes = 0
curve = []

for day in range(100):
    t = team.select_treatment()
    r = patient.apply_treatment(t)
    team.update(t, r)

    successes += r
    curve.append(successes)

print("Succès total :", successes)
print("Traitement le plus choisi (sur 100 jours) :", max(set(team.choices), key=team.choices.count))
print("Dernier traitement choisi :", team.last_choice)
import matplotlib.pyplot as plt

plt.figure()
plt.plot(range(1, 101), curve)
plt.xlabel("Jour")
plt.ylabel("Succès cumulés")
plt.title("Thompson Sampling - Succès cumulés sur 100 jours")
plt.grid(True)
plt.show()


import numpy as np
import matplotlib.pyplot as plt

a_hist = np.array(team.a_history)  # (101, 10)
b_hist = np.array(team.b_history)  # (101, 10)
mean_hist = a_hist / (a_hist + b_hist)

plt.figure()
for i in range(mean_hist.shape[1]):
    plt.plot(range(mean_hist.shape[0]), mean_hist[:, i], label=f"T{i}")
plt.xlabel("Jour")
plt.ylabel("Moyenne Beta (a/(a+b))")
plt.title("Évolution des croyances (moyenne) - Thompson Sampling")
plt.grid(True)
plt.legend()
plt.show()
