#pppp
## Plots original value, exponential averages for some betas and the rolling averages for some windows
#pppp

plot_last = 50
beta_values = [0.058, 0.1, 0.259]
rolling_avg_windows = [50, 28, 10]

# Convert the input string to a list of numbers
input = """
251.01
251.95
...
...
"""
import numpy as np
import matplotlib.pyplot as plt

values = [float(value) for value in input.split("\n") if value.strip()]

# Define the function to calculate the exponential weighted average
def exponential_weighted_average(values, beta):
    ewa = []
    prev_ewa = values[0]
    ewa.append(prev_ewa)
    
    for value in values[1:]:
        ewa_val = beta * value + (1 - beta) * prev_ewa
        ewa.append(ewa_val)
        prev_ewa = ewa_val
    
    return ewa

# Calculate the exponential weighted average for different values of beta
ewa_results = [exponential_weighted_average(values, beta) for beta in beta_values]

rolling_avgs = []
for window_length in rolling_avg_windows:
    rolling_avg = np.convolve(values, np.ones(window_length)/window_length, 'valid')
    rolling_avgs.append(rolling_avg)

# Plot the results
plt.figure(figsize=(15, 9))
# Plot the last 50 original values
plt.plot(range(len(values)-plot_last, len(values)), values[-plot_last:], label="Original Values")

colors=['red', 'green', 'blue', 'black']
linewidths = [0.6, 1.0, 1.4, 1.8]
linestyles = ['--', '-.', ':', '--']

for beta, ewa, lw, color in zip(beta_values, ewa_results, linewidths, colors):
    plt.plot(range(len(ewa)-plot_last, len(ewa)), ewa[-plot_last:], label=f"Beta = {beta}", lw=lw, color=color)

for window_length, rolling_avg, ls, color in zip(rolling_avg_windows, rolling_avgs, linestyles, colors):
    plt.plot(range(len(values)-plot_last, len(values)), rolling_avg[-plot_last:], label=f"Rolling Average (Window = {window_length})", linestyle=ls, color=color)

plt.title("Exponential Weighted Average")
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.show()