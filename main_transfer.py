# Import packages
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Import custom functions
from Supporters import Parameter_update, stage_transfer_equations

# import model components
from Parameters_tanks import Fixed_parameters 
from Model_bborganism import ode_batch_stage, ode_batch_stage_duration
import Model_bborganism
     
# Initialise parameters
par = Parameter_update(Fixed_parameters)

 #%%--- ODE solver Tank 1
# Pre-calculation
V_L = par.V_tank_1 * par.f_hs

# Initial values
c_x0 = 1  # g/L
c_s0 = par.c_s_new
c_o20 = par.c_o2_sat
x_0 = [c_x0, c_s0, c_o20]

# Define transfer trigger event
def transfer_trigger(t, y):
    return y[1]

transfer_trigger.terminal = True

# initiate any event duration timers
event_duration_start = None
duration = 5 #h
trigger = par.mu_max * 0.98 #1/h

event_args = [event_duration_start, duration, trigger]
arg1 = event_duration_start
arg2 = duration
arg3 = trigger


wrap_event_duration = lambda t, x: event_duration(t,x,*event_args)

# define mu_trigger
def event_duration(t, y, *args):
    # specify state variable/calculated value to be tracked:
    y_tracked = y[0]
    
    #Check if parameter has reached trigger
    if y_tracked <= trigger:
        #Inefficiency in ChatGPT code to constantly check... Figure out a seperate timer initiation?
        if event_duration_start is None:
            event_duration_start = t
        # Check whether duration condition has been fulfilled
        if t - event_duration_start >=duration:
                return 0 #trigger event action specified in attributes
            
        else: 
            # define and/or reset start timer (useful for entering new stage with a new duration)
            event_duration_start = None
            
    return 1


#def  event_duration(t, y, event_duration, event_duration_start):
#    return y[1] # <- CHECK WHY THIS ONE

# Define t_span 
t_0, t_end = 0, 40  # h
t_span = np.linspace(t_0, t_end, 200)

# Initiate simulation
sol = solve_ivp(ode_batch_stage_duration, [t_0, t_end], x_0, args=(event_duration_start, duration, trigger), 
                t_eval=t_span, method='RK45', events=(
                    lambda t, x: transfer_trigger(t,x), 
                    wrap_event_duration))

# Get the number of evaluations of the solver
print('Number of evaluations: {:.0f}'.format(sol.nfev))

# Retrieve solution
t  = sol.t          # Time points
c_x = sol.y[0, :]    # Concentration of X (gX/L)
c_s = sol.y[1, :]    # Concentration of S (gS/L)
c_o2 = sol.y[2, :]    # Concentration of S (gS/L)

plt.subplot(2,3,1)
plt.plot(t, c_x)
plt.legend('X')
plt.xlabel('Time (h)')
plt.ylabel('Biomass (g/L)')

plt.subplot(2,3,2)
plt.plot(t, c_s)
plt.legend('S')
plt.xlabel('Time (h)')
plt.ylabel('Substrate (g/L)')

plt.subplot(2,3,3)
plt.plot(t, c_o2)
plt.legend('O')
plt.xlabel('Time (h)')
plt.ylabel('Oxygen (g/L)')


 #%%--- Transfer calculations
x_0, V_L_new = stage_transfer_equations (sol, par, V_L)

 #%%--- ODE solver Tank 2
t_0, t_end = 0, 40  # h
t_span = np.linspace(t_0, t_end, 200)

# Initiate simulation
sol2 = solve_ivp(ode_batch_stage, [t_0, t_end], x_0, t_eval=t_span, method='RK45', events=transfer_trigger)

# Get the number of evaluations of the solver
print('Number of evaluations: {:.0f}'.format(sol2.nfev))

# Retrieve solution
t2  = sol2.t          # Time points
c_x2 = sol2.y[0, :]    # Concentration of X (gX/L)
c_s2 = sol2.y[1, :]    # Concentration of S (gS/L)
c_o22 = sol2.y[1, :]    # Concentration of O2 (gS/L)


plt.subplot(2,3,4)
plt.plot(t2, c_x2)
plt.legend('X')
plt.xlabel('Time (h)')
plt.ylabel('Biomass 2 (g/L)')

plt.subplot(2,3,5)
plt.plot(t2, c_s2)
plt.legend('S')
plt.xlabel('Time (h)')
plt.ylabel('Substrate 2 (g/L)')

plt.subplot(2,3,6)
plt.plot(t2, c_o22)
plt.legend('O')
plt.xlabel('Time (h)')
plt.ylabel('Oxygen 2 (g/L)')

