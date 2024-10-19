import logging

class Controller:
    """
    Controller

    This class is the controller to call the model
    It calls the model, run it to get all the steps and returns a list
    of simulated values
    这个类是调用模型的控制器。它调用模型，运行它以获得所有步骤，并返回模拟值列表

    """

    # LOGGING
    log = logging.getLogger(__name__)

    def __init__(self, _params, _paramsFile):
        """
        Constructor having config, seed and maxSteps
        具有配置、seed和maxSteps的构造函数
        """
        Model.set_config_file_name(_paramsFile)
        self.model = Model(_params)

    def get_model_parameters(self):
        """
        @return the ModelParameters object where all the parameters are defined
        ModelParameters对象，其中定义了所有的参数
        """
        return self.model.get_parameters_object()

    def set_model_parameters(self, _params):
        """
        Set the ModelParameters object for all the defined parameters
        为所有定义的参数设置ModelParameters对象
        """
        self.model.set_parameters_object(_params)

    def run_model(self):
        """
        Run the model one time
        运行模型一次
        @return the statistics after running the model
        运行模型后的统计信息
        """
        # starting and looping the mode

        # object to store results into the stats object
        stats = RunStats(self.model.get_parameters_object().get_runs_mc(),
                         self.model.get_parameters_object().get_max_steps())

        self.log.debug("\n**Starting MC sim\n")
        self.log.debug("\n%s\n", self.model.get_parameters_object().export())

        print(f"\nMC runs ({self.model.get_parameters_object().get_runs_mc()}): ", end="")

        for i in range(self.model.get_parameters_object().get_runs_mc()):
            # for each MC run we start the model and run it
            # 调用modle类文件
            self.model.start()

            while self.model.schedule.get_steps() < self.model.get_parameters_object().get_max_steps():
                if not self.model.schedule.step(self.model):
                    break

            self.model.finish()

            # store to the stats object
            stats.set_k_i_for_run(i, self.model.get_k_i_agents_array())
            stats.set_k_t_for_run(i, self.model.get_k_t_agents_array())
            stats.set_k_u_for_run(i, self.model.get_k_u_agents_array())

            stats.set_strategy_changes_for_run(i, self.model.get_strategy_changes_agents_array())

            # TODO doing both, saving the global wealth in the final step and in the last n steps (e.g., 25%)
            # 在最后一步和最后n步中储存全球财富（例如25％）
            stats.set_net_wealth_for_run(i, self.model.get_global_payoffs())

            # to show some logs about activity of the agents
            self.model.print_statistics_screen()

            self.log.debug("MC-%d/%d ended\n\n", i+1, self.model.get_parameters_object().get_runs_mc())

            print(".", end="", flush=True)

        print(" -> Ended!")

        return stats

