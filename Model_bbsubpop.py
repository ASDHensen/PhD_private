def ode_batch_subpop (t, x):
    # Unpack variabels
    from Parameters_tanks import Fixed_parameters, subpop_parameters
    from Supporters import Parameter_update
    # Initialise parameters
    par = Fixed_parameters | subpop_parameters
    par = Parameter_update(par)
    
    # State Variables, alphabatised
    (
        c_o2,
        c_p,
        c_s, 
        c_x_lp,
        c_x_np,
        c_x_nv, 
        c_x_op,
        Gen
    )= x
    
    # Algebraic equations (all passed parameters given in alphabetised order
    # replace par w/individual parameters where there's multiple populations)
    mu = mu_monod(c_o2, c_s, par)
    q_p = q_p_growth_related(c_x_op, mu, par)
    q_p_degen = q_p_degeneration_burden(c_x_lp, mu, par)
    q_s = q_s_affinity(c_s, par)
    q_s_prod = q_s_HP(mu, q_p, par)
    q_s_degen = q_s_HP(mu, q_p_degen, par)
    q_o2 = q_o2_affinity(c_o2, par)
    T_o2 = T_o2_total(c_o2, par)
    
    # placeholder for the subpopulation transfer rates
    k_lp = low_producer_transfer_rate(Gen, par)
    k_nv = non_viable_transfer_rate(Gen, par)

    
    # During construction, assume that all populations consume at the same rates
    
    # Differential equations
    
    dc_o2dt = T_o2 - (c_x_lp + c_x_np + c_x_nv + c_x_op) * q_o2
    dc_pdt = c_x_lp * q_p_degen + c_x_op * q_p
    dc_sdt = -c_x_np * q_s - c_x_lp * q_s_degen - c_x_op * q_s_prod
    dc_x_lpdt = c_x_lp * mu + c_x_op * k_lp - c_x_lp * k_np
    dc_x_npdt = c_x_np * mu + c_x_lp * k_np
    dc_x_nvdt = c_x_nv * 0 + c_x_op * k_nv + c_x_lp * k_nv + c_x_np * k_nv
    dc_x_opdt = c_x_op * mu - c_x_op * k_lp - c_x_op * k_nv
    dGendt = mu/np.log(2)
    
    
    dx = [dc_o2dt, dc_pdt, dc_sdt, dc_x_lpdt, dc_x_npdt, dc_x_nvdt, dc_x_opdt, dGendt]
    return dx

# Listing algebraic equations that can be selected for in the model. Parameters will be kept in subpop_parameters as a working file
# Some of these will also be re-used per subpopulation with different passed parameters.

# Note, for consistency sake, better to write parmateres as par.name and pass the whole par as constructed in the main ODE model.


def mu_monod(c_o2, c_s, par):
    mu = par.mu_max * (c_s / (c_s + par.K_s)) * (c_o2/(c_o2+par.K_o2))
    return mu

def q_s_affinity(c_s, par):
    q_s = par.q_s_max * (c_s / (c_s + par.K_s))
    return q_s

def q_s_HP():
    
    return 

def q_o2_affinity():
    return

def q_p_growth_related():
    #Leudeking piret? Monod-esque?
    return

def q_p_degeneration_generations():
    return 

def q_p_degeneration_burden():
    return

def ms_burden():
    return

def ms_generations(): 
    return

def low_producer_transfer_rate(Gen, par):
    k_lp = par.k_lp
    # placeholder dependency 
    '''
    k_lp = par.alpha_lp * Gen + par.beta_lp * tau_stress
    '''
    return k_lp

def non_viable_transfer_rate(Gen, par):
    k_np = par.k_np
    return k_np

'''
def tau_doubling(mu):
    tau_d = np.log(2)/mu 
    return tau_d
'''

def T_o2_total(c_o2, par):
    T_o2 = par.kLa * (par.c_o2_sat-c_o2)
    return
#Functions for stress left out, next stage. 







