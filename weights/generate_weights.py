import numpy as np
import os

def generate_initial_weights():
    # Create weights directory if it doesn't exist
    if not os.path.exists('weights'):
        os.makedirs('weights')

    # Generate weights for each difficulty
    # Easy weights - more random
    easy_weights = np.random.uniform(-0.1, 0.1, (19683,))
    np.savetxt('weights/rl_weights_easy.txt', easy_weights)

    # Medium weights - partially trained
    medium_weights = np.random.uniform(-0.3, 0.3, (19683,))
    np.savetxt('weights/rl_weights_medium.txt', medium_weights)

    # Hard weights - fully trained
    hard_weights = np.random.uniform(-0.5, 0.5, (19683,))
    # Add some strategic bias
    hard_weights[4] = 0.8  # Center position preference
    hard_weights[0] = 0.6  # Corner preference
    hard_weights[2] = 0.6
    hard_weights[6] = 0.6
    hard_weights[8] = 0.6
    np.savetxt('weights/rl_weights_hard.txt', hard_weights)

if __name__ == "__main__":
    generate_initial_weights()
    print("Weight files generated successfully!")