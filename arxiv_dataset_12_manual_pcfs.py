from ramanujantools.pcf import PCF
import sympy as sp
import pickle
import pandas as pd


SAVE_FILE = r"manual_pcfs_from_29.10.24.pkl" 

# defaults
SAVE_DIR = r"C:\Users\totos\Desktop\12 - manual_pcfs"
SAVE_PATH = f"{SAVE_DIR}/{SAVE_FILE}"
ORIGIN_PATH = r"misc\pi_pcfs_29.10.24.pkl"

with open(ORIGIN_PATH, "rb") as f:
    manual_pi_pcfs = pickle.load(f)

list_of_dictionaries = []

for pcf, dic in manual_pi_pcfs.items():
    temp_dic = {}
    
    pcf = PCF(*pcf)
    
    temp_dic['a'] = pcf.a_n
    temp_dic['b'] = pcf.b_n
    temp_dic['limit'] = sp.sympify(dic['limit'])

    limits = pcf.limit(list(range(2, 22)))
    first20convergents = [sp.Rational(*lim.as_rational()) for lim in limits]
    temp_dic['first20convergents'] = first20convergents
    temp_dic['origin_formula_type'] = 'cf'
    temp_dic['source_type'] = 'manual'
    temp_dic['source'] = r'Manual PCFs from 29.10.24 (misc\pi_pcfs_29.10.24.pkl) - ' + dic['source']
    temp_dic['metadata'] = {'valid': dic['valid']}

    list_of_dictionaries.append(temp_dic)

manual_pcfs = pd.DataFrame(list_of_dictionaries).to_pickle(SAVE_PATH)
