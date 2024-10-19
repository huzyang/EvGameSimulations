import os
import math
import networkx as nx
import matplotlib.pyplot as plt

# Parameters of the model of evolutionary dynamics for the N-player Trust Game
# n -玩家信任博弈演化动力学模型的参数
#
# @author mchica
# @date 2016/04/27
#

class ModelParameters:

    # Read configuration file
    # 用util中的ConfigFileReader类
    config = None

    # FOR THE STRATEGY TYPE FOR AGENTS
    # 用于代理的策略类型
    UNDEFINED_STRATEGY = 0
    TRUSTER = 1
    TRUSTWORTHY_TRUSTEE = 2
    UNTRUSTWORTHY_TRUSTEE = 3

    # TYPE OF NETWORK
    # 网络类型
    WELL_MIXED_POP = -1
    SF_NETWORK = 0
    ER_NETWORK = 1
    SW_NETWORK = 2
    PGP_NETWORK = 3
    EMAIL_NETWORK = 4
    REGULAR_NETWORK = 5

    # TYPE OF UPDATE RULE FOR THE AGENTS
    PROPORTIONAL_UPDATE_RULE = 1
    UI_UPDATE_RULE = 2
    VOTER_UPDATE_RULE = 3
    FERMI_UPDATE_RULE = 4
    MORAN_UPDATE_RULE = 5

    # ########################################################################
    # Variables
    # ########################################################################

    outputFile = None

    # modified just to use a static SN from a file
    # 修改只是为了使用文件中的静态SN

    # FILE_NETWORK ONLY!!
    # Choose between several social networks:
    # SCALE_FREE_NETWORK, scale-free (Barabasi)
    # ER_RANDOM_NETWORK
    # SW_RANDOM_NETWORK
    typeOfNetwork = None

    networkFilesPattern = None

    # graph read from file
    graphFromFile = None

    ##################################################

    # multipliers for the payoff calculation between cooperators
    # 合作者之间收益计算的乘数
    R_T = None  # multiplier of what is received by k_T from k_I (R_T*tv)
    R_U = None  # multiplier of what is received by k_U from k_I (R_U*tv)
    r_UT = None  # temptation to defect ratio which falls in (0,1). It is equal to (R_U-R_T)/R_T

    tv = None  # value payed by trusters to trustee (normally fixed)

    # population distribution
    nrAgents = None

    # 模拟开始时代理成为信任者的百分比 总用户
    percentageTrusters = None  # percentage of agents to be trusters at the
                               # beginning of the simulation w.r.t. total
                               # users
    # 代理商成为可信赖受托人的百分比 人口的受托人（nrAgents-（k_I * nrAgents））
    percentageTrustworthies = None  # percentage of agents to be trustworthy
                                    # trustees w.r.t. the trustees of the pop
                                    # (nrAgents - (k_I*nrAgents)

    k_I = None  # number of agents to be trusters/investors at the beginning of the simulation
    k_T = None  # number of agents to be trustworthy trustees at the beginning of the simulation
    k_U = None  # number of agents to be untrustworthy trustees at the beginning of the simulation

    # update's rule for the ev dynamics game
    T_rounds = 1  # number of steps to update the strategy of the agents by
                  # an update rule
    maxSteps = None  # maximum number of steps for the simulation
    runsMC = None  # number of MC runs
    updateRule = None  # identifier for the update rule of the agents

    q_VM = 1  # q value in [0,1] to either choose the VM or UI. If 1, always VM. 1-q, UI is applied

    seed = None  # seed to run all the simulations

    # --------------------------- Get/Set methods ---------------------------//

    def getQ_VM(self):
        return self.q_VM

    def setQ_VM(self, q_VM):
        self.q_VM = q_VM

    def getSeed(self):
        return self.seed

    def setSeed(self, _seed):
        self.seed = _seed

    def getMaxSteps(self):
        return self.maxSteps

    def setMaxSteps(self, _maxSteps):
        self.maxSteps = _maxSteps

    def getOutputFile(self):
        return self.outputFile

    def setOutputFile(self, outputFile):
        self.outputFile = outputFile

    def getR_UT(self):
        return self.r_UT

    def setR_UT(self, _ratio):
        self.r_UT = _ratio

    def getT_rounds(self):
        return self.T_rounds

    def setT_rounds(self, _T_rounds):
        self.T_rounds = _T_rounds

    def getTypeOfNetwork(self):
        return self.typeOfNetwork

    def setTypeOfNetwork(self, typeOfNetwork):
        self.typeOfNetwork = typeOfNetwork

    def getGraph(self):
        return self.graphFromFile

    def setGraph(self, _graph):
        self.graphFromFile = _graph

    def getNetworkFilesPattern(self):
        return self.networkFilesPattern

    def setNetworkFilesPattern(self, networkFilesPattern):
        self.networkFilesPattern = networkFilesPattern

    def readGraphFromFile(self, fileNameGraph):
        self.graphFromFile = nx.read_graphml(fileNameGraph)

    def displayGraph(self, k_I, k_T, k_U):
        pos = nx.spring_layout(self.graphFromFile)
        labels = {node: node for node in self.graphFromFile.nodes()}

        for node in self.graphFromFile.nodes():
            if node in k_I:
                color = 'green'
            elif node in k_T:
                color = 'blue'
            elif node in k_U:
                color = 'red'
            else:
                color = 'gray'

            nx.draw_networkx_nodes(self.graphFromFile, pos, nodelist=[node], node_color=color)

        nx.draw_networkx_edges(self.graphFromFile, pos)
        nx.draw_networkx_labels(self.graphFromFile, pos, labels)
        plt.show()

    def getNrAgents(self):
        return self.nrAgents

    def setNrAgents(self, nrAgents):
        if nrAgents > 0:
            self.nrAgents = nrAgents

    def getUpdateRule(self):
        return self.updateRule

    def setUpdateRule(self, _updateRule):
        self.updateRule = _updateRule

    def getTv(self):
        return self.tv

    def setTv(self, _tv):
        self.tv = _tv

    def getR_T(self):
        return self.R_T

    def setR_T(self, _R_T):
        self.R_T = _R_T

    def getR_U(self):
        return self.R_U

    def setR_U(self, _R_U):
        self.R_U = _R_U

    def getPercentageTrusters(self):
        return self.percentageTrusters

    def getPercentageTrustworthies(self):
        return self.percentageTrustworthies

    def setPercentageTrusters(self, percentageTrusters):
        self.percentageTrusters = percentageTrusters

    def setPercentageTrustworthies(self, percentageTrustworthies):
        self.percentageTrustworthies = percentageTrustworthies

    def getk_I(self):
        return self.k_I

    def setk_I(self, _k_I):
        self.k_I = _k_I

    def getk_T(self):
        return self.k_T

    def setk_T(self, _k_T):
        self.k_T = _k_T

    def getk_U(self):
        return self.k_U

    def setk_U(self, _k_U):
        self.k_U = _k_U

    def getRunsMC(self):
        return self.runsMC

    def setRunsMC(self, _runsMC):
        self.runsMC = _runsMC

    # ########################################################################
    # Constructors
    # ########################################################################

    def __init__(self):
        pass

    # ########################################################################
    # Export methods
    # ########################################################################

    def export(self):
        values = ""
        values += self.exportGeneral()
        values += self.exportSN()
        return values

    def exportSN(self):
        result = ""
        result += "SNFile = " + self.networkFilesPattern + "\n"
        result += "typeOfSN = " + str(self.typeOfNetwork) + "\n"
        return result

    def exportGeneral(self):
        result = ""
        result += "MC_runs = " + str(self.runsMC) + "\n"
        result += "seed = " + str(self.seed) + "\n"
        result += "nrAgents = " + str(self.nrAgents) + "\n"
        result += "maxSteps = " + str(self.maxSteps) + "\n"
        result += "T_rounds = " + str(self.T_rounds) + "\n"
        result += "percentage_trusters = " + str(self.percentageTrusters) + "\n"
        result += "percentage_trustworthies = " + str(self.percentageTrustworthies) + "\n"
        result += "k_I = " + str(self.k_I) + "\n"
        result += "k_T = " + str(self.k_T) + "\n"
        result += "k_U = " + str(self.k_U) + "\n"
        result += "R_T = " + str(self.R_T) + "\n"
        result += "r_UT = " + str(self.r_UT) + "\n"
        result += "R_U = " + str(self.R_U) + "\n"
        result += "tv = " + str(self.tv) + "\n"

        if self.updateRule == ModelParameters.PROPORTIONAL_UPDATE_RULE:
            result += "updateRule = PROPORTIONAL_UPDATE_RULE\n"
        elif self.updateRule == ModelParameters.UI_UPDATE_RULE:
            result += "updateRule = UI_UPDATE_RULE\n"
        elif self.updateRule == ModelParameters.VOTER_UPDATE_RULE:
            result += "updateRule = VOTER_UPDATE_RULE\n"
            result += "q_VM = " + str(self.q_VM) + "\n"
        elif self.updateRule == ModelParameters.FERMI_UPDATE_RULE:
            result += "updateRule = FERMI_UPDATE_RULE\n"
        elif self.updateRule == ModelParameters.MORAN_UPDATE_RULE:
            result += "updateRule = MORAN_UPDATE_RULE\n"

        return result

    def updateKsFromPercentages(self):
        # round() 方法返回一个最接近的 int、long 型值，四舍五入。
        self.k_I = int(round(self.nrAgents * self.percentageTrusters))
        self.k_T = int(round(self.nrAgents * self.percentageTrustworthies))
        self.k_U = self.nrAgents - (self.k_I + self.k_T)

    """
     # Reads parameters from the configuration file.
	 # 从配置文件中读取参数。
    """
    def readParameters(self, CONFIGFILENAME):
        try:
            # Read parameters from the file
            self.config = ConfigFileReader(CONFIGFILENAME)
            self.config.readConfigFile()

            # Get global parameters
            self.maxSteps = self.config.getParameterInteger("maxSteps")
            self.runsMC = self.config.getParameterInteger("MCRuns")
            self.T_rounds = self.config.getParameterInteger("T_rounds")
            self.seed = self.config.getParameterInteger("seed")
            self.nrAgents = self.config.getParameterInteger("nrAgents")

            # obtain the percentage of trusters and trustworthies to calculate k_I, k_T, k_U
            self.percentageTrusters = self.config.getParameterDouble("percentage_trusters")
            self.percentageTrustworthies = self.config.getParameterDouble("percentage_trustworthies")

            if (self.percentageTrusters + self.percentageTrustworthies) > 1.0:
                raise ValueError("Error with % of trusters and trustworthies. It is > 1. "
                                 "Check params percentageTrusters and percentageTrustworthies\n")

            self.updateKsFromPercentages()

            self.updateRule = self.config.getParameterInteger("updateRule")

            if self.updateRule == ModelParameters.VOTER_UPDATE_RULE:
                try:
                    self.q_VM = self.config.getParameterDouble("q_VM")
                except Exception:
                    # if it is not defined, q by default (= 1). Always VM
                    self.q_VM = 1.0
            else:
                self.q_VM = -1

            self.R_T = self.config.getParameterDouble("R_T")
            self.r_UT = self.config.getParameterDouble("r_UT")
            self.R_U = (1 + self.r_UT) * self.R_T
            self.tv = self.config.getParameterInteger("tv")

            # Always read social network file but this file can be SF, Random,
            # RW or regular
            self.setNetworkFilesPattern(self.config.getParameterString("SNFile"))
            self.readGraphFromFile(self.networkFilesPattern)

            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.SW_NETWORK:
                self.typeOfNetwork = NetworkType.SW_NETWORK
            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.ER_NETWORK:
                self.typeOfNetwork = NetworkType.RANDOM_NETWORK
            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.SF_NETWORK:
                self.typeOfNetwork = NetworkType.SCALE_FREE_NETWORK
            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.WELL_MIXED_POP:
                self.typeOfNetwork = NetworkType.WELL_MIXED_POP
            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.PGP_NETWORK:
                self.typeOfNetwork = NetworkType.PGP_NETWORK
            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.EMAIL_NETWORK:
                self.typeOfNetwork = NetworkType.EMAIL_NETWORK
            if self.config.getParameterInteger("typeOfNetwork") == ModelParameters.REGULAR_NETWORK:
                self.typeOfNetwork = NetworkType.REGULAR_NETWORK

        except Exception as e:
            print(f"Error with SN file when loading parameters for the simulation {CONFIGFILENAME}\n{e}")

    # ----------------------------- I/O methods -----------------------------//

    def printParameters(self, writer):
        # printing general params
        writer.write(self.export())

