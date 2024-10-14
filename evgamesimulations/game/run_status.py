import numpy as np
from scipy import stats

class RunStats:

    def __init__(self, _nRuns, _nSteps):
        """
        Constructor for RunStats
        Args:
            _nRuns: Number of Monte Carlo runs
            _nSteps: Number of steps in the simulation
        """

        self.numberRuns = _nRuns
        self.numberSteps = _nSteps

        # Allocate space for metrics
        self.k_I = np.zeros((_nRuns, _nSteps), dtype=int)
        self.k_T = np.zeros((_nRuns, _nSteps), dtype=int)
        self.k_U = np.zeros((_nRuns, _nSteps), dtype=int)
        self.netWealth = np.zeros((_nRuns, _nSteps), dtype=float)
        self.strategyChanges = np.zeros((_nRuns, _nSteps), dtype=int)

        self.avgk_I = np.zeros(_nSteps, dtype=float)
        self.stdk_I = np.zeros(_nSteps, dtype=float)
        self.min_k_I = np.zeros(_nSteps, dtype=float)
        self.max_k_I = np.zeros(_nSteps, dtype=float)

        self.avgk_T = np.zeros(_nSteps, dtype=float)
        self.stdk_T = np.zeros(_nSteps, dtype=float)
        self.min_k_T = np.zeros(_nSteps, dtype=float)
        self.max_k_T = np.zeros(_nSteps, dtype=float)

        self.avgk_U = np.zeros(_nSteps, dtype=float)
        self.stdk_U = np.zeros(_nSteps, dtype=float)
        self.min_k_U = np.zeros(_nSteps, dtype=float)
        self.max_k_U = np.zeros(_nSteps, dtype=float)

        self.avgnetWealth = np.zeros(_nSteps, dtype=float)
        self.stdnetWealth = np.zeros(_nSteps, dtype=float)
        self.min_netWealth = np.zeros(_nSteps, dtype=float)
        self.max_netWealth = np.zeros(_nSteps, dtype=float)

        self.avgStrategyChanges = np.zeros(_nSteps, dtype=float)
        self.stdStrategyChanges = np.zeros(_nSteps, dtype=float)
        self.min_StrategyChanges = np.zeros(_nSteps, dtype=float)
        self.max_StrategyChanges = np.zeros(_nSteps, dtype=float)

    def get_k_T(self):
        return self.k_T

    def set_k_T(self, _k_T):
        self.k_T = _k_T

    def get_strategy_changes(self):
        return self.strategyChanges

    def set_strategy_changes(self, _StrategyChanges):
        self.strategyChanges = _StrategyChanges

    def get_k_U(self):
        return self.k_U

    def set_k_U(self, _k_U):
        self.k_U = _k_U

    def calc_all_stats(self):
        """
        Calculate all statistical metrics for each step and run
        """

        for j in range(self.numberSteps):
            # Create empty lists to store the metrics for the j-th step
            statsk_I = []
            statsk_T = []
            statsk_U = []
            statsnetWealth = []
            statsStrategyChanges = []

            for i in range(self.numberRuns):
                statsk_I.append(self.k_I[i][j])
                statsk_T.append(self.k_T[i][j])
                statsk_U.append(self.k_U[i][j])
                statsnetWealth.append(self.netWealth[i][j])
                statsStrategyChanges.append(self.strategyChanges[i][j])

            # Compute statistical values for each metric
            self.avgk_I[j] = np.mean(statsk_I)
            self.stdk_I[j] = np.std(statsk_I)
            self.min_k_I[j] = np.min(statsk_I)
            self.max_k_I[j] = np.max(statsk_I)

            self.avgk_T[j] = np.mean(statsk_T)
            self.stdk_T[j] = np.std(statsk_T)
            self.min_k_T[j] = np.min(statsk_T)
            self.max_k_T[j] = np.max(statsk_T)

            self.avgk_U[j] = np.mean(statsk_U)
            self.stdk_U[j] = np.std(statsk_U)
            self.min_k_U[j] = np.min(statsk_U)
            self.max_k_U[j] = np.max(statsk_U)

            self.avgnetWealth[j] = np.mean(statsnetWealth)
            self.stdnetWealth[j] = np.std(statsnetWealth)
            self.min_netWealth[j] = np.min(statsnetWealth)
            self.max_netWealth[j] = np.max(statsnetWealth)

            self.avgStrategyChanges[j] = np.mean(statsStrategyChanges)
            self.stdStrategyChanges[j] = np.std(statsStrategyChanges)
            self.min_StrategyChanges[j] = np.min(statsStrategyChanges)
            self.max_StrategyChanges[j] = np.max(statsStrategyChanges)
