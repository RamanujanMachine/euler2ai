from coboundary_via_limits import CobViaLim, NoSolutionError
from recurrence_transforms import FoldToPCFTransform, CobTransform, RecurrenceTransform, CobTransformShift
from pcf_dynamical_parameters import PCFDynamics
from recurrence_transforms_utils import mobius
from ramanujantools.pcf import PCF
import sympy as sp
from sympy.abc import n
from typing import Tuple
from IPython.display import display


# not currently used
# for getting best rational approximations to the ratios between eigenvalue ratios
def extract_cf(n, d):
    if d == 0: return []
    q = n // d
    r = n - q*d
    return [q] + extract_cf(d, r)


def compute_cf(alist, depth):
    if len(alist) == 0:
        return 0
    if len(alist) == 1 or depth == 0:
        return alist[0]
    return alist[0] + 1 / compute_cf(alist[1:], depth-1)


def get_necessary_shift_to_coboundary(U, g1, g2):
    shift = 0
    cob_zeros = [z for z in sp.solve(U.det(), n) if isinstance(z, sp.Integer) or isinstance(z, int)]
    if cob_zeros:
        shift = max(shift, sp.Integer(max(cob_zeros)))
        # no + 1 since we are counting from n=1 due to the way a PCF is computed
    multiplier_zeros = [z for z in sp.solve(g1, n) if isinstance(z, sp.Integer) or isinstance(z, int)]
    multiplier_zeros += [z for z in sp.solve(g2, n) if isinstance(z, sp.Integer) or isinstance(z, int)]
    if multiplier_zeros:
        shift = max(shift, sp.Integer(max(multiplier_zeros)))
    return shift


class CannotFoldError(Exception):
    pass


