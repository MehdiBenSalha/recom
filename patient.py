import random

class Patient:
    def __init__(self):
        # clé = ID du médicament, valeur = probabilité de succès
        self.treatment_success_prob = {
            0: 0.10,
            1: 0.20,
            2: 0.15,
            3: 0.40,
            4: 0.35,
            5: 0.05,
            6: 0.25,
            7: 0.50,
            8: 0.50,
            9: 0.90
        }

    def apply_treatment(self, treatment_id):
        p = self.treatment_success_prob[treatment_id]
        return 1 if random.random() < p else 0
