#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import time
from datetime import datetime
import sys
import getopt
from evgamesimulations.game import RunStats

"""MAIN FUNCTION.
主要用于运行一个模拟模型，包含了命令行参数解析、模拟运行控制、模型参数读取、以及统计数据的输出。
这个类提供了执行简单模型运行或进行敏感性分析的功能。代码通过文件系统来管理输出，并将运行结果保存到指定的日志文件中。

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py
"""
# Constants to get different options for simple or SA runs
NO_SA = 0  # No Simulated Annealing
SA_INITIAL_POPULATION = 1  # Simulated Annealing with initial population
SA_RT_RU = 2  # Simulated Annealing with runtime resource usage

# ============ LOGGING ===============
log = logging.getLogger(__name__)

# 设置日志的最低级别，类似于 Java 中 Logger 的默认行为
log.setLevel(logging.DEBUG)

# 可以为 Logger 添加处理程序，如输出到控制台
handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    """MAIN CONSOLE-BASED FUNCTION TO RUN A SIMPLE RUN OR A SENSITIVITY ANALYSIS OF THE MODEL PARAMETERS"""
    # 基于控制台的主要功能，用于简单运行或模型参数的敏感性分析

    if argv is None:
        argv = sys.argv
    try:
        # Counter to keep track of the total number of iterations
        total_count = 0

        # Start timing
        time_start = time.time()

        # ===============================
        # Set parameters
        # ===============================
        # Custom output file for results
        file_my_data = "./logs/fileMyData.txt"
        output_file = "exp_SA"

        # Initialize SA parameter
        SA = NO_SA

        # Path to the parameter configuration file
        params_file = "./config/params_1024agents_model_master_SF4.properties"

        params = ModelParameters()

        # Set the number of Monte Carlo (MC) runs
        params.set_runs_MC(5)

        # Set SA (can be changed if needed)
        # SA = SA_RT_RU

        # Read parameters from file
        params.read_parameters(params_file)

        # Set the output file
        params.set_output_file(output_file)

        # Files to store text output with the obtained results
        file_all_mc = f"./logs/AllMCruns_{params.get_output_file()}.txt"
        file_summary_mc = f"./logs/SummaryMCruns_{params.get_output_file()}.txt"
        file_all_mc_lq = f"./logs/AllMCrunsLQ_{params.get_output_file()}.txt"
        file_summary_mc_lq = f"./logs/SummaryMCrunsLQ_{params.get_output_file()}.txt"
        file_time_series_mc = f"./logs/TimeSeriesMCruns_{params.get_output_file()}.txt"

        # Print the message indicating the start of the model run
        print("\n****** STARTING THE RUN OF THE -TRUST- DYNAMICS ABM MODEL ******\n")

        # Get the current date and time，Print the current date and time
        current_date = datetime.now()
        print(f"****** {current_date} ******\n")

        # the SA check
        if SA == NO_SA:
            """No Sensitivity Analysis, simple run"""

            # Print parameters for double-checking
            print("-> Parameters values of this model:")

            # TODO Running the model with the MC simulations
            time1 = time.time()
            controller = Controller(params, params_file)
            run_stats = controller.run_model()

            # run_stats.set_exp_name(params.get_output_file())

            # Simulation ends here
            time2 = time.time()
            print(f"\n****** {(time2 - time1):.2f}s spent during the simulation.")

            # calculating results
            run_stats.calc_all_stats()

            # Print the stats on the screen
            # run_stats.print_summary_stats(out, False)
            # run_stats.print_summary_stats_by_averaging_last_quartile(out, False)  # Also the last quartile info

            # save the stats into a file
            # try:
            #     print("\n****** Stats also saved into a file ******\n")

            #     # Print all the runs info into a file
            #     with open(file_all_mc, 'w') as print_writer:
            #         stats.print_all_stats(print_writer, False)

            #     # Print all runs info (last quartiles of the sims) into a file
            #     with open(file_all_mc_lq, 'w') as print_writer:
            #         stats.print_all_stats_by_averaging_last_quartile(print_writer, False)

            #     # Print the summarized MC runs into a file
            #     with open(file_summary_mc, 'w') as print_writer:
            #         stats.print_summary_stats(print_writer, False)

            #     # Print the summarized MC runs (last quartiles of the sims) into a file
            #     with open(file_summary_mc_lq, 'w') as print_writer:
            #         stats.print_summary_stats_by_averaging_last_quartile(print_writer, False)

            #     # Print the time series into a file
            #     with open(file_time_series_mc, 'w') as print_writer:
            #         stats.print_time_series_stats(print_writer)

            # except FileNotFoundError as e:
            #     # Handle file not found error
            #     e.print_stack_trace()
            #     log.log(logging.ERROR, str(e))

        else:
            # SA over the initial population
            if SA == SA_INITIAL_POPULATION:
                SensitivityAnalysis.run_SA_kI_kT_kU(
                    params,
                    params_file,
                    file_all_mc,
                    file_summary_mc,
                    file_all_mc_lq,
                    file_summary_mc_lq,
                )
            elif SA == SA_RT_RU:
                SensitivityAnalysis.run_SA_RT_RU(
                    params,
                    params_file,
                    file_all_mc,
                    file_summary_mc,
                    file_all_mc_lq,
                    file_summary_mc_lq,
                )

        time_end = time.time()
        time_total = time_end - time_start

        # Print the total number of simulations and time spent
        print(f"Total simulations: {total_count}, Time spent: {time_total:.2f} s!")

    except Usage as err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())


