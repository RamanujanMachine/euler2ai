# This file will contain the algorithms for matching two pcfs after getting a hypothesis that they are coboundary,
# e.g. we get similar deltas
# 1. caclulate the dynamical parameters.
# 2. try to match the eigenvector ratios by folding according to the .
# 3. after that, apply coboundary to the resulting folded pcfs.


from coboundary_via_limits import CobViaLim, NoSolutionError
from recurrence_transforms import FoldToPCFTransform, CobTransform
from pcf_dynamical_parameters import PCFDynamics
from recurrence_transforms_utils import mobius
from ramanujantools.pcf import PCF
import sympy as sp
from typing import Tuple


def match_pcfs_first_attempt(pcf1: PCF, pcf2: PCF, limit1, limit2, depth: int = 2000, base_constant=sp.pi,
               tolerance: float = 1e-2, max_fold: int = 3, max_fit_up_to: int = 40, fit_up_to_step: int = 5, 
               verbose=False) -> Tuple[FoldToPCFTransform, FoldToPCFTransform, CobTransform]:
    r"""
    Matches two pcfs by finding the compound transformation between them (folding + coboundary).

    Args:
        pcf1, pcf2: the pcfs to match.
        limit1, limit2: the limits of the pcfs in terms of base_constant.
        depth: the depth to calculate the dynamical parameters up to.
        base_constant: the base constant for the pcfs.

        tolerance: tolerance for determining whether two pcfs have similar deltas.
        
        
        max_fit_up_to: the maximum fit up to value to try to extract the coboundary triple.
        fit_up_to_step: the step to increase the fit up to value by.
    
    Returns:
        A triple: (T1, T2, C)
            - T1: transformation applied to pcf1 (T1),
            - T2: transformation applied to pcf2 (T2),
            - C: coboundary transformation between the pcfs resulting from the above transformations (C).
            where T1 (pcf1) is coboundary via C to T2 (pcf2), i.e.
            C(T1(pcf1)) = T2(pcf2).
    """
    # check coboundary feasibility
    if verbose:
        print(f'Comparing pcf deltas: {pcf1}, {pcf2}.')
    delta1 = pcf1.delta(depth); delta2 = pcf2.delta(depth)
    if verbose:
        print(f'    {str(delta1)[:5]}, {str(delta2)[:5]}.')
    assert abs(delta1 - delta2) <= tolerance, \
        f'The deltas are not similar: {str(delta1)[:10]}, {str(delta2)[:10]} the pcfs are likely not coboundary.'

    # matching convergence rates
    if verbose:
        print(f'Calculating eigenvalue ratios.')
    eigenratio1 = PCFDynamics(pcf1).eigenvalue_ratio(depth)
    eigenratio2 = PCFDynamics(pcf2).eigenvalue_ratio(depth)
    ratio = sp.Rational(str(round(eigenratio1 / eigenratio2, 2)))
    if ratio.denominator > max_fold or ratio.numerator > max_fold:
        raise ValueError(f'Cannot fold: max_fold is set to {max_fold} and folds are {ratio.denominator, ratio.numerator}.')
    if verbose:
        print(f'    Eigenvalue ratios: {str(eigenratio1)[:5]}, {str(eigenratio2)[:5]}, ratio: {str(ratio)[:5]}.')
        print(f'Folding pcfs by {ratio.denominator} and {ratio.numerator}.')
    foldtopcf1 = FoldToPCFTransform(pcf1.M(), ratio.denominator, shift_pcf_as_necessary=False)
    foldtopcf2 = FoldToPCFTransform(pcf2.M(), ratio.numerator, shift_pcf_as_necessary=False)
    folded_pcf1 = foldtopcf1(pcf1.M()) # foldedpcf{i} are matrices
    folded_pcf2 = foldtopcf2(pcf2.M())
    folded_limit1 = foldtopcf1.transform_limit(mobius(pcf1.A().inv(), limit1))
    folded_limit2 = foldtopcf2.transform_limit(mobius(pcf2.A().inv(), limit2))
    
    # fold1 = FoldTransform(ratio.denominator)
    # fold2 = FoldTransform(ratio.numerator)
    # folded_pcf1 = fold1(pcf1.M())
    # folded_pcf2 = fold2(pcf2.M())
    
    # if verbose:
    #     print(f'Companionizing the folded pcfs.')
    # aspcf1 = CobTransformAsPCF(folded_pcf1)
    # aspcf2 = CobTransformAsPCF(folded_pcf2)
    # folded_pcf1 = aspcf1(folded_pcf1) # PCF(*aspcf1(folded_pcf1)[:, 1])
    # folded_pcf2 = aspcf2(folded_pcf2)
    # folded_pcf1_rep = PCF(*list(aspcf1(folded_pcf1)[:, 1])[::-1])
    # folded_pcf2_rep = PCF(*list(aspcf2(folded_pcf2)[:, 1])[::-1])

    folded_pcf1_rep = PCF(*list(folded_pcf1[:, 1])[::-1])
    folded_pcf2_rep = PCF(*list(folded_pcf2[:, 1])[::-1])
    if verbose:
        print(f'    Folded pcfs: {folded_pcf1_rep}, {folded_pcf2_rep}.')
        print(f'    Updated matrix limits: {folded_limit1}, {folded_limit2}.')
        print(f'    Updated pcf limits: {mobius(folded_pcf1_rep.A(), folded_limit1)}, {mobius(folded_pcf2_rep.A(), folded_limit2)}.')
    # if verbose:
    #     print(f'Comparing folded pcfs\' deltas.')
    # delta1 = folded_pcf1_rep.delta(1000)
    # delta2 = folded_pcf2_rep.delta(1000)
    # if verbose:
    #     print(f'    {str(delta1)[:5]}, {str(delta2)[:5]}.')
    # assert abs(delta1 - delta2)  <= 2 * tolerance, \
    #     f'The deltas are not similar after folding,: {str(delta1)[:5]}, {str(delta2)[:5]} check this.'
    
    # solving coboundary
    if verbose:
        print(f'Solving coboundary.')
    cobvialim = CobViaLim(folded_pcf1, folded_pcf2, folded_limit1, folded_limit2, base_constant=base_constant)
    cobvialim.solve_empirical_U(max_fit_up_to)
    U = None
    fit_up_to = 10
    while U is None and fit_up_to < max_fit_up_to:
        if verbose:
            print(f'    Trying fit_up_to = {fit_up_to}')
    # for fit_up_to in range(10, max_fit_up_to - fit_up_to_step + 1, fit_up_to_step):
        try:
            U, g1, g2 = cobvialim.extract_coboundary_triple(fit_up_to=fit_up_to)
        except NoSolutionError:
            pass
        fit_up_to += fit_up_to_step
    if U is None:
        U, g1, g2 = cobvialim.extract_coboundary_triple(fit_up_to=max_fit_up_to)

    return foldtopcf1, foldtopcf2, CobTransform(U, g1 / g2)




