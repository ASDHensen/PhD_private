class Parameter_update:
    def __init__(self, dictionary_parameters):
        self.update_attributes(dictionary_parameters)
   
    def update_attributes(self, new_dict):
        '''
        Constructs object containing attrubutes named by the keys of the
        processed dictionary and assigns the corresponding value.  

        Parameters
        ----------
        new_dict : dictionary
            Parameter dictionary to be used in ODE simulation.

        Returns
        -------
        None.

        '''
        for key, value in new_dict.items():
            setattr(self, key, value)

 #%%--- Transfer calculations
def stage_transfer_equations (sol, par, Volume):
    '''
    Calculates initial values for state variable in subsequent tank in seed 
    train, combining the initial medium settings from the parameter dictionary
    with the added broth from the previous tank. 

    Parameters
    ----------
    sol : scipy.integrate._ivp.ivp.OdeResult
        Object that contains simulated time series from ODE simulation and the
        events that took place. 
    par : Supporters.Parameter_update
        Object that contains attributes with values aconstructed form key value
        pairs in a model parameter dictionary.
    Volume : float
        Broth volume [L] at end of stage. 

    Returns
    -------
    list
        Returns initial values for state variables for simulation of next 
        tank stage.

    '''
    # Retrieve solution
    t  = sol.t          # Time points
    c_x = sol.y[0, :]    # Concentration of X (gX/L)
    c_s = sol.y[1, :]    # Concentration of S (gS/L)
    c_o2 = sol.y[2, :]    # Concentration of O2 (go2/L)
    
    c_x_end = c_x[-1]
    c_s_end = c_s[-1]
    c_o2_end = c_o2[-1]
    
    '''
    def stage_transfer_equations ():
        # Unpack and define values from previous stage
        # PLACEHOLDER
    '''
    V_L = Volume
    V_L_old = V_L           # Later to be replaced with V_L_end when I implement multiple stages
    V_L_new = (par.V_tank_2 * par.f_hs) - V_L_old
    
    c_x0 = (c_x_end * V_L_old)/(V_L_old + V_L_new)
    c_s0 = ((c_s_end * V_L_old)+(par.c_s_new*V_L_new))/(V_L_old + V_L_new)
    c_o22 = ((c_o2_end * V_L_old)+(par.c_o2_sat*V_L_new))/(V_L_old + V_L_new)
    
    x_0 = [c_x0, c_s0, c_o22]
    return [x_0, V_L_new]

def event_duration(t, y, trigger, duration, event_duration_start):
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
    

