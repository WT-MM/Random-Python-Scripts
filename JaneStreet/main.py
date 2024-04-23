import cupy as cp
from tqdm import tqdm

def optimal_move_distance_erin(num_simulations):
    move_distances = cp.linspace(0.69, 0.71, 100000, dtype=cp.float64)  # Use double precision
    best_distance = cp.inf
    best_d = 0

    # Simulate all at once for each distance
    r = cp.sqrt(cp.random.uniform(0, 1, num_simulations, dtype=cp.float64))
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
    move_distances = cp.linspace(0, 0.1, 100000, dtype=cp.float64)  # Use double precision
    best_distance = cp.inf
    best_d = 0

    # Simulate all at once for each distance
    r = cp.sqrt(cp.random.uniform(0, 1, num_simulations, dtype=cp.float64))
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

def simulate_winning_probability(num_simulations, d_erin, d_aaron, num_batches=5, alt_step_ratio=0.5, alt_threshold=0.125):
    total = 0
    for _ in tqdm(range(num_batches), desc="Simulating games"):
    #for _ in range(num_batches):

        r = cp.sqrt(cp.random.uniform(0, 1, num_simulations, dtype=cp.float64))
        theta = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)
        theta_aaron = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)

        d_erin = cp.asarray(d_erin)
        d_aaron = cp.asarray(d_aaron)

        x_erin = d_erin * cp.cos(theta)
        y_erin = d_erin * cp.sin(theta)
        x_flag = r * cp.cos(theta)
        y_flag = r * cp.sin(theta)

        alt_r = alt_step_ratio * r
        alt_theta_aaron = cp.random.uniform(0, 2 * cp.pi, num_simulations, dtype=cp.float64)

        x_aaron = cp.where(r > alt_threshold, alt_r * cp.cos(alt_theta_aaron), d_aaron * cp.cos(theta_aaron))
        y_aaron = cp.where(r > alt_threshold, alt_r * cp.sin(alt_theta_aaron), d_aaron * cp.sin(theta_aaron))

        dist_erin = cp.sqrt((x_erin - x_flag)**2 + (y_erin - y_flag)**2)
        dist_aaron = cp.sqrt((x_aaron - x_flag)**2 + (y_aaron - y_flag)**2)

        wins_aaron = cp.sum(dist_aaron < dist_erin)
        total += (wins_aaron / num_simulations).get()

    return total / num_batches

def optimize_parameters(num_simulations, d_erin, d_aaron, num_batches, ratio_range, threshold_range, num_steps):
    best_ratio = None
    best_threshold = None
    best_probability = 0
    ratios = cp.linspace(ratio_range[0], ratio_range[1], num_steps)
    thresholds = cp.linspace(threshold_range[0], threshold_range[1], num_steps)

    for ratio in tqdm(ratios, desc="Optimizing within ratios"):
        for threshold in thresholds:
            #print(f"Evaluating alt_step_ratio={ratio:.10f}, alt_threshold={threshold:.10f}")
            probability = simulate_winning_probability(num_simulations, d_erin, d_aaron, num_batches, alt_step_ratio=ratio, alt_threshold=threshold)
            #print(f"Winning Probability: {probability:.10f}")

            if probability > best_probability:
                best_probability = probability
                best_ratio = ratio
                best_threshold = threshold

    return best_ratio, best_threshold, best_probability

def optimize():
  best_ratio, best_threshold, best_probability = optimize_parameters(
      num_simulations=100,
      d_erin=(1/cp.sqrt(2)),
      d_aaron=0,
      num_batches=100,
      ratio_range=(0.1, 1.0),
      threshold_range=(0.0, 0.5),
      num_steps=100
  )

  print(f"Best settings: alt_step_ratio={best_ratio}, alt_threshold={best_threshold} with probability {best_probability}")

def simulate():

  # Main simulation settings
  num_simulations_optimal = 5000#000
  num_simulations_probability = 100000000  # Increased simulations for higher precision

  # Compute optimal distances using GPU
  #d_erin = optimal_move_distance_erin(num_simulations_optimal)
  #d_aaron = optimal_move_distance_aaron(num_simulations_optimal)

  d_aaron = 0.000000000000000000
  d_erin = 1/cp.sqrt(2)
  #aaron_win_prob_weird = simulate_winning_probability(num_simulations_probability, d_erin, d_aaron, num_batches=1000)
  #d_erin = 0.5
  # Compute winning probability using GPU
  aaron_wins_probability = simulate_winning_probability(num_simulations_probability, d_erin, d_aaron, num_batches=1000, alt_step_ratio=1.0, alt_threshold=(1/(2*cp.sqrt(2))))

  # Output results
  #print(f"Optimal Move Distance for Erin: {d_erin:.10f}")
  #print(f"Optimal Move Distance for Aaron: {d_aaron:.10f}")
  print(f"Aaron's Probability of Winning: {aaron_wins_probability:.12f}")
  #print(f"Aaron's Probability of Winning with weird num: {aaron_win_prob_weird:.10f}")


simulate()

#0.1928002120
#0.192800667748
