from unifier import PCF


def compute_dynamics(pcf, depth=1000, depth_shift=100, verbose=False):
    orig_depth = depth

    delta = float('+inf'); i = 0; success = False
    while (delta == float('+inf') or not success) and i < 5:
        if i > 0:
            if verbose:
                print('delta is +inf')
                print(i, pcf)
        try:
            delta = pcf.delta(depth)
            success = True
        except Exception as e:
            # print(f'Error in delta of {pcf}:', e)
            success = False
        depth += depth_shift; i += 1
    delta = round(delta, 5)

    depth = orig_depth
    convrate = 0; i = 0; success = False
    while not success and i < 5:
        try:
            convrate = round(pcf.convergence_rate(orig_depth), 5)
            success = True
        except Exception as e:
            if verbose:
                print(f'Error in convrate of {pcf}:', e)
        depth += depth_shift; i += 1

    return delta, convrate
