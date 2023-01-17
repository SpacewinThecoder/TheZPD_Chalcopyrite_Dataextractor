import json
import os
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from collections import defaultdict


def main():
    with open('result.json', 'w') as f:
        json.dump([], f)
    param = ['_database_code_ICSD',
             '_chemical_formula_structural',
             '_cell_length_a',
             '_cell_length_c',
             '_atom_type_symbol',
             '_atom_type_oxidation_number']
    dir = 'Chalcopyrites'
    data = []
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        d = MMCIF2Dict(path)
        p = defaultdict()
        for par in param:
            try:
                if len(d[par]) > 1:
                    p[par] = d[par]
                else:
                    p[par] = d[par][0]
            except KeyError:
                pass
        data.append(p)
    with open('result_for_radii.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
