# To be run on a free Colab instance
#Jane street robot flag capture thing

import cupy as cp
from tqdm import tqdm

def optimal_move_distance_erin(num_simulations):
    move_distances = cp.linspace(0, 1, 10000, dtype=cp.float64)  # Use double precision
    best_distance = cp.inf
    best_d = 0

    # Simulate all at once for each distance
    r = cp.random.uniform(0, 1, num_simulations, dtype=cp.float64)
    theta = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)

    for d in tqdm(move_distances, desc="Optimizing Erin"):
        x_flag = r * cp.cos(theta)
        y_flag = r * cp.sin(theta)
        x_move = d * cp.cos(theta)
        y_move = d * cp.sin(theta)
        distance_move = cp.sqrt((x_flag - x_move)**2 + (y_flag - y_move)**2)
        avg_move = cp.mean(distance_move)

        if avg_move < best_distance:
            best_distance = avg_move
            best_d = d.get()

    return best_d

def optimal_move_distance_aaron(num_simulations):
    move_distances = cp.linspace(0, 1, 10000, dtype=cp.float64)  # Use double precision
    best_distance = cp.inf
    best_d = 0

    # Simulate all at once for each distance
    r = cp.random.uniform(0, 1, num_simulations, dtype=cp.float64)
    theta_flag = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)
    theta_move = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)

    for d in tqdm(move_distances, desc="Optimizing Aaron"):
        x_flag = r * cp.cos(theta_flag)
        y_flag = r * cp.sin(theta_flag)
        x_move = d * cp.cos(theta_move)
        y_move = d * cp.sin(theta_move)
        distance_move = cp.sqrt((x_flag - x_move)**2 + (y_flag - y_move)**2)
        avg_move = cp.mean(distance_move)

        if avg_move < best_distance:
            best_distance = avg_move
            best_d = d.get()

    return best_d

def simulate_winning_probability(num_simulations, d_erin, d_aaron):
    # Batch generate all random variables
    r = cp.random.uniform(0, 1, num_simulations, dtype=cp.float64)
    theta = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)
    theta_aaron = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)

    d_erin = cp.asarray(d_erin)
    d_aaron = cp.asarray(d_aaron)

    x_erin = d_erin * cp.cos(theta)
    y_erin = d_erin * cp.sin(theta)
    x_flag = r * cp.cos(theta)
    y_flag = r * cp.sin(theta)
    x_aaron = d_aaron * cp.cos(theta_aaron)
    y_aaron = d_aaron * cp.sin(theta_aaron)

    dist_erin = cp.sqrt((x_erin - x_flag)**2 + (y_erin - y_flag)**2)
    dist_aaron = cp.sqrt((x_aaron - x_flag)**2 + (y_aaron - y_flag)**2)

    # Calculate wins for Aaron
    wins_aaron = cp.sum(dist_aaron < dist_erin)

    return (wins_aaron / num_simulations).get()

# Main simulation settings
num_simulations_optimal = 1000000
num_simulations_probability = 100000000  

d_erin = optimal_move_distance_erin(num_simulations_optimal)
d_aaron = optimal_move_distance_aaron(num_simulations_optimal)

aaron_wins_probability = simulate_winning_probability(num_simulations_probability, d_erin, d_aaron)

print(f"Optimal Move Distance for Erin: {d_erin:.10f}")
print(f"Optimal Move Distance for Aaron: {d_aaron:.10f}")
print(f"Aaron's Probability of Winning: {aaron_wins_probability:.10f}")
