import matplotlib.pyplot as plt

# define input nodes
input_nodes = {(2.5, 2.5, 1.0): 1, (2.5, 10.0, 1.0): 2, (2.5, 17.5, 1.0): 3, (6.25, 6.25, 1.0): 4}

# create figure and axis objects
fig, ax = plt.subplots()

# plot nodes on axis
for node, node_num in input_nodes.items():
    ax.text(node[0], node[1], str(node_num), ha='center', va='center', fontsize=12)

# add labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

# set axis limits
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)

# display the plot
plt.show()
