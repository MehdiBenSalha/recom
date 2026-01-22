import numpy as np

class BayesianMedicalTeam:
    """
    Thompson Sampling (Beta-Bernoulli) :
    - Pour chaque traitement i, on maintient une croyance Beta(a_i, b_i) sur p_i.
    - Chaque jour :
        1) on sample theta_i ~ Beta(a_i, b_i) pour tous les i
        2) on choisit i* = argmax(theta_i)
        3) si succès: a_i* += 1 ; sinon: b_i* += 1
    """

    def __init__(self, n_treatments: int = 10, a0: int = 1, b0: int = 1, seed: int | None = None):
        self.n_treatments = n_treatments
        self.rng = np.random.default_rng(seed)

        # paramètres Beta pour chaque traitement
        self.a = np.full(n_treatments, a0, dtype=int)
        self.b = np.full(n_treatments, b0, dtype=int)

        # historique (utile pour plots / debug)
        self.last_choice = None
        self.choices = []
        self.outcomes = []
        self.a_history = [self.a.copy()]
        self.b_history = [self.b.copy()]

    def select_treatment(self) -> int:
        """Choisit le traitement via Thompson Sampling."""
        samples = self.rng.beta(self.a, self.b)          # theta_i échantillonnés
        choice = int(np.argmax(samples))                 # meilleur sample
        self.last_choice = choice
        return choice

    def update(self, treatment_id: int, outcome: int) -> None:
        """Met à jour Beta(a,b) selon le résultat (0/1)."""
        outcome = int(outcome)
        if outcome == 1:
            self.a[treatment_id] += 1
        else:
            self.b[treatment_id] += 1

        self.choices.append(treatment_id)
        self.outcomes.append(outcome)
        self.a_history.append(self.a.copy())
        self.b_history.append(self.b.copy())

    def get_params(self):
        """Renvoie (a, b) actuels (copies)."""
        return self.a.copy(), self.b.copy()
