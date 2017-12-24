
# coding: utf-8

# In[ ]:

import sys
from ortools.constraint_solver import pywrapcp

def main():
    solver = pywrapcp.Solver('schedule_shifts')
    n_nurses = 4
    n_shifts = 4
    n_days = 7
    
    # creating the shifts decision variable
    shifts = {}
    for nrs in range(n_nurses):
        for day in range(n_days):
            shifts[(nrs, day)] = solver.IntVar(0, n_shifts-1)
    shifts_flat = [shifts[(nrs, day)] for nrs in range(n_nurses) for day in range(n_days)]
    
    # creating the nurses decision variable
    nurses = {}
    for shft in range(n_shifts):
        for day in range(n_days):
            nurses[(shft, day)] = solver.IntVar(0, n_nurses)
    
    
    ## Linking shifts and nurses in each day
    for day in range(n_days):
        
        # go into the nurses variable and lay them out for the day
        nurses_for_day = [nurses[(shft, day)] for shft in range(n_shifts)]
        
        # go into the shifts variable, and for each shift, link the one \
        # corresponding to the right nurse, to the nurse for the day above
        for nrs in range(n_nurses):
            s = shifts[(nrs, day)]
            solver.Add(s.IndexOf(nurses_for_day)==nrs)
    
    ## CONSTRAINTS ##
    
    # On each day, all nurses are assigned to different shifts
    for day in range(n_days):
        solver.Add(solver.AllDifferent([shifts[(nrs, day)] for nrs in range(n_nurses)]))
        solver.Add(solver.AllDifferent([nurses[(shft, day)] for shft in range(n_shifts)]))

    # Each nurse works five or six days a week.
    for nrs in range(n_nurses):
        solver.Add(solver.Sum([shifts[(nrs, day)]>0 for day in range(n_days)]) >= 5)
        solver.Add(solver.Sum([shifts[(nrs, day)]>0 for day in range(n_days)]) <= 6)

    
    ## No shift is staffed by more than two different nurses in a week.
    works_shift = {}
    for nrs in range(n_nurses):
        for shft in range(n_shifts):
            works_shift[(nrs, shft)] = solver.BoolVar()
    
    for nrs in range(n_nurses):
        for shft in range(n_shifts):
            solver.Add(works_shift[(nrs, shft)] == solver.Max([shifts[(nrs, day)]==shft for day in range(n_days)]))
    
    for shft in range(n_shifts):
        solver.Add(solver.Sum([works_shift[(nrs, shft)] for nrs in range(n_nurses)]) <=2)

    # If a nurse works shifts 2 or 3 on a given day, he must also work \
    # the same shift either the previous day or the following day.
    solver.Add(solver.Max(nurses[(2, 0)] == nurses[(2, 1)], nurses[(2, 1)] == nurses[(2, 2)]) == 1)
    solver.Add(solver.Max(nurses[(2, 1)] == nurses[(2, 2)], nurses[(2, 2)] == nurses[(2, 3)]) == 1)
    solver.Add(solver.Max(nurses[(2, 2)] == nurses[(2, 3)], nurses[(2, 3)] == nurses[(2, 4)]) == 1)
    solver.Add(solver.Max(nurses[(2, 3)] == nurses[(2, 4)], nurses[(2, 4)] == nurses[(2, 5)]) == 1)
    solver.Add(solver.Max(nurses[(2, 4)] == nurses[(2, 5)], nurses[(2, 5)] == nurses[(2, 6)]) == 1)
    solver.Add(solver.Max(nurses[(2, 5)] == nurses[(2, 6)], nurses[(2, 6)] == nurses[(2, 0)]) == 1)
    solver.Add(solver.Max(nurses[(2, 6)] == nurses[(2, 0)], nurses[(2, 0)] == nurses[(2, 1)]) == 1)
    solver.Add(solver.Max(nurses[(3, 0)] == nurses[(3, 1)], nurses[(3, 1)] == nurses[(3, 2)]) == 1)
    solver.Add(solver.Max(nurses[(3, 1)] == nurses[(3, 2)], nurses[(3, 2)] == nurses[(3, 3)]) == 1)
    solver.Add(solver.Max(nurses[(3, 2)] == nurses[(3, 3)], nurses[(3, 3)] == nurses[(3, 4)]) == 1)
    solver.Add(solver.Max(nurses[(3, 3)] == nurses[(3, 4)], nurses[(3, 4)] == nurses[(3, 5)]) == 1)
    solver.Add(solver.Max(nurses[(3, 4)] == nurses[(3, 5)], nurses[(3, 5)] == nurses[(3, 6)]) == 1)
    solver.Add(solver.Max(nurses[(3, 5)] == nurses[(3, 6)], nurses[(3, 6)] == nurses[(3, 0)]) == 1)
    solver.Add(solver.Max(nurses[(3, 6)] == nurses[(3, 0)], nurses[(3, 0)] == nurses[(3, 1)]) == 1)
    
    
    #### TIM TO SOLVE ###
    db = solver.Phase(shifts_flat,
                     solver.CHOOSE_FIRST_UNBOUND,
                     solver.ASSIGN_MIN_VALUE)
    
    solution = solver.Assignment()
    solution.Add(shifts_flat)
    collector = solver.AllSolutionCollector(solution)
    
    solver.Solve(db, [collector])
    
    print("Solutions found:", collector.SolutionCount())
    print("Time:", solver.WallTime(), "ms")
    #Display a few solutions picked at random.
    a_few_solutions = [6, 66, 666]
    
    for sol in a_few_solutions:
        print("Solution number" , sol, '\n')

    for i in range(n_days):
        print("Day", i)
        for j in range(n_nurses):
            print("Nurse", j, "assigned to task",
                  collector.Value(sol, shifts[(j, i)]))

if __name__ == "__main__":
    main()


# In[ ]:



