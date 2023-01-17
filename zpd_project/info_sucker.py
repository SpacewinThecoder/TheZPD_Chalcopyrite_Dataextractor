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
             '_cell_length_b',
             '_cell_length_c']
    param_2 = ['_atom_site_label',
               '_atom_site_type_symbol',
               '_atom_site_symmetry_multiplicity',
               '_atom_site_Wyckoff_symbol',
               '_atom_site_fract_x',
               '_atom_site_fract_y',
               '_atom_site_fract_z',
               '_atom_site_occupancy',
               '_atom_site_attached_hydrogens']
    dir = 'Chalcopyrites'
    data = []
    d = MMCIF2Dict('Chalcopyrites/Ag1_5Cu0_5In2Te4.cif')
    print(d)
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        d = MMCIF2Dict(path)
        p = defaultdict()
        for par in param:
            try:
                p[par] = d[par][0]
            except KeyError:
                pass
        s = ''
        for i in range(len(d[param_2[0]])):
            for par in param_2:
                s += d[par][i] + ' '
            s += '\n'
        p['notation'] = s
        data.append(p)
    with open('result.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
