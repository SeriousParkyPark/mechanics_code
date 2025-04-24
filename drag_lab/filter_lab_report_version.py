# Mechanics filter lab part 2 : Alex P. and Feodor
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
terminal_velocities_lst = [
 -0.7552631578947369,
 -0.6763157894736844,
 -0.6402255639097749,
 -0.7315789473684213,
 -0.7131578947368422,
 -0.6887218045112791,
 -0.7244360902255631,
 -0.7661654135338344,
 -0.7240601503759397,
 -0.6492481203007521
 ] # All terminal velocities recorded for single filter experiment
experiment_data  = [
    1.01, 1.00, 0.99, 0.99, 0.98, 0.96,0.95, 0.94, 0.92, 0.91,
    0.89, 0.87, 0.86, 0.84, 0.82, 0.80, 0.77, 0.75, 0.72, 0.70,
    0.67, 0.65, 0.62, 0.59, 0.56, 0.54, 0.51, 0.48, 0.45, 0.42,
    0.39, 0.35, 0.32, 0.29, 0.26, 0.23, 0.20, 0.17, 0.13
] # All the positions recorded during the actual experiment (for 3 coffee filters)

experiment_data = [round(elem-0.13,2) for elem in experiment_data] #Since the data reaches "bottom" at 0.13, shift all values by this.
y = experiment_data[0] #setting initial y of simulation (to be used later), to match with initial y of experiment 
avg_terminal_velocity = sum(terminal_velocities_lst)/len(terminal_velocities_lst)


m = 8.7/1000/10 # Mass of 10 filters, to reduce uncertainty (diving by 10 to calculate mass for a single filter)
g = 9.8
p = 1.192 # At 23 degrees celsius
A = 0.0162733 # Suface area of our filter
v = avg_terminal_velocity
C = (2*m*g)/(p*A*(v**2)) # Drag equation, found in lab sheet
print(C)


def eulers_method(y, v, c, p, A, mass, arr, acceleration, t):
    acceleration = -9.8 + (c * p * A * v**2) / (2 * mass)
    v += acceleration * t
    y += v * t
    arr = np.append(arr, y)
    return v, y, acceleration, arr

# Constants
arr = np.array([])
t = 0.02 # Intervals of time in which position was recorded in orignal experiment
m = m*3 # Since now we are simulating for 3 filters
acceleration = -9.8
v = 0
arr = np.append(arr, y)

# Euler's Method Iterations
while y > 0:
    v, y, acceleration, arr = eulers_method(y, v, C, p, A, m, arr, acceleration, t)

print(arr)


#Plotting Data
data = pd.DataFrame({
    'time(s)': [i * 0.02 for i in range(len(arr))],
    'position(m)': arr
})
data = data[:-1] 
print(data)


data.plot(x = "time(s)", y = 'position(m)', label = "Eulers graph") 

index_num = min([len(data['time(s)']),len(experiment_data)]) #in case the amount of time intervals needed differ between experiment and simulation
xpoints = data['time(s)'][:index_num]
ypoints = experiment_data[:index_num] 
plt.plot(xpoints, ypoints, label = 'Experiment graph')

plt.legend()
plt.ylabel('Position (m)')
plt.xlabel('Time (s)')
plt.show()