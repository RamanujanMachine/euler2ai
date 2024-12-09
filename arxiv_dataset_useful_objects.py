

def arxiv_metadata_dataset_pth():
    return r"C:\Users\totos\Desktop\arXiv dataset (kaggle)\arxiv-metadata-oai-snapshot.json"


def categories_of_interest(original_list=False):
    ls = ['cs.AI', 'cs.LG', 'cs.DC', 'math.NT', 'math.PR', 'math.CO', 'math.GM', 'math.HO']
    if original_list:
        return ls
    ls.append('math.CA') # from 2402.08693
    return ls


def arxiv_dataset_useful_ids(original_list=False):
    ls =  ['1711.00459', '1704.02875', 'math/0402462', '2004.00090',
            '1806.03346', '2108.07718', 'math/9306213', '0709.2181',
            '2308.11829', '1907.00205', '2203.09465']
    if original_list:
        return ls
    # Night of 7-8/12/24:
    # "formula for pi" - arXiv search
    ls.append('2402.08693') # interesting infinite series
    ls.append('1906.00122') # Wallis product
    ls.append('1704.02875') # another arctan series (may be useful)
    ls.append('1608.06185') # nested square roots (may be useful)
    ls.append('1402.6577') # Wallis product

    # "pi formula" - arXiv search (NOTE: apparently PI formula is something in gauge theories on a cylinder)
    ls.append('2402.10589') # Leibniz + more interesting series (from integrals)

    # "series for pi" - arXiv search (NOTE: PI-Algebras are a thing)
    ls.append('0909.1523') # series for pi, though might be incorrect

    # "continued  fraction" + pi - arXiv search
    # ls.append('1201.6687') # Euler's original paper in German? not useful, does not contain pi formulas
    ls.append('0807.0872') # new (to me) infinite series (eqs. 5, 23, 26, 40, 42 for pi look useful!), 
    # also has familiar ones like BBP type (eqs. 31, 33), continued fractions, nested square roots, Wallis product, integrals

    # "calculate pi" - arXiv search
    # ls.append('1310.5610') # review of different methods (may be useful but likely not)
    ls.append('1008.3171') # BBP type

    # "the constant pi" - arXiv search
    # ls.append('2110.02749') # contains high degree pi formulas, e.g. zeta(2) (may be useful)
    ls.append('1604.03752') # interesting parametric series for pi (only extra variable that is take to infinity,
    # but it appears in the summand)
    ls.append('1603.03310') # same as above (in fact is same author)
    ls.append('1603.01462') # same as last two
    # ls.append('1402.0133') # contains zeta(2) (may be useful)

    return ls
    


#  filtered = sat_filter_gather(gather, [[pi_unifier_patterns(r'\pi', return_string=True)]])
