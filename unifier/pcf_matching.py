from .coboundary_solver import CobViaLim, PCFCobViaLim
from .utils.rational_fit_utils import NoSolutionError
from .recurrence_transforms import FoldToPCFTransform, CobTransform, RecurrenceTransform, CobTransformShift
from .utils.recurrence_transforms_utils import mobius
from .pcf import PCF
import sympy as sp
from sympy.abc import n
from typing import Tuple


def apply_match_pcfs(pcf1: PCF, pcf2: PCF, limit1, limit2, convrate1, convrate2, base_constant=sp.pi,
                     cob_via_lim_verbose=False, verbose=False
                    ) -> Tuple[RecurrenceTransform, RecurrenceTransform, CobTransform]:
    """
    Applies the match_pcfs function to the given pcfs and returns the transformations.
    If the convergence rates are 0, it tries to match the pcfs using 3 folding schemes:
    fold neither or fold one of them by 2 (two options).

    Args:
        * pcf1, pcf2: the pcfs to match.
        * limit1, limit2: the limits of the pcfs in terms of base_constant.
        * convrate1, convrate2: the exponential convergence rates of the pcfs.
        * base_constant: the base constant for the pcfs.
        * cob_via_lim_verbose: whether to print the progress of the coboundary via limits algorithm.
        * verbose: whether to print the progress of the matching algorithm.
    
    Returns:
        A triple: (T1, T2, C) as in match_pcfs.
        
    Raises:
        NoSolutionError: if no coboundary solution is found.
    """
    
    if convrate1 == 0 or convrate2 == 0:
        if verbose:
            print("One of the convergence rates is 0, trying to match by folding by 1 or 2")
        transformation = None

        attempts = [(1, 1), (1, 2), (2, 1)]
        for attempt in attempts:
            if verbose:
                print("\nAttempting folds by:", attempt[0], attempt[1])
            try:
                transformation = match_pcfs(pcf1, pcf2, limit1, limit2, attempt[0], attempt[1], base_constant=base_constant,
                                            try_simple_cob=False,
                                            cob_via_lim_verbose=cob_via_lim_verbose, verbose=verbose)
            except Exception as e:
                continue
            if transformation is not None:
                break

        if transformation is None:
            raise NoSolutionError('Matching failed.')
    
    else:
        transformation = match_pcfs(pcf1, pcf2, limit1, limit2, convrate1, convrate2, base_constant=base_constant,
                                    cob_via_lim_verbose=cob_via_lim_verbose, verbose=verbose)
    
    return transformation


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


# def iterative_coboundary(cob, max_fit_up_to: int = 40, fit_up_to_step: int = 5, verbose=False):
# make this a function and plug in where necessary
# # solving coboundary
#     if verbose:
#         print(f'Solving coboundary.')
#     cobvialim = CobViaLim(folded_pcf1, folded_pcf2, folded_limit1, folded_limit2, base_constant=base_constant)
#     cobvialim.solve_empirical_U(max_fit_up_to, verbose=cob_via_lim_verbose)
#     U = None
#     fit_up_to = 10
#     while U is None and fit_up_to < max_fit_up_to:
#         if verbose:
#             print(f'    Trying fit_up_to = {fit_up_to}')
#     # for fit_up_to in range(10, max_fit_up_to - fit_up_to_step + 1, fit_up_to_step):
#         try:
#             U, g1, g2 = cobvialim.extract_coboundary_triple(fit_up_to=fit_up_to)
#         except NoSolutionError:
#             pass
#         fit_up_to += fit_up_to_step
#     if U is None:
#         # this will raise a NoSolutionError if no solution is found
#         U, g1, g2 = cobvialim.extract_coboundary_triple(fit_up_to=max_fit_up_to)


