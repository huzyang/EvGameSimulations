import numpy as np

"""
RunStats class:
    This class will store all the results for the MonteCarlo simulation.
    It will also update the stats and error metrics w.r.t. the historical data.

"""

class RunStats:

    def __init__(self):
        """constructor of RunStats"""
        self.number_runs = 0  # number of MC simulations
        self.number_steps = 0  # number of steps in the simulation

        # fields for k_I members of the population (time series)
        # Fields for the k_I members of the population (time series)
        self.k_I = []  # all the k_I members (each for run and step)
        self.avg_k_I = []  # average k_I over all the runs for each step
        self.std_k_I = []  # std k_I over all the runs for each step
        self.min_k_I = []  # min k_I over all the runs for each step
        self.max_k_I = []  # max k_I over all the runs for each step

        # fields for k_T members of the population (time series)
        self.k_T = []  # all the k_T members (each for run and step)
        self.avg_k_T = []  # average k_T over all the runs for each step
        self.std_k_T = []  # std k_T over all the runs for each step
        self.min_k_T = []  # min k_T over all the runs for each step
        self.max_k_T = []  # max k_T over all the runs for each step

        # fields for k_U members of the population (time series)
        self.k_U = []  # all the k_U members (each for run and step)
        self.avg_k_U = []  # average k_U over all the runs for each step
        self.std_k_U = []  # std k_U over all the runs for each step
        self.min_k_U = []  # min k_U over all the runs for each step
        self.max_k_U = []  # max k_U over all the runs for each step

        # fields for netWealth
        self.net_wealth = []  # all the netWealth metrics (each for run and step)
        self.avg_net_wealth = []  # average netWealth over all the runs for each step
        self.std_net_wealth = []  # std netWealth over all the runs for each step
        self.min_net_wealth = []  # min netWealth over all the runs for each step
        self.max_net_wealth = []  # max netWealth over all the runs for each step

        # fields for changes in the agents' strategies
        # Fields for strategy changes of agents
        self.strategy_changes = []  # the number of strategy changes in the agents (each for run and step)
        self.avg_strategy_changes = []  # average of strategy changes over all the runs for each step
        self.std_strategy_changes = []  # std of strategy changes over all the runs for each step
        self.min_strategy_changes = []  # min of strategy changes over all the runs for each step
        self.max_strategy_changes = []  # max of strategy changes over all the runs for each step

        self.exp_name = ""  # the key name of this experiment (all the MC runs)

    # ================================================
    # Methods/Functions
    # ================================================

    def calc_all_stats(self):
        """
        This method is for calculating all the statistical information 
        for the runs of the metrics.
        """
        for j in range(self.number_steps):
            # TODO Get a DescriptiveStatistics instance

            # Temporary storage for each metric
            k_I_stats = [self.k_I[i][j] for i in range(self.number_runs)]
            k_T_stats = [self.k_T[i][j] for i in range(self.number_runs)]
            k_U_stats = [self.k_U[i][j] for i in range(self.number_runs)]
            net_wealth_stats = [self.net_wealth[i][j] for i in range(self.number_runs)]
            strategy_changes_stats = [self.strategy_changes[i][j] for i in range(self.number_runs)]

            # Calculating mean, standard deviation, min, and max for k_I
            self.avg_k_I.append(np.mean(k_I_stats))
            self.std_k_I.append(np.std(k_I_stats))
            self.min_k_I.append(min(k_I_stats))
            self.max_k_I.append(max(k_I_stats))

            # Calculating mean, standard deviation, min, and max for k_T
            self.avg_k_T.append(np.mean(k_T_stats))
            self.std_k_T.append(np.std(k_T_stats))
            self.min_k_T.append(min(k_T_stats))
            self.max_k_T.append(max(k_T_stats))

            # Calculating mean, standard deviation, min, and max for k_U
            self.avg_k_U.append(np.mean(k_U_stats))
            self.std_k_U.append(np.std(k_U_stats))
            self.min_k_U.append(min(k_U_stats))
            self.max_k_U.append(max(k_U_stats))

            # Calculating mean, standard deviation, min, and max for net wealth
            self.avg_net_wealth.append(np.mean(net_wealth_stats))
            self.std_net_wealth.append(np.std(net_wealth_stats))
            self.min_net_wealth.append(min(net_wealth_stats))
            self.max_net_wealth.append(max(net_wealth_stats))

            # Calculating mean, standard deviation, min, and max for strategy changes
            self.avg_strategy_changes.append(np.mean(strategy_changes_stats))
            self.std_strategy_changes.append(np.std(strategy_changes_stats))
            self.min_strategy_changes.append(min(strategy_changes_stats))
            self.max_strategy_changes.append(max(strategy_changes_stats))


    # ===================================================
    # Getters and setters
    # ===================================================
    # Getter and setter methods for number_runs
    def get_number_runs(self):
        return self.number_runs

    def set_number_runs(self, number_runs):
        self.number_runs = number_runs

    # Getter and setter methods for number_steps
    def get_number_steps(self):
        return self.number_steps

    def set_number_steps(self, number_steps):
        self.number_steps = number_steps

    # Getter and setter methods for k_I
    def get_k_I(self):
        return self.k_I

    def set_k_I(self, k_I):
        self.k_I = k_I

    # Getter and setter methods for avg_k_I
    def get_avg_k_I(self):
        return self.avg_k_I

    def set_avg_k_I(self, avg_k_I):
        self.avg_k_I = avg_k_I

    # Getter and setter methods for std_k_I
    def get_std_k_I(self):
        return self.std_k_I

    def set_std_k_I(self, std_k_I):
        self.std_k_I = std_k_I

    # Getter and setter methods for min_k_I
    def get_min_k_I(self):
        return self.min_k_I

    def set_min_k_I(self, min_k_I):
        self.min_k_I = min_k_I

    # Getter and setter methods for max_k_I
    def get_max_k_I(self):
        return self.max_k_I

    def set_max_k_I(self, max_k_I):
        self.max_k_I = max_k_I

    # Getter and setter methods for k_T
    def get_k_T(self):
        return self.k_T

    def set_k_T(self, k_T):
        self.k_T = k_T

    # Getter and setter methods for avg_k_T
    def get_avg_k_T(self):
        return self.avg_k_T

    def set_avg_k_T(self, avg_k_T):
        self.avg_k_T = avg_k_T

    # Getter and setter methods for std_k_T
    def get_std_k_T(self):
        return self.std_k_T

    def set_std_k_T(self, std_k_T):
        self.std_k_T = std_k_T

    # Getter and setter methods for min_k_T
    def get_min_k_T(self):
        return self.min_k_T

    def set_min_k_T(self, min_k_T):
        self.min_k_T = min_k_T

    # Getter and setter methods for max_k_T
    def get_max_k_T(self):
        return self.max_k_T

    def set_max_k_T(self, max_k_T):
        self.max_k_T = max_k_T

    # Getter and setter methods for k_U
    def get_k_U(self):
        return self.k_U

    def set_k_U(self, k_U):
        self.k_U = k_U

    # Getter and setter methods for avg_k_U
    def get_avg_k_U(self):
        return self.avg_k_U

    def set_avg_k_U(self, avg_k_U):
        self.avg_k_U = avg_k_U

    # Getter and setter methods for std_k_U
    def get_std_k_U(self):
        return self.std_k_U

    def set_std_k_U(self, std_k_U):
        self.std_k_U = std_k_U

    # Getter and setter methods for min_k_U
    def get_min_k_U(self):
        return self.min_k_U

    def set_min_k_U(self, min_k_U):
        self.min_k_U = min_k_U

    # Getter and setter methods for max_k_U
    def get_max_k_U(self):
        return self.max_k_U

    def set_max_k_U(self, max_k_U):
        self.max_k_U = max_k_U

    # Getter and setter methods for net_wealth
    def get_net_wealth(self):
        return self.net_wealth

    def set_net_wealth(self, net_wealth):
        self.net_wealth = net_wealth

    # Getter and setter methods for avg_net_wealth
    def get_avg_net_wealth(self):
        return self.avg_net_wealth

    def set_avg_net_wealth(self, avg_net_wealth):
        self.avg_net_wealth = avg_net_wealth

    # Getter and setter methods for std_net_wealth
    def get_std_net_wealth(self):
        return self.std_net_wealth

    def set_std_net_wealth(self, std_net_wealth):
        self.std_net_wealth = std_net_wealth

    # Getter and setter methods for min_net_wealth
    def get_min_net_wealth(self):
        return self.min_net_wealth

    def set_min_net_wealth(self, min_net_wealth):
        self.min_net_wealth = min_net_wealth

    # Getter and setter methods for max_net_wealth
    def get_max_net_wealth(self):
        return self.max_net_wealth

    def set_max_net_wealth(self, max_net_wealth):
        self.max_net_wealth = max_net_wealth

    # Getter and setter methods for strategy_changes
    def get_strategy_changes(self):
        return self.strategy_changes

    def set_strategy_changes(self, strategy_changes):
        self.strategy_changes = strategy_changes

    # Getter and setter methods for avg_strategy_changes
    def get_avg_strategy_changes(self):
        return self.avg_strategy_changes

    def set_avg_strategy_changes(self, avg_strategy_changes):
        self.avg_strategy_changes = avg_strategy_changes

    # Getter and setter methods for std_strategy_changes
    def get_std_strategy_changes(self):
        return self.std_strategy_changes

    def set_std_strategy_changes(self, std_strategy_changes):
        self.std_strategy_changes = std_strategy_changes

    # Getter and setter methods for min_strategy_changes
    def get_min_strategy_changes(self):
        return self.min_strategy_changes

    def set_min_strategy_changes(self, min_strategy_changes):
        self.min_strategy_changes = min_strategy_changes

    # Getter and setter methods for max_strategy_changes
    def get_max_strategy_changes(self):
        return self.max_strategy_changes

    def set_max_strategy_changes(self, max_strategy_changes):
        self.max_strategy_changes = max_strategy_changes

    # Getter and setter methods for exp_name
    def get_exp_name(self):
        return self.exp_name

    def set_exp_name(self, exp_name):
        self.exp_name = exp_name
