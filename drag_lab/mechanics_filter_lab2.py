# Mechanics filter lab part 2 : Alex P. and Feodor

import matplotlib.pyplot as plt
import pandas as pd 

#Part 1: Extracting data from programming assignment

experiment_data  = [1.05, 1.04, 1.04, 1.03, 1.02, 1.01, 0.99, 0.97, 0.95, 0.93, 0.9, 0.87, 0.85, 0.81, 0.78, 0.75, 0.71, 0.67, 0.63, 0.59, 0.55, 0.5, 0.45, 0.41, 0.36] 
# All the positions recorded during the actual experiment
experiment_data = [round(elem-0.36,2) for elem in experiment_data] #Since the data reaches "bottom" at 0.36, shift all values by this.
y = experiment_data[0] #setting initial y (to be used later), to match with initial y of experiemnt 
avg_terminal_velocity = -1.71954887 
#coefficient obtained from programming assigment at 3 filters using ployfit function

# TODO: Drag coefficient constant, for drop with 3 filters

m = 2.6/1000 # Mass measured in class, divided by 1000 to attain mass in kg (was in g)
g = 9.8
p = 1.204 #at 20 degrees celsius
A = 0.0162733 #suface area of our filter
v = avg_terminal_velocity
C = (2*m*g)/(p*A*(v**2)) #Drag equation, found in lab sheet
print(C)

'''
For uncertainty, we will take into account the uncertainty on the mass which is
0.05 grams (since we used a digital scale). With this our range of masses is 
2.55 to 2.65

Additionally in the air density calculator website
https://www.engineeringtoolbox.com/air-density-specific-weight-d_600.html
it is said that there is an uncertainty of +/- 0.2%
Which for our air density of 1.204 gives us a range from 1.202 to 1.206

Since in the drag equation, mass is in the numerator and air density is
in the denominator. The highest possible value of C can be calculated
when mass is the largest and air density is the lowest
'''
m = 2.65/1000 # highest range for mass
g = 9.8
p = 1.202 #lowest range for air density
A = 0.0162733
v = avg_terminal_velocity
max_C = (2*m*g)/(p*A*(v**2))

uncertainty = C - max_C
print(uncertainty) # Final uncertainty (for both +/-)


'''
Part 2: 
Define a function, Euler's method.

Initilaize a dictionary, with keys that are strings (postion, time and velocity).
The values associated with the keys are list containing entries of their respecitve values
(according to their key names). The first entry in the position key starts at the desired dropping height
while the time and velocity have a first entry of 0 (since there is no time elapsed at the start,
and the initial velocity is zero).

While the position is not negative (does not go below the ground):
1. Compute the acceleration using the drag equation
2. Record the next velocity entry, by multiplying computed acceleration
   and the specified time interval (t) and adding this product to 
   the previous velocity entry
3. Record the next position entry, by multiplying the most recent velocity
   entry by value t and adding this product to the previous position entry
4. Record the next time entry, by adding value t to the previous
'''
def eulersMethod(m,A,p,C,t,y):  
    data = {'position(m)': [y], 'time(s)': [0], 'velocity(m/s)': [0]  }
    while data['position(m)'][-1] > 0:
        a = -9.8 + ( (C*p*A*(data['velocity(m/s)'][-1]**2)/ (2*m)))
        data['velocity(m/s)'] += [data['velocity(m/s)'][-1] + (a*t)]
        data['position(m)'] += [data['position(m)'][-1] + (data['velocity(m/s)'][-1]*t)]
        data['time(s)'] += [data['time(s)'][-1] + t]

    return data

t = 0.02 #since original experiment was measure in 0.02 second intervals
data = eulersMethod(m,A,p,C,t,y)
data = pd.DataFrame(data)
data = data[:-1] #Since last entry is when the position becomes negative


data.plot(x = "time(s)", y = 'position(m)', label = "Eulers graph") # Plotting graph using eulers method

index_num = min([len(data['time(s)']),len(experiment_data)]) #in case the number of time intervals needed doesn't mathch up with number of recorded positions for the experiment
xpoints = data['time(s)'][:index_num]
ypoints = experiment_data[:index_num] 
plt.plot(xpoints, ypoints, label = 'Experiment graph')

plt.legend()
plt.ylabel('Position (m)')
plt.xlabel('Time (s)')
plt.show()