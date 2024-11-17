import numpy as np

# Load the perfectly trained weights
hard_weights = np.loadtxt('rl_weights_hard.txt')

# Create medium weights (75% of optimal performance)
medium_weights = hard_weights * 0.75 + np.random.normal(0, 0.1, hard_weights.shape)
np.savetxt('rl_weights_medium.txt', medium_weights)

# Create easy weights (50% of optimal performance)
easy_weights = hard_weights * 0.5 + np.random.normal(0, 0.2, hard_weights.shape)
np.savetxt('rl_weights_easy.txt', easy_weights)