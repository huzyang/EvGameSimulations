from money_model import MoneyModel
# Data visualization tools.
import seaborn as sns


all_wealth = []
# This runs the model 100 times, each model executing 10 steps.
for j in range(10):
    # Run the model
    model = MoneyModel(10)
    for i in range(10):
        model.step()

    # Store the results
    for agent in model.schedule.agents:
        all_wealth.append(agent.wealth)

# Use seaborn
g = sns.histplot(all_wealth, discrete=True)
g.set(title="Wealth distribution", xlabel="Wealth", ylabel="Number of agents")