import logging
import time
from random import random
from collections import deque
"""
# Simulation core, responsible for scheduling agents of the n-trust game
# 仿真核心，负责安排n人信任游戏的代理
"""
class Model(SimState):
    # ########################################################################
	# Variables
	# ########################################################################

    INCLUDEZERO = True
    INCLUDEONE = True

    SHOW_SN = False
    OUTPUT_LATTICE = False

    # LOGGING
    log = logging.getLogger(__name__)

    CONFIG_FILENAME = None  # Assuming this is defined somewhere in the actual code

    # MODEL VARIABLES
    minPayOff = None   # min payoff to be obtained by agents for the update rule
    maxPayOff = None    # max payoff to be obtained by agents for the update rule

    global_payoffs = []  # Placeholder for global payoffs
    agents = None  # Placeholder for Bag instance
    k_T_Agents = []  # Placeholder for k_T agents array
    k_I_Agents = []  # Placeholder for k_I agents array
    k_U_Agents = []  # Placeholder for k_U agents array
    strategy_changes = []  # Placeholder for strategy changes
    params = None  # Placeholder for ModelParameters instance

    MC_RUN = -1

    # SOCIAL NETWORK
    social_network = None  # Placeholder for GraphStreamer instance

    def __init__(self, _params):
        super().__init__(_params.getSeed())

        try:
            millis = int(time.time() * 1000)
            logging.basicConfig(filename=f"./logs/{_params.getOutputFile()}_{millis}.log", level=logging.DEBUG)
            self.log.debug(f"Log file created at {millis} (System Time Millis)\n")
        except Exception as e:
            print(e)

        self.params = _params

        self.k_I_Agents = [0] * self.params.getMaxSteps()
        self.k_T_Agents = [0] * self.params.getMaxSteps()
        self.k_U_Agents = [0] * self.params.getMaxSteps()

        self.strategyChanges = [0] * self.params.getMaxSteps()
        self.globalPayoffs = [0.0] * self.params.getMaxSteps()

        self.socialNetwork = GraphStreamer(self.params.nrAgents, self.params)
        self.socialNetwork.setGraph(self.params)

        self.minPayOff = self.maxPayOff = -1.0

    def get_config_file_name():
        return CONFIG_FILENAME

    def set_config_file_name(config_file_name):
        global CONFIG_FILENAME
        CONFIG_FILENAME = config_file_name

    def get_social_network():
        return social_network

    def get_global_payoffs():
        return global_payoffs

    def set_global_payoffs(global_payoffs_array):
        global global_payoffs
        global_payoffs = global_payoffs_array

    def get_agents():
        return agents

    def set_agents(agents_bag):
        global agents
        agents = agents_bag

    def get_global_payoff_at_step(position):
        return global_payoffs[position]

    def get_k_T_agents_at_step(position):
        return k_T_Agents[position]

    def get_k_T_agents_array():
        return k_T_Agents

    def get_k_I_agents_at_step(position):
        return k_I_Agents[position]

    def get_k_I_agents_array():
        return k_I_Agents

    def get_k_U_agents_at_step(position):
        return k_U_Agents[position]

    def get_strategy_changes_agents_array():
        return strategy_changes

    def get_k_U_agents_array():
        return k_U_Agents

    def get_parameters_object():
        return params

    def set_parameters_object(parameters):
        global params
        params = parameters

    def start(self):
        super().start()

        self.MC_RUN += 1

        if (self.params.getk_I() + self.params.getk_T() + self.params.getk_U()) != self.params.nrAgents:
            print("Error with the k_I, k_T, k_U distribution. Check k_I + k_T + k_U is equal to the total number of agents \n")

        FIRST_SCHEDULE = 0
        scheduleCounter = FIRST_SCHEDULE

        for i in range(self.params.getMaxSteps()):
            self.k_I_Agents[i] = self.k_T_Agents[i] = self.k_U_Agents[i] = 0
            self.strategyChanges[i] = 0
            self.globalPayoffs[i] = 0.0

        self.minPayOff = -1 * self.params.getTv()
        self.maxPayOff = self.socialNetwork.getAvgDegree() * self.params.getR_U() * self.params.getTv()

        self.agents = deque()

        for i in range(self.params.getNrAgents()):
            strategy = ModelParameters.UNDEFINED_STRATEGY

            if i < self.params.k_I:
                strategy = ModelParameters.TRUSTER
            elif i < (self.params.k_I + self.params.k_T):
                strategy = ModelParameters.TRUSTWORTHY_TRUSTEE
            elif i < (self.params.k_I + self.params.k_T + self.params.k_U):
                strategy = ModelParameters.UNTRUSTWORTHY_TRUSTEE

            cl = self.generateAgent(i, strategy)
            self.agents.append(cl)
            schedule.scheduleRepeating(Schedule.EPOCH, scheduleCounter, cl)

        # shuffle agents in the Bag and later, reassign the id to the position in the bag
        # 在袋中洗牌，然后将ID重新分配到袋中的位置
        self.shuffle_agents()
        
        if Model.SHOW_SN:
            self.testShowSN()

        self.setAnonymousAgentApriori(scheduleCounter)
        scheduleCounter += 1
        self.setAnonymousAgentAposteriori(scheduleCounter)

    def shuffle_agents(self):
        shuffled_agents = list(self.agents)
        random.shuffle(shuffled_agents)
        for i, agent in enumerate(shuffled_agents):
            agent.setGamerAgentId(i)

    def testShowSN(self):
        stylesheet = "graph { fill-color: rgb(255,255,255); padding: 50px; } node { size: 12px; fill-mode: dyn-plain; fill-color: red,green,blue,yellow,orange,pink,purple; } node .membrane { size: 25px; } edge { fill-color: grey; } edge.important { fill-color: red; } edge.reset { fill-color: grey; }"
        self.socialNetwork.getGraph().addAttribute("ui.stylesheet", stylesheet)

        colorPalette = Colors(6)
        self.socialNetwork.getGraph().addAttribute("ui.default.title", f"MC {self.MC_RUN}, seed: {self.seed()}")

        for node in self.socialNetwork.getGraph():
            node.setAttribute("size", "medium")
            node.addAttribute("ui.label", node.getId())

        self.display_agent_types(colorPalette)

    def display_agent_types(self, colorPalette):
        print("Trusters: ", end="")
        for i in range(len(self.agents)):
            if self.agents[i].getCurrentStratey() == ModelParameters.TRUSTER:
                print(f"{self.agents[i].getGamerAgentId()},", end="")
                self.socialNetwork.setNodeColor(i, 1, colorPalette)
        print("\nTrustworthies: ", end="")
        for i in range(len(self.agents)):
            if self.agents[i].getCurrentStratey() == ModelParameters.TRUSTWORTHY_TRUSTEE:
                print(f"{self.agents[i].getGamerAgentId()},", end="")
                self.socialNetwork.setNodeColor(i, 2, colorPalette)
        print("\nUntrustworthies: ", end="")
        for i in range(len(self.agents)):
            if self.agents[i].getCurrentStratey() == ModelParameters.UNTRUSTWORTHY_TRUSTEE:
                print(f"{self.agents[i].getGamerAgentId()},", end="")
                self.socialNetwork.setNodeColor(i, 3, colorPalette)
        print("")

        self.socialNetwork.getGraph().display()

    def generateAgent(self, _nodeId, _strategy):
        cl = GamerAgent(_nodeId, _strategy, self.params.maxSteps, self.params.T_rounds)
        cl.setProbabilityToAct(1)

        active = [False] * self.params.maxSteps
        for i in range(len(active)):
            r = random()
            active[i] = r < cl.getProbabilityToAct()

        cl.setActiveArray(active)
        return cl

    def calculatePayoffWithNeighborsGlobally(self):
        currentStep = int(schedule.getSteps())
        tv = self.getParametersObject().getTv()
        R_T = self.getParametersObject().getR_T()
        R_U = self.getParametersObject().getR_U()

        denom = (self.k_T_Agents[currentStep] + self.k_U_Agents[currentStep])
        self.globalPayoffs[currentStep] = 0.0

        for i in range(self.params.nrAgents):
            agentWealth = 0.0

            if denom > 0:
                strategy = self.agents[i].getCurrentStratey()
                if strategy == ModelParameters.TRUSTER:
                    agentWealth = tv * ((R_T * (self.k_T_Agents[currentStep] / denom)) - 1)
                elif strategy == ModelParameters.TRUSTWORTHY_TRUSTEE:
                    agentWealth = R_T * tv * (self.k_I_Agents[currentStep] / denom)
                elif strategy == ModelParameters.UNTRUSTWORTHY_TRUSTEE:
                    agentWealth = R_U * tv * (self.k_I_Agents[currentStep] / denom)

            self.agents[i].setPayoff(agentWealth, currentStep)
            self.globalPayoffs[currentStep] += agentWealth

        return self.globalPayoffs[currentStep]
    
    # -------------------------- Auxiliary methods --------------------------
    def generate_agent(self, node_id, strategy):
        """
        Generates an agent with its initial strategy, id, and an array indicating its activity over steps.
        All agents are always active in this case.

        :param node_id: ID of the agent
        :param strategy: Strategy the agent is going to follow
        :return: The generated agent with assigned properties
        """
        agent = GamerAgent(node_id, strategy, self.params['max_steps'], self.params['T_rounds'])
        
        # Set probability to act (all agents are always active)
        agent.set_probability_to_act(1)

        # Initialize activity array
        active_array = [False] * self.params['max_steps']
        
        for i in range(self.params['max_steps']):
            # Generate a random number between INCLUDEZERO and INCLUDEONE
            r = self.random.uniform(Model.INCLUDEZERO, Model.INCLUDEONE)
            
            # Check if the agent is active in this step
            active_array[i] = r < agent.probability_to_act

        # Save the activity array to the agent
        agent.set_active_array(active_array)
        
        return agent
    
    def calculate_payoff_with_neighbors_globally(self):
        """
        * This function calculates the global wealth of the population for the current step and it is called
        * when finishing the steps. It counts the number of k_I, k_T, and k_U of the whole population 
        * (without taking into account the SN) and apply the utility matrix.
        * 
        * Also, this function updates the individual payoffs for each agent depending on its strategy
        * 此函数计算当前步骤的总体人口财富，并在完成步骤时调用。 
        * 它计算整个总体的k_I，k_T和k_U数（不考虑SN），并应用效用矩阵。
        * 此外，此功能根据其策略更新每个代理商的个人收益

        Calculate the global payoff of all agents by iterating over their strategies and computing their wealth 
        from the utility matrix.
        """

        # Get the current step from the simulation schedule
        current_step = int(self.schedule.get_steps())
        
        # Retrieve relevant parameters for payoff calculation
        tv = self.get_parameters_object().get_tv()
        r_t = self.get_parameters_object().get_r_t()
        r_u = self.get_parameters_object().get_r_u()

        # Denominator used for payoff calculations (sum of trusters and untrustworthy trustees)
        denom = self.k_T_Agents[current_step] + self.k_U_Agents[current_step]

        # Initialize global payoff at the current step
        self.global_payoffs[current_step] = 0.0

        # Iterate through all agents to compute their individual wealth and update global payoff
        for i in range(self.params.nr_agents):
            agent_wealth = 0.0

            # Check if the denominator is greater than zero (i.e., there are trustees)
            if denom > 0:
                agent = self.agents[i]

                # Depending on the agent's strategy, apply the corresponding utility function
                strategy = agent.get_current_strategy()

                if strategy == ModelParameters.TRUSTER:
                    # Truster's utility function: tv * (R_T * (k_T / k_TU) - 1)
                    agent_wealth = tv * ((r_t * (self.k_T_Agents[current_step] / denom)) - 1)

                elif strategy == ModelParameters.TRUSTWORTHY_TRUSTEE:
                    # Trustworthy trustee's utility function: R_T * tv * (k_I / k_TU)
                    agent_wealth = r_t * tv * (self.k_I_Agents[current_step] / denom)

                elif strategy == ModelParameters.UNTRUSTWORTHY_TRUSTEE:
                    # Untrustworthy trustee's utility function: R_U * tv * (k_I / k_TU)
                    agent_wealth = r_u * tv * (self.k_I_Agents[current_step] / denom)

                else:
                    raise ValueError("Fatal Error! Unknown agent strategy. Must be either Truster, Trustworthy Trustee, or Untrustworthy Trustee.")
            else:
                # Log that no trustees are available to perform a transaction (optional)
                pass

            # Save the computed wealth to the agent's payoff array
            agent.set_payoff(agent_wealth, current_step)

            # Add the agent's wealth to the global payoff of the population
            self.global_payoffs[current_step] += agent_wealth

        # Return the global payoff at the current step
        return self.global_payoffs[current_step]
    
    def set_anonymous_agent_apriori(schedule, schedule_counter, social_network):
        """
        * 设置匿名代理先验
        * Adds the anonymous agent to schedule (at the beginning of each step), 
        * which calculates the statistics.
        * 将匿名代理添加到计划中（在每个步骤的开始处），以计算统计信息。

        Adds a repeating task to the schedule. This task resets the colors of the social network's edges
        at the end of each simulation step.
        """
        def step_function(state):
            """
            The step function to be executed at each step in the simulation.
            Resets the colors of edges in the social network if SHOW_SN is enabled.
            """
            if Model.SHOW_SN:
                # Reset all edge colors in the social network
                for edge in social_network.graph.get_each_edge():
                    edge.set_attribute("ui.class", "reset")

        # Schedule the repeating task at the end of each step
        schedule.schedule_repeating(Schedule.EPOCH, schedule_counter, step_function)

    def print_statistics_screen(agents, social_network, params):
        """
        * Prints simple statistics evolution during the time.
	    * 打印一段时间内的简单统计信息演变。
        
        Prints statistics related to agents' strategies and their evolution during the simulation.
        """
        allk_I, allk_T, allk_U = 0, 0, 0

        for i in range(params.nr_agents):
            gamer_agent = agents[i]
            current_strategy = gamer_agent.get_current_strategy()

            if current_strategy == ModelParameters.TRUSTER:
                allk_I += 1
            elif current_strategy == ModelParameters.TRUSTWORTHY_TRUSTEE:
                allk_T += 1
            elif current_strategy == ModelParameters.UNTRUSTWORTHY_TRUSTEE:
                allk_U += 1

            # Obtain number of strategy changes during the simulation
            evolution = gamer_agent.get_evolution_strategies()
            changes = sum(1 for j in range(1, len(evolution)) if evolution[j] != evolution[j - 1])

            # Obtain average degree (number of neighbors) of the agent
            neighbors = social_network.get_neighbors_of_node(gamer_agent.gamer_agent_id)

            # Print agent statistics (commented out for now, but can be re-enabled)
            # print(f"A-{gamer_agent.gamer_agent_id}; {len(neighbors)}; {changes}; {evolution[0]}; {gamer_agent.get_current_strategy()}")

