from patient import Patient
from medical_team import MedicalTeam
import matplotlib.pyplot as plt

patient = Patient()
team = MedicalTeam(n_treatments=10, screen_trials=3, retest_trials=7, fallback_top_k=3)

successes = 0
curve = []

for day in range(100):
    t = team.select_treatment()
    r = patient.apply_treatment(t)
    team.update(t, r)

    successes += r
    curve.append(successes)

print("Succès total:", successes)
print("team.best_treatment:", team.best_treatment)


import matplotlib.pyplot as plt

plt.figure()
plt.plot(range(1, 101), curve)
plt.xlabel("Jour")
plt.ylabel("Nombre de succès cumulés")
plt.title("Succès cumulés au cours des 100 jours")
plt.grid(True)
plt.show()
