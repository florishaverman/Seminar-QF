# from ortools.linear_solver import pywraplp
# from ortools.init import pywrapinit
import hedging
import cashflows

def main():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    #problem settings
    maxBond = 1000000
    # Create hedging products
    maxMonths = 12
    bonds = hedging.createHedgingBonds(12)
    #Generate Cashflows to match
    Rcashflows = cashflows.getAllSimCashflows(1)[0]
    
    x = []
    for i in range(maxMonths):
        x.append(solver.NumVar(0, maxBond, 'x' + str(i)))


    print('Number of variables =', solver.NumVariables())

    # Create a linear constraint, 0 <= x + y <= 2.
    ct = solver.Constraint(0, 20, 'ct')
    for i in range(maxMonths):
        ct.SetCoefficient(x[i], 1)

    print('Number of constraints =', solver.NumConstraints())

    # Create the objective function, 3 * x + y.
    objective = solver.Objective()
    for i in range(maxMonths):
        objective.SetCoefficient(x[i], 1)
    objective.SetMaximization()


    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    for i in range(maxMonths):
        print(f'x {i} =', x[i].solution_value())


# if __name__ == '__main__':
#     pywrapinit.CppBridge.InitLogging('basic_example.py')
#     cpp_flags = pywrapinit.CppFlags()
#     cpp_flags.logtostderr = True
#     cpp_flags.log_prefix = False
#     pywrapinit.CppBridge.SetFlags(cpp_flags)

    #main()