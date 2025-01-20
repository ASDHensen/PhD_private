
# Define ODE-system
def ode_batch_stage(t, x):
    # Unpack variabels
    from Parameters_tanks import Fixed_parameters as par
    from Supporters import Parameter_update
    # Initialise parameters
    par = Parameter_update(par)
    
    # State variables
    c_x, c_s, c_o2 = x

    # Algebraic equations
    mu = par.mu_max * (c_s / (c_s + par.K_s)) * (c_o2/(c_o2+par.K_o2))
    q_s = par.q_s_max * (c_s / (c_s + par.K_s))
    q_o2 = par.q_o2_max * (c_o2/(c_o2+par.K_o2))
    T_o2 = par.kLa * (par.c_o2_sat-c_o2)

    # Differential Equations
    dcxdt = c_x * mu 
    dcsdt = -c_x * q_s
    dco2dt = T_o2 - c_x * q_o2 

    dx = [dcxdt, dcsdt, dco2dt]
    return dx

# Define ODE-system
def ode_batch_stage_duration(t, x, trigger, duration, event_duration_start):
    # Unpack variabels
    from Parameters_tanks import Fixed_parameters as par
    from Supporters import Parameter_update
    # Initialise parameters
    par = Parameter_update(par)
    
    # State variables
    c_x, c_s, c_o2 = x

    # Algebraic equations
    mu = par.mu_max * (c_s / (c_s + par.K_s)) * (c_o2/(c_o2+par.K_o2))
    q_s = par.q_s_max * (c_s / (c_s + par.K_s))
    q_o2 = par.q_o2_max * (c_o2/(c_o2+par.K_o2))
    T_o2 = par.kLa * (par.c_o2_sat-c_o2)

    # Differential Equations
    dcxdt = c_x * mu 
    dcsdt = -c_x * q_s
    dco2dt = T_o2 - c_x * q_o2 

    dx = [dcxdt, dcsdt, dco2dt]
    return dx


          

