import json
import requests
import pandas as pd
from collections import defaultdict


def strip(p: str, s='1234567890.+-'):
    res = ''
    for x in p:
        if x not in s:
            res += x
    return res


def main():
    with open('result_final.json', 'w') as f:
        json.dump([], f)
    df = pd.read_excel('radii.xlsx', dtype={'Ion': str,
                                            'Charge': str,
                                            'Coordination': str,
                                            'Ionic Radius': float})
    with open('result_for_radii.json', 'r') as f:
        data = json.load(f)
    response = requests.get(
        'https://www.wikitable2json.com/api/Electronegativities_of_the_elements_(data_page)?table=0').json()
    e_n = pd.DataFrame(response[0][1:], columns=response[0][0])
    result = pd.DataFrame()
    for x in data:
        F_ELEMENTS = defaultdict()
        d = defaultdict()
        formula = x['_chemical_formula_structural']
        d['ID'] = x['_database_code_ICSD']
        d['Formula'] = x['_chemical_formula_structural']
        try:
            d['Cell_length_A'] = x['_cell_length_a']
            d['Cell_length_C'] = x['_cell_length_c']
        except KeyError:
            pass
        for i, p in enumerate(x['_atom_type_symbol']):
            el = strip(p)
            d[f'Element_{i}'] = el
            F_ELEMENTS[el] = i
            d[f'Electronegativity_{i}'] = e_n.loc[e_n['Symbol'] == el]['use'].to_string().split()[1]
        if '.' in formula and '(' in formula:
            f = formula[formula.find('(') + 1:formula.find(')')]
            elements = []
            for p in x['_atom_type_symbol']:
                el = strip(p)
                if el in f:
                    elements.append(el)
            for s in elements:
                f = f.replace(s, '')
            numb = [float(strip(r, s='()')) for r in f.split(' ')]
            ip = 0
            for i, p in enumerate(x['_atom_type_symbol']):
                el = strip(p)
                if el in elements:
                    if 'Ionic_radius_()' not in d:
                        d[f'Ionic_radius_()'] = \
                            pd.to_numeric(df.loc[(df['Ion'] == el) & (
                                    df['Charge'] == strip(x['_atom_type_oxidation_number'][F_ELEMENTS[el]], '+-')) & (
                                           df['Coordination'] == 'IV')][
                                'Ionic Radius']) * numb[ip]
                    else:
                        d[f'Ionic_radius_()'] += \
                            pd.to_numeric(df.loc[(df['Ion'] == el) & (
                                    df['Charge'] == strip(x['_atom_type_oxidation_number'][F_ELEMENTS[el]], '+-')) & (
                                           df['Coordination'] == 'IV')][
                                'Ionic Radius']) * numb[ip]
                    ip += 1
            formula = formula.replace('(' + formula[formula.find('(') + 1:formula.find(')')] + ')', '')
        if '(' not in formula:
            try:
                for i, p in enumerate(x['_atom_type_symbol']):
                    el = strip(p)
                    if el in F_ELEMENTS:
                        d[f'Ionic_radius_{i}'] = pd.to_numeric(df.loc[(df['Ion'] == el)
                                                        & (df['Charge'] == strip(x['_atom_type_oxidation_number'][F_ELEMENTS[el]], '+-'))
                                                        & (df['Coordination'] == 'IV')]['Ionic Radius'])
                res = pd.DataFrame([d])
                result = pd.concat([result, res], ignore_index=True)
            except IndexError:
                pass

    with open('result_final.json', 'w') as f:
        json.dump(json.loads(result.to_json(orient='records')), f, indent=1)
    result.to_excel(r'radii_for_all_species.xlsx', index=False)


if __name__ == '__main__':
    main()
