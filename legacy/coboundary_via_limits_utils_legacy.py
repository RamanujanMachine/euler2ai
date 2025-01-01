import cvc5.pythonic as cp
import sympy as sp
from sympy import symbols
n = symbols('n')


class NoSolutionError(Exception):
    pass


# Obsolete - for the obsolete `solver_extract_U` method of CobViaLim class


def check_zero_dict(dic, keys):
    return all([dic[key] == 0 or dic[key] == float(0) for key in dic.keys() if key in keys])


def sympy_fit_rational_function(empirical_numerators, empirical_denominators, num_deg, den_deg, symbol=n):
    num_coeffs = [symbols(f'num_{i}') for i in range(num_deg + 1)]
    den_coeffs = [symbols(f'den_{i}') for i in range(den_deg + 1)]
    all_vars = num_coeffs + den_coeffs

    def rational_function(r):
        numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
        denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
        return numerator, denominator

    equations = []
    for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
        func_num, func_den = rational_function(i + 1)
        equations.append(func_num * emp_den - func_den * emp_num)
    solutions = sp.solve(equations, all_vars, dict=True)

    dummy_symb = symbols('x')
    found_solution = False
    for sol in solutions:
        vars_left = [v for v in all_vars if v not in sol.keys()]
        subs_dict = {var: 1 for var in vars_left}
        assignment = {key: sp.Rational((val * dummy_symb / dummy_symb).subs(subs_dict)) for key, val in sol.items()}
        assignment.update(subs_dict)
        if check_zero_dict(assignment, den_coeffs):
            continue
        else:
            found_solution = True
            break

    if not found_solution:
        print('No viable (nontrivial + defined) solution found. Solutions found:')
        print(solutions)
        raise NoSolutionError('No viable (nontrivial + defined) solution found.')

    numerator = sum(num_coeffs[i] * symbol**i for i in range(num_deg + 1))
    denominator = sum(den_coeffs[i] * symbol**i for i in range(den_deg + 1))
    quotient = sp.simplify((numerator / denominator).subs(assignment))

    return quotient


def cvc5_fit_rational_function(empirical_numerators, empirical_denominators, num_deg, den_deg, symbol=n):
    num_coeffs = [cp.Int(f'num_{i}') for i in range(num_deg + 1)]
    den_coeffs = [cp.Int(f'den_{i}') for i in range(den_deg + 1)]

    def rational_function(r):
        numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
        denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
        return numerator, denominator

    solver = cp.Solver()
    if len(den_coeffs) > 1:
        solver.add(cp.Or([v != 0 for v in den_coeffs]))
    else:
        solver.add(den_coeffs[0] != 0)

    for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
        func_num, func_den = rational_function(i + 1)
        solver.add(func_num * emp_den == func_den * emp_num)

    if solver.check() == cp.sat:
        model = solver.model()
        num_values = [model.evaluate(coeff).as_long() for coeff in num_coeffs]
        den_values = [model.evaluate(coeff).as_long() for coeff in den_coeffs]

        numerator = sum(sp.Rational(num_values[i]) * symbol**i for i in range(num_deg + 1))
        denominator = sum(sp.Rational(den_values[i]) * symbol**i for i in range(den_deg + 1))

        quotient = sp.simplify(numerator / denominator)

        return quotient

    else:
        raise NoSolutionError('Equations not satisfiable.')