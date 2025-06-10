from harvesting_utils.gather_utils import apply_to_gather
from .classification_gpt import classify_formula


def classify_gather(api_key, constant='pi', eq_length_limit=1500):

    def process_eq(eqdict):
        eq = eqdict['e']
        if len(eq) > eq_length_limit:
            return
        eqdict['c'] = classify_formula(eqdict['e'], api_key, constant=constant)
        return eqdict
    
    return apply_to_gather(process_eq, return_func=True)
