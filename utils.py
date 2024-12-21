# miscellaneous utility functions.
from LIReC.db.access import db


def lid(string, constants=['pi']):
    r"""
    Identify relation to pi using LIReC.
    """
    for res in db.identify([str(string), *constants]):
        print(res)


def write_dicts_to_latex_table(dict_list, output_file, headers=None, sort=None):
    if not dict_list:
        raise ValueError("The list of dictionaries is empty.")
    
    if not headers:
        # Get the headers from the keys of the first dictionary
        header_list = [dic.keys() for dic in dict_list]
        headers_set = set()
        for h in header_list:
            headers_set.update(set(h))
        print(headers_set)
        headers = list(headers_set)
        assert set(headers) == headers_set, "The headers do not match the keys of the dictionaries."

    if sort:
        dict_list = sorted(dict_list, key=lambda x: x[sort])
    
    with open(output_file, 'w') as f:
        # Write the beginning of the LaTeX document
        f.write(r'\documentclass{article}' + '\n')
        f.write(r'\usepackage{booktabs}' + '\n')
        f.write(r'\begin{document}' + '\n')
        f.write(r'\begin{table}[h!]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{' + ' '.join(['l' for _ in headers]) + '}' + '\n')
        f.write(r'\toprule' + '\n')
        
        # Write the headers
        f.write(' & '.join(headers) + r' \\' + '\n')
        f.write(r'\midrule' + '\n')
        
        # Write the rows
        for dictionary in dict_list:
            dictionary = {header: dictionary.get(header, '') for header in headers} # Fill in missing values with empty strings
            row = ' & '.join(str(dictionary[header]) for header in headers)
            f.write(row + r' \\' + '\n')
        
        # Write the end of the table and document
        f.write(r'\bottomrule' + '\n')
        f.write(r'\end{tabular}' + '\n')
        f.write(r'\caption{Your Table Caption Here}' + '\n')
        f.write(r'\end{table}' + '\n')
        f.write(r'\end{document}' + '\n')
        