def match_pcfs(pcf1: PCF, pcf2: PCF, limit1, limit2, convrate1, convrate2, base_constant=sp.pi,
                                 fold=True, max_fold: int = 3, approximate_ratio_to=10, max_shift=3,
                                 max_fit_up_to: int = 40, fit_up_to_step: int = 5, shift_cob_as_necessary=True, # currently not used, see end of function
                                 try_simple_cob=True,
                                 cob_via_lim_verbose=False, verbose=False
                                 ) -> Tuple[RecurrenceTransform, RecurrenceTransform, CobTransform]:
    r"""
    Matches two pcfs by finding the compound transformation between them (folding + coboundary).
    NOTE: requires PCFs in terms of sympy symbol n.

    Args:
        * pcf1, pcf2: the pcfs to match.
        * limit1, limit2: the limits of the pcfs in terms of base_constant.
        * convrate1, convrate2: the exponential convergence rates of the pcfs.
        * base_constant: the base constant for the pcfs.
        * fold: whether to fold the pcfs to match the convergence rates.
        * max_fold: the maximum fold to allow when folding the pcfs.
        * approximate_ratio_to: the maximum denominator to approximate the convergence rates to.
        * max_shift: the maximum shift to allow when hopping along the lattice to find a well-defined coboundary matrix.
        * max_fit_up_to: the maximum fit up to value to try to extract the coboundary triple.
        * fit_up_to_step: the step to increase the fit up to value by.
        * shift_cob_as_necessary: whether to apply a shift
            to make the coboundary matrix well-defined (det(U) != 0) at all depths
        * try_simple_cob: whether to try a simple coboundary match without folding first. 
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

    U, g1, g2 = None, None, None

    if try_simple_cob:

        if verbose:
            print(f'Checking coboundary for pcfs: {pcf1}, {pcf2}.')
        if verbose:
            print(f'Solving coboundary.')

        cobvialim = PCFCobViaLim(pcf1, pcf2, limit1, limit2, base_constant=base_constant)
        cobvialim.solve_empirical_U(max_fit_up_to, verbose=cob_via_lim_verbose)
    
        fit_up_to = 10
        while U is None and fit_up_to <= max_fit_up_to + 1: # NOTE: <= to make sure the last fit_up_to is tried, differs from the loop for after folding below
            if verbose:
                print(f'    Trying fit_up_to = {fit_up_to}')
            try:
                U, g1, g2 = cobvialim.extract_coboundary_triple(fit_up_to=fit_up_to)
            except NoSolutionError:
                pass
            fit_up_to += fit_up_to_step
        foldtopcf1, foldtopcf2 = FoldToPCFTransform(pcf1.CM(), 1), FoldToPCFTransform(pcf1.CM(), 1) # initialize
    
    if U is None:
        # matching convergence rates
        if fold and convrate1 != 0 and convrate2 != 0:
            ratio = sp.Rational(str(round(convrate1 / convrate2, 2))).limit_denominator(approximate_ratio_to)
            num, den = ratio.as_numer_denom()
            num = num if num != 0 else 1
            den = den if den != 0 else 1
            ratio = sp.Rational(num, den)
            if verbose:
                print(f'Convergence rates: {str(convrate1)[:5]}, {str(convrate2)[:5]}, ratio: {str(ratio)[:5]}.')
            
            if not ratio == 1 or not try_simple_cob:
                if ratio.denominator > max_fold or ratio.numerator > max_fold:
                    raise CannotFoldError(f'Cannot fold: max_fold is set to {max_fold}' + \
                                        f' and folds are {ratio.denominator, ratio.numerator}.')
                if verbose:
                    print(f'Folding pcfs by {ratio.denominator} and {ratio.numerator}.')
                foldtopcf1 = FoldToPCFTransform(pcf1.CM(), ratio.denominator, shift_pcf_as_necessary=False) 
                foldtopcf2 = FoldToPCFTransform(pcf2.CM(), ratio.numerator, shift_pcf_as_necessary=False)
                # shift_pcf_as_necessary=False because otherwise the new limit will be problematic to compute... may not converge to pi?
                
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
                        shift_transform1 = RecurrenceTransform([CobTransformShift(pcf1.CM(), cob_shift1)])
                        shift_transform2 = RecurrenceTransform([CobTransformShift(pcf2.CM(), cob_shift2)])
                        foldtopcf1 = FoldToPCFTransform(shift_transform1(pcf1.CM()), ratio.denominator, shift_pcf_as_necessary=False)
                        foldtopcf2 = FoldToPCFTransform(shift_transform2(pcf2.CM()), ratio.numerator, shift_pcf_as_necessary=False)
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
                folded_pcf1 = foldtopcf1(pcf1.CM()) # folded_pcf{i} are matrices
                folded_pcf2 = foldtopcf2(pcf2.CM())
                if verbose:
                    print(f'    Folded pcf matrices:') 
                    print(folded_pcf1)
                    print(folded_pcf2)
                folded_limit1 = foldtopcf1.transform_limit(mobius(pcf1.A().inv(), limit1))
                folded_limit2 = foldtopcf2.transform_limit(mobius(pcf2.A().inv(), limit2))

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

    if U is None or g1 is None or g2 is None:
        raise NoSolutionError('Matching failed.')

    return foldtopcf1, foldtopcf2, CobTransform(U, g1 / g2)