# tests:


from pcf_matching import match_pcfs
from recurrence_transforms_utils import as_pcf
from ramanujantools.pcf import PCF
from ramanujantools.cmf import known_cmfs
import sympy as sp


n, a, b, c = sp.symbols('n a b c')
f21 = known_cmfs.hypergeometric_derived_2F1()


def test_gauss_example():
    pcf1 = as_pcf(f21.trajectory_matrix({a: 1, b: 1, c: 0}, {a: 0, b: 0, c: 0}))
    pcf2 = PCF(2*n + 1, n**2)
    limit1 = -6 / sp.pi
    limit2 = 4 / sp.pi
    T1, T2, C = match_pcfs_first_attempt(pcf1, pcf2, limit1, limit2, base_constant=sp.pi, verbose=False)
    assert C(T1(pcf1.M())) == T2(pcf2.M())
    T1, T2, C = match_pcfs(pcf1, pcf2, limit1, limit2, 2, 1)
    assert C(T1(pcf1.M())) == T2(pcf2.M())


def test_trivial_example():
    pcf = PCF(2*n + 1, n**2)
    limit = 4 / sp.pi
    T1, T2, C = match_pcfs_first_attempt(pcf, pcf, limit, limit, base_constant=sp.pi, verbose=False)
    assert C(T1(pcf.M())) == T2(pcf.M())
    T1, T2, C = match_pcfs(pcf, pcf, limit, limit, 1, 1)
    assert C(T1(pcf.M())) == T2(pcf.M())


def test_example1():
    pcf1 = PCF(2 * n + 3, n ** 2 + 2 * n)
    pcf2 = PCF(2 * n + 1, n ** 2)
    limit1 =  4 / (sp.pi - 2)
    limit2 = 4 / sp.pi
    T1, T2, C = match_pcfs_first_attempt(pcf1, pcf2, limit1, limit2, base_constant=sp.pi, verbose=False)
    assert C(T1(pcf1.M())) == T2(pcf2.M())
    T1, T2, C = match_pcfs(pcf1, pcf2, limit1, limit2, 1, 1)
    assert C(T1(pcf1.M())) == T2(pcf2.M())


# gets stuck TODO
# def test_example2():
#     pcf1 = PCF(2 * n + 3, n ** 2 + 2 * n)
#     pcf2 = PCF(2 * n + 1, n ** 2)
#     limit1 =  4 / (sp.pi - 2)
#     limit2 = 4 / sp.pi
#     limit2 = get_folded_pcf_limit(pcf2, 3, limit2)
#     pcf2 = fold_pcf(pcf2, 3)
#     T1, T2, C = match_pcfs(pcf1, pcf2, limit1, limit2, base_constant=sp.pi, verbose=False)
#     assert C(T1(pcf1.M())) == T2(pcf2.M())


# TODO: add a test for a pcf vs its folded version.
# NOTE: there will likely be problems.