class CoreConsoleSimulation:

    @staticmethod
    def create_arguments():
        # TODO
        """
        Create an options dictionary to store all the arguments of the command-line call of the program.
        @param options the class containing the options, when returned. It has to be created before calling

        创建一个选项类来存储程序命令行调用的所有参数
        """
        options = {
            "params_file": None,
            "SN_file": None,
            "output_file": None,
            "percentage_trusters": None,
            "percentage_trustworthies": None,
            "R_T": None,
            "R_U": None,
            "max_steps": None,
            "MC": None,
            "seed": None,
            "SA": False,
            "SA_RT_RU": False,
            "SA_trusters_min": None,
            "SA_trusters_max": None,
            "SA_trusters_step": None,
            "SA_trustworthies_min": None,
            "SA_trustworthies_max": None,
            "SA_trustworthies_step": None,
            "help": False,
        }
        """
        # TODO
        set as optional those arguments they are optional
        将这些参数设置为可选，它们是可选的
		
        options.getOption("density").setOptionalArg(true);
		options.getOption("probRewiring").setOptionalArg(true);
		options.getOption("m").setOptionalArg(true);
		
		options.getOption("density").setRequired(false);
		options.getOption("probRewiring").setRequired(false);
		options.getOption("m").setRequired(false);
        """
        return options

    @staticmethod
    def main():
        """
        Main console-based function to run a simple run or a sensitivity analysis of the model parameters.

        基于控制台的主要功能，用于简单运行或分析模型参数的敏感性
        """

        # Simple run or sensitivity analysis check
        if SA == NO_SA:
            # No SA, simple run
            stats = None

            # Print parameters for double-checking
            print("-> Parameters values:")
            params.print_parameters()

            log.debug(f"\n*** Parameters values of this model:\n{params.export()}")

            # Run the MC simulations
            time1 = time.time()
            controller = Controller(params, params_file)
            stats = controller.run_model()

            stats.set_exp_name(params.get_output_file())

            # End of simulation
            time2 = time.time()
            print(
                f"\n****** {round((time2 - time1), 3)} seconds spent during the simulation"
            )

            stats.calc_all_stats()

            # Print stats
            stats.print_summary_stats(False)
            stats.print_summary_stats_by_averaging_last_quartile(False)

            print("\n****** Stats also saved into a file ******\n")

            try:
                # Save all runs info to files
                with open(file_all_mc, "w") as file:
                    stats.print_all_stats(file, False)

                with open(file_all_mc_lq, "w") as file:
                    stats.print_all_stats_by_averaging_last_quartile(file, False)

                with open(file_summary_mc, "w") as file:
                    stats.print_summary_stats(file, False)

                with open(file_summary_mc_lq, "w") as file:
                    stats.print_summary_stats_by_averaging_last_quartile(file, False)

                with open(file_time_series_mc, "w") as file:
                    stats.print_time_series_stats(file)

            except FileNotFoundError as e:
                log.error(f"Error occurred: {e}")
                print(f"Error occurred: {e}")

        else:
            if SA == SA_INITIAL_POPULATION:
                SensitivityAnalysis.run_SA_kI_kT_kU(
                    params,
                    params_file,
                    file_all_mc,
                    file_summary_mc,
                    file_all_mc_lq,
                    file_summary_mc_lq,
                )
            elif SA == SA_RT_RU:
                SensitivityAnalysis.run_SA_RT_RU(
                    params,
                    params_file,
                    file_all_mc,
                    file_summary_mc,
                    file_all_mc_lq,
                    file_summary_mc_lq,
                )

        total_time = round((time.time() - time1), 3)
        print(
            f"Total simulation count: {total_count}, Total time: {total_time} seconds."
        )