def match_pcfs(pcf1: PCF, pcf2: PCF, limit1, limit2, eigenratio1, eigenratio2, base_constant=sp.pi,
                                 fold=True, max_fold: int = 3, approximate_ratio_to=10, max_shift=3,
                                 max_fit_up_to: int = 40, fit_up_to_step: int = 5, shift_cob_as_necessary=True,
                                 cob_via_lim_verbose=False, verbose=False
                                 ) -> Tuple[RecurrenceTransform, RecurrenceTransform, CobTransform]:
    r"""
    Matches two pcfs by finding the compound transformation between them (folding + coboundary).
    NOTE: requires PCFs in terms of sympy symbol n.

    Args:
        * pcf1, pcf2: the pcfs to match.
        * limit1, limit2: the limits of the pcfs in terms of base_constant.
        * eigenratio1, eigenratio2: the eigenvalue ratios of the pcfs.
        * base_constant: the base constant for the pcfs.
        * fold: whether to fold the pcfs to match the eigenvalue ratios.
        * max_fold: the maximum fold to allow when folding the pcfs.
        * approximate_ratio_to: the maximum denominator to approximate the eigenvalue ratios to.
        * max_shift: the maximum shift to allow when hopping along the lattice to find a well-defined coboundary matrix.
        * max_fit_up_to: the maximum fit up to value to try to extract the coboundary triple.
        * fit_up_to_step: the step to increase the fit up to value by.
        * shift_cob_as_necessary: whether to apply a shift
            to make the coboundary matrix well-defined (det(U) != 0) at all depths 
        * cob_via_lim_verbose: whether to print the progress of the coboundary via limits algorithm.
        * verbose: whether to print the progress of the matching algorithm.
    
    Returns:
        A triple: (T1, T2, C)
        * T1: transformation applied to pcf1 (T1),
        * T2: transformation applied to pcf2 (T2),
        * C: coboundary transformation between the pcfs resulting from the above transformations (C).

        Where T1 (pcf1) is coboundary via C to T2 (pcf2), i.e.
        C(T1(pcf1)) = T2(pcf2).

    Raises:
        NoSolutionError: if no coboundary solution is found.
    """

    # matching convergence rates
    if fold:
        ratio = sp.Rational(str(round(eigenratio1 / eigenratio2, 2))).limit_denominator(approximate_ratio_to)
        num, den = ratio.as_numer_denom()
        num = num if num != 0 else 1
        den = den if den != 0 else 1
        ratio = sp.Rational(num, den)
        if verbose:
            print(f'Eigenvalue ratios: {str(eigenratio1)[:5]}, {str(eigenratio2)[:5]}, ratio: {str(ratio)[:5]}.')
            print(f'Folding pcfs by {ratio.denominator} and {ratio.numerator}.')
        if ratio.denominator > max_fold or ratio.numerator > max_fold:
            raise CannotFoldError(f'Cannot fold: max_fold is set to {max_fold}' + \
                                  f' and folds are {ratio.denominator, ratio.numerator}.')
        foldtopcf1 = FoldToPCFTransform(pcf1.M(), ratio.denominator, shift_pcf_as_necessary=False) 
        foldtopcf2 = FoldToPCFTransform(pcf2.M(), ratio.numerator, shift_pcf_as_necessary=False)
        # shift_pcf_as_necessary=False because otherwise the new limit will be problematic to compute... may not converge to pi?
        # TODO: understand what a singular matrix does to the limit
        # Example to consider: ([2, 2], [1, 1]). This will convert the limit to 2. No matter what it was...
        
        # hop along the pcf{i}-foldedpcf{i} lattice
        # shift the coboundary matrix to make sure it is nonsingular
        # critical for transforming the limit
        if verbose:
            print(f'    Checking if a shift to the coboundary matrices (a lattice hop) is necessary.')
        cob_shift1 = 0
        cob_shift2 = 0
        fixed = False
        while max(cob_shift1, cob_shift2) <= max_shift:
            aspcf1 = foldtopcf1.transforms[1]; aspcf2 = foldtopcf2.transforms[1] # the second transform is the coboundary
            aspcf1g1, aspcf1g2 = aspcf1.multiplier.as_numer_denom(); aspcf2g1, aspcf2g2 = aspcf2.multiplier.as_numer_denom()
            shift1 = get_necessary_shift_to_coboundary(aspcf1.U, aspcf1g1, aspcf1g2)
            shift2 = get_necessary_shift_to_coboundary(aspcf2.U, aspcf2g1, aspcf2g2)
            if (shift1 or shift2):
                cob_shift1 += shift1; cob_shift2 += shift2
                if verbose:
                    print(f'        Shifting pcf1, pcf2 by: {cob_shift1}, {cob_shift2}.')
                shift_transform1 = RecurrenceTransform([CobTransformShift(pcf1.M(), cob_shift1)])
                shift_transform2 = RecurrenceTransform([CobTransformShift(pcf2.M(), cob_shift2)])
                foldtopcf1 = FoldToPCFTransform(shift_transform1(pcf1.M()), ratio.denominator, shift_pcf_as_necessary=False)
                foldtopcf2 = FoldToPCFTransform(shift_transform2(pcf2.M()), ratio.numerator, shift_pcf_as_necessary=False)
            else:
                fixed = True
                foldtopcf1 = RecurrenceTransform([shift_transform1, foldtopcf1]) if cob_shift1 else foldtopcf1
                foldtopcf2 = RecurrenceTransform([shift_transform2, foldtopcf2]) if cob_shift2 else foldtopcf2
                break
        if not fixed:
            words = ["pcf1" if cob_shift1 else None, "pcf2" if cob_shift2 else None]
            phrase = " and ".join([word for word in words if word])
            raise CannotFoldError(f'Could not make {phrase}' + \
                                  f' AsPCF coboundary matrix nonsingular by shifting by {max_shift}.')                
        
        # solved!
        ##### !!!!! CONTINUE HERE !!!!! #####
        # TODO: debug why these do not result in polynomial matrices, but in rational matrices...
        # There may be a mistake in the logic that the transforms are modified by a subs upon shifting (hopping) in the lattice... 
        folded_pcf1 = foldtopcf1(pcf1.M()) # folded_pcf{i} are matrices
        folded_pcf2 = foldtopcf2(pcf2.M())
        if verbose:
            print(f'    Folded pcf matrices:') 
            # display(folded_pcf1)
            print(folded_pcf1)
            # display(folded_pcf2)
            print(folded_pcf2)
        folded_limit1 = foldtopcf1.transform_limit(mobius(pcf1.A().inv(), limit1))
        folded_limit2 = foldtopcf2.transform_limit(mobius(pcf2.A().inv(), limit2))
    else:
        foldtopcf1 = FoldToPCFTransform(pcf1.M(), 1)
        foldtopcf2 = FoldToPCFTransform(pcf1.M(), 1)
        folded_pcf1 = pcf1.M()
        folded_pcf2 = pcf2.M()
        folded_limit1 = mobius(pcf1.A().inv(), limit1)
        folded_limit2 = mobius(pcf2.A().inv(), limit2) 

    folded_pcf1_rep = PCF(*list(folded_pcf1[:, 1])[::-1])
    folded_pcf2_rep = PCF(*list(folded_pcf2[:, 1])[::-1])
    if verbose:
        print(f'    Updated pcfs:\n    {folded_pcf1_rep}\n    {folded_pcf2_rep}')
        print(f'    Updated matrix limits: {folded_limit1}, {folded_limit2}.')
        print(f'    Updated pcf limits: {mobius(folded_pcf1_rep.A(), folded_limit1).simplify()}, {mobius(folded_pcf2_rep.A(), folded_limit2).simplify()}')

    # solving coboundary
    if verbose:
        print(f'Solving coboundary.')
    cobvialim = CobViaLim(folded_pcf1, folded_pcf2, folded_limit1, folded_limit2, base_constant=base_constant)
    cobvialim.solve_empirical_U(max_fit_up_to, verbose=cob_via_lim_verbose)
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
        # this will raise a NoSolutionError if no solution is found
        U, g1, g2 = cobvialim.extract_coboundary_triple(fit_up_to=max_fit_up_to)

    
    # TODO: figure out if there is a simple way to convert the transformations found
    # so that the resulting coboundary matrix between the final PCFs is always invertible

    # hop along the foldedpcf1-foldedpcf2 lattice
    # to the first index from which the coboundary transformation is always indvertible
    # include this shift in the final transformations returned

    # if verbose:
    #     print(f'Checking if a shift to the coboundary matrix (a lattice hop) is necessary.')
    # if shift_cob_as_necessary:
    #     shift = get_necessary_shift_to_coboundary(U, g1, g2)
    #     if shift:
    #         if verbose:
    #             print(f'    Shifting everything by {shift}.')
    #         foldtopcf1 = RecurrenceTransform([CobTransformShift(pcf1.M(), shift), foldtopcf1.shift(shift)]) # TODO: implememt subs in RecurrenceTransform
    #         foldtopcf2 = RecurrenceTransform([CobTransformShift(pcf2.M(), shift), foldtopcf2.shift(shift)])
    #         U = U.subs({n: n + shift})
    #         g1 = g1.subs({n: n + shift}); g2 = g2.subs({n: n + shift})

    return foldtopcf1, foldtopcf2, CobTransform(U, g1 / g2)
