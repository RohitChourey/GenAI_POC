import numpy as np  
from scipy.optimize import minimize  
  
# Define the objective function  
def objective(x):  
    E, D = x  
    return E + D  
  
# Define the constraints  
def constraints(x, RE, RD, p_e, p_d, Goal):  
    E, D = x  
    return [  
        {'type': 'eq', 'fun': lambda x:  Goal - (((12*E)*((((1+RE)**Years)-1)/RE)) + ((12*D)*((((1+RD)**Years)-1)/RD)))},  
        {'type': 'eq', 'fun': lambda x:  E - p_e*(E+D)},  
        {'type': 'eq', 'fun': lambda x:  D - p_d*(E+D)}  
    ]  
  
# Define a function to solve the problem  
def solve(RE, RD, Years, p_e, p_d, Goal):  
    # Initial guess  
    x0 = np.array([Goal*p_e/12/Years, Goal*p_d/12/Years])  # Initial guess is proportioned according to p_e and p_d  
  
    # Bounds for the variables  
    bnds = ((0, None), (0, None))  
  
    # Solve the problem  
    res = minimize(objective, x0, args=(), bounds=bnds, method='SLSQP', constraints=constraints(x0, RE, RD, p_e, p_d, Goal))  
  
    # Return the solution  
    return (res.x[0]+res.x[1])  
  
# Ask for user inputs for the constants  
RE = float(input("Enter yearly return in equity (as a decimal, e.g., 0.07 for 7%): "))   
RD = float(input("Enter yearly return in debt (as a decimal, e.g., 0.05 for 5%): "))    
p_e = float(input("Enter equity allocation (as a decimal, e.g., 0.6 for 60%): "))   
p_d = 1-p_e #float(input("Enter debt allocation (as a decimal, e.g., 0.4 for 40%): "))   
Goal = float(input("Enter retirement goal: "))   
Years = int(input("Enter years to achieve goal: "))  
  
# Solve the problem with the original parameters  
original_solution = solve(RE, RD, Years, p_e, p_d, Goal)  
print(f'Original solution: {original_solution}')  
  
# Define a list of perturbations  
perturbations = [0.9, 0.95, 1.05, 1.1]  
  
# Perturb each parameter and re-solve the problem  
for perturbation in perturbations:  
    perturbed_solution = solve(RE*perturbation, RD*perturbation, Years, p_e*perturbation, p_d*perturbation, Goal*perturbation)  
    print(f'Perturbation: {perturbation}, solution: {perturbed_solution}')  
