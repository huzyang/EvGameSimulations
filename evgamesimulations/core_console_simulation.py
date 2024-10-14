# -*- coding: utf-8 -*-
import logging
import os
import time
from datetime import datetime

"""
ConsoleSimulation.java 主要用于运行一个模拟模型，包含了命令行参数解析、模拟运行控制、模型参数读取、以及统计数据的输出。这个类提供了执行简单模型运行或进行敏感性分析的功能。代码通过文件系统来管理输出，并将运行结果保存到指定的日志文件中。

代码重构到 Python 时的关键要点
1. 命名规范
Java 的驼峰命名法将被转换为 Python 的下划线命名法。例如，createArguments 可以变成 create_arguments。
类常量的命名保持大写并用下划线分隔，例如 NO_SA 仍然是 NO_SA。
2. 主要修改点
Java 类转为 Python 类: Java 类会变成 Python 类，类中的静态方法用 @staticmethod 注解。
日志处理: Java 中的日志管理器 (Logger) 在 Python 中可以用 logging 模块替代。
文件处理: Java 文件操作部分，如 PrintWriter，在 Python 中可以用 with open() 语句来处理。
异常处理: Java 的 try-catch 语句转换为 Python 的 try-except 语句。
模型参数: 类似于 ModelParameters 这样的类需要确保它们在 Python 中有合适的等效实现。

可能的问题点
需要确保 ModelParameters、Controller 和 SensitivityAnalysis 类在实际 Python 项目中有对应实现，本文中提供了占位符。
如果原始 Java 项目中包含更多的外部依赖（例如用于模型控制或敏感性分析的库），需要根据 Python 的相关模块或库来进行等效实现。
"""
# Constants for different options for simple or SA runs
NO_SA = 0
SA_INITIAL_POPULATION = 1
SA_RT_RU = 2

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Model')

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
            'params_file': None,
            'SN_file': None,
            'output_file': None,
            'percentage_trusters': None,
            'percentage_trustworthies': None,
            'R_T': None,
            'R_U': None,
            'max_steps': None,
            'MC': None,
            'seed': None,
            'SA': False,
            'SA_RT_RU': False,
            'SA_trusters_min': None,
            'SA_trusters_max': None,
            'SA_trusters_step': None,
            'SA_trustworthies_min': None,
            'SA_trustworthies_max': None,
            'SA_trustworthies_step': None,
            'help': False
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
        # Custom result output file
        file_my_data = "./logs/fileMyData.txt" 
        total_count = 0  # Total loop count
        total_count += 1
        SA = NO_SA  # for simple or SA runs

        # TODO Parameter configuration file path
        params_file = "./config/params_1024agents_model_master_SF4.csv"
        output_file = "exp_SA"

        # TODO Get parameters
        params = ModelParameters()

        # Set MC
        params.set_runs_MC(5)

        # Read parameters from file
        params.read_parameters(params_file)

        # Set the output file
        params.set_output_file(output_file)

        print("\n****** STARTING THE RUN OF THE TRUST DYNAMICS ABM MODEL ******\n")
        current_date = datetime.now()

        # Present date and time
        print(f"****** {current_date} ******\n")

        # Prepare file paths for storing results
        file_all_mc = f"./logs/AllMCruns_{params.get_output_file()}.txt"
        file_summary_mc = f"./logs/SummaryMCruns_{params.get_output_file()}.txt"
        file_all_mc_lq = f"./logs/AllMCrunsLQ_{params.get_output_file()}.txt"
        file_summary_mc_lq = f"./logs/SummaryMCrunsLQ_{params.get_output_file()}.txt"
        file_time_series_mc = f"./logs/TimeSeriesMCruns_{params.get_output_file()}.txt"

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
            print(f"\n****** {round((time2 - time1), 3)} seconds spent during the simulation")

            stats.calc_all_stats()

            # Print stats
            stats.print_summary_stats(False)
            stats.print_summary_stats_by_averaging_last_quartile(False)

            print("\n****** Stats also saved into a file ******\n")

            try:
                # Save all runs info to files
                with open(file_all_mc, 'w') as file:
                    stats.print_all_stats(file, False)

                with open(file_all_mc_lq, 'w') as file:
                    stats.print_all_stats_by_averaging_last_quartile(file, False)

                with open(file_summary_mc, 'w') as file:
                    stats.print_summary_stats(file, False)

                with open(file_summary_mc_lq, 'w') as file:
                    stats.print_summary_stats_by_averaging_last_quartile(file, False)

                with open(file_time_series_mc, 'w') as file:
                    stats.print_time_series_stats(file)

            except FileNotFoundError as e:
                log.error(f"Error occurred: {e}")
                print(f"Error occurred: {e}")

        else:
            if SA == SA_INITIAL_POPULATION:
                SensitivityAnalysis.run_SA_kI_kT_kU(params, params_file, file_all_mc, file_summary_mc, file_all_mc_lq, file_summary_mc_lq)
            elif SA == SA_RT_RU:
                SensitivityAnalysis.run_SA_RT_RU(params, params_file, file_all_mc, file_summary_mc, file_all_mc_lq, file_summary_mc_lq)

        total_time = round((time.time() - time1), 3)
        print(f"Total simulation count: {total_count}, Total time: {total_time} seconds.")

# Define placeholders for ModelParameters, Controller, and SensitivityAnalysis as these classes are external in the original code
class ModelParameters:
    def __init__(self):
        self.output_file = ""
        self.MC_runs = 0

    def set_runs_MC(self, runs):
        self.MC_runs = runs

    def read_parameters(self, file_path):
        print(f"Reading parameters from {file_path}")

    def set_output_file(self, file_name):
        self.output_file = file_name

    def get_output_file(self):
        return self.output_file

    def print_parameters(self):
        print("Printing model parameters")

    def export(self):
        return "Model parameter values"

class Controller:
    def __init__(self, params, params_file):
        self.params = params
        self.params_file = params_file

    def run_model(self):
        print(f"Running model with params from {self.params_file}")
        return RunStats()

class RunStats:
    def set_exp_name(self, name):
        print(f"Setting experiment name: {name}")

    def calc_all_stats(self):
        print("Calculating all stats")

    def print_summary_stats(self, out_file, flag):
        print("Printing summary stats")

    def print_summary_stats_by_averaging_last_quartile(self, out_file, flag):
        print("Printing summary stats for the last quartile")

    def print_all_stats(self, out_file, flag):
        print("Printing all stats")

    def print_time_series_stats(self, out_file):
        print("Printing time series stats")

class SensitivityAnalysis:
    @staticmethod
    def run_SA_kI_kT_kU(params, params_file, file_all_mc, file_summary_mc, file_all_mc_lq, file_summary_mc_lq):
        print("Running sensitivity analysis over initial population parameters")

    @staticmethod
    def run_SA_RT_RU(params, params_file, file_all_mc, file_summary_mc, file_all_mc_lq, file_summary_mc_lq):
        print("Running sensitivity analysis over RT-RU parameters")

