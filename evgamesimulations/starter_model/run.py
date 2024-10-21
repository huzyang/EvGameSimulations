from money_model import MoneyModel

# Data visualization tools.
import seaborn as sns

# Has multi-dimensional arrays and matrices. Has a large collection of
# mathematical functions to operate on these arrays.
import numpy as np

# Data manipulation and analysis.
import pandas as pd

all_wealth = []
# This runs the model 100 times, each model executing 10 steps.
# for j in range(5):
# Run the model
model = MoneyModel(100, 10, 10)
for i in range(10):
    model.step()

    # Store the results
    for agent in model.schedule.agents:
        all_wealth.append(agent.wealth)

# Use seaborn
# g = sns.histplot(all_wealth, discrete=True)
# g.set(title="Wealth distribution", xlabel="Wealth", ylabel="Number of agents")

# 100 agents on a 10x10 grid
agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell_content, (x, y) in model.grid.coord_iter():
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
# Plot using seaborn, with a size of 5x5
g = sns.heatmap(agent_counts, cmap="viridis", annot=True, cbar=False, square=True)
g.figure.set_size_inches(4, 4)
g.set(title="Number of agents on each cell of the grid")
