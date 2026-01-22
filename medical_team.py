import random

class MedicalTeam:
    """
    Stratégie :
    - Phase 1 (screening) : tester chaque traitement 3 fois.
      -> candidats = ceux à 3/3 ; si vide -> ceux à 2/3 ; si vide -> les meilleurs (top 3).
    - Phase 2 (re-test) : tester chaque candidat 5 fois.
      -> choisir le meilleur (succès max, tie-break aléatoire).
    - Phase 3 (exploitation) : appliquer le meilleur jusqu'à la fin.
    """

    def __init__(self, n_treatments=10, screen_trials=3, retest_trials=5, fallback_top_k=3):
        self.n_treatments = n_treatments
        self.screen_trials = screen_trials
        self.retest_trials = retest_trials
        self.fallback_top_k = fallback_top_k

        self.day = 0

        # Phase 1: on va tester 0,0,0,1,1,1,...,9,9,9
        self.phase = "screen"
        self.current_treatment = 0
        self.current_repeat_left = self.screen_trials

        self.screen_results = {i: 0 for i in range(n_treatments)}  # nb succès sur 3

        # Phase 2: candidats et retest
        self.candidates = []
        self.retest_queue = []
        self.retest_results = {}  # treatment -> [successes, trials]

        # Phase 3: meilleur traitement final
        self.best_treatment = None

    def select_treatment(self):
        """Retourne l'id du traitement à appliquer aujourd'hui."""
        if self.phase == "screen":
            return self.current_treatment

        if self.phase == "retest":
            # tête de queue = traitement en cours de retest
            return self.retest_queue[0]

        # exploitation
        return self.best_treatment

    def update(self, treatment_id, outcome):
        """
        Met à jour l'état après avoir reçu le résultat du patient.
        outcome: 0 ou 1
        """
        self.day += 1

        if self.phase == "screen":
            # enregistrer le succès du traitement testé
            self.screen_results[treatment_id] += int(outcome)

            # décrémenter le nombre de répétitions restantes pour ce traitement
            self.current_repeat_left -= 1

            # si on a fini les 3 essais pour ce traitement, passer au suivant
            if self.current_repeat_left == 0:
                self.current_treatment += 1
                self.current_repeat_left = self.screen_trials

                # si on a terminé les 10 traitements -> déterminer candidats et passer en retest
                if self.current_treatment >= self.n_treatments:
                    self._build_candidates_from_screen()
                    self._start_retest_phase()

        elif self.phase == "retest":
            t = self.retest_queue[0]
            self.retest_results[t][0] += int(outcome)  # successes
            self.retest_results[t][1] += 1             # trials

            # si on a fait assez de jours de retest pour ce candidat -> pop
            if self.retest_results[t][1] >= self.retest_trials:
                self.retest_queue.pop(0)

                # si plus rien à retester -> choisir le meilleur et passer en exploitation
                if not self.retest_queue:
                    self.best_treatment = self._choose_best_from_retest()
                    self.phase = "exploit"

        else:
            # phase exploit : rien de spécial à mettre à jour pour ta stratégie
            pass

    def _build_candidates_from_screen(self):
        # 1) candidats = 3/3
        self.candidates = [t for t, s in self.screen_results.items() if s == self.screen_trials]

        # 2) si vide => 2/3
        if not self.candidates:
            self.candidates = [t for t, s in self.screen_results.items() if s == self.screen_trials - 1]

        # 3) si toujours vide => fallback: top K par nombre de succès (tie-break random)
        if not self.candidates:
            items = list(self.screen_results.items())  # (t, successes)
            random.shuffle(items)  # tie-break aléatoire
            items.sort(key=lambda x: x[1], reverse=True)
            self.candidates = [t for t, _ in items[: self.fallback_top_k]]

    def _start_retest_phase(self):
        self.phase = "retest"
        self.retest_queue = list(self.candidates)  # on va retester chaque candidat 5 jours d’affilée
        self.retest_results = {t: [0, 0] for t in self.candidates}  # [successes, trials]

    def _choose_best_from_retest(self):
        # choisir le traitement avec le + de succès sur 5 (tie-break random)
        items = [(t, self.retest_results[t][0]) for t in self.candidates]
        random.shuffle(items)
        items.sort(key=lambda x: x[1], reverse=True)
        print("Traitement choisi après retest:", items[0][0], "avec", items[0][1], "succès sur 5")
        return items[0][0]
