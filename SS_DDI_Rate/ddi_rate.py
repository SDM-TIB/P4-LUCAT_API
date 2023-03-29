import json
import pandas as pd
import treatment_generation
pd.options.mode.chained_assignment = None  # default='warn'
from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, load, ask

from SPARQLWrapper import SPARQLWrapper, JSON
from math import comb
import os

# KG = os.environ["ENDPOINT"]
KG = 'https://labs.tib.eu/sdm/p4lucat_kg/sparql'


def execute_query(query, limit=0, page=0):
    if limit != 0:
        query += "LIMIT " + str(limit)
    query += " OFFSET " + str(page)
    sparql_ins = SPARQLWrapper(KG)
    sparql_ins.setQuery(query)
    sparql_ins.setReturnFormat(JSON)
    return sparql_ins.query().convert()


def create_filter_cui(input_cui):
    return ','.join(['<http://research.tib.eu/p4-lucat/entity/' + cui + '>' for cui in input_cui])


def build_query_p4lucat(input_cui_uri):
    query = """
    prefix p4-lucat: <http://research.tib.eu/p4-lucat/vocab/>
    select distinct ?EffectorDrugLabel ?AffectedDrugLabel ?Effect  ?Impact ?precipitantDrug ?objectDrug
        where {
        ?ddi a p4-lucat:DrugDrugInteraction .
        ?ddi p4-lucat:precipitantDrug ?precipitantDrug . 
        ?ddi p4-lucat:objectDrug ?objectDrug .
        ?ddi p4-lucat:effect ?o . 
        ?o <http://research.tib.eu/p4-lucat/vocab/annLabel> ?Effect . 
        ?ddi p4-lucat:impact ?Impact .
        ?precipitantDrug <http://research.tib.eu/p4-lucat/vocab/annLabel> ?EffectorDrugLabel.
        ?objectDrug <http://research.tib.eu/p4-lucat/vocab/annLabel> ?AffectedDrugLabel.

    FILTER (?precipitantDrug in (""" + input_cui_uri + """ ) && ?objectDrug in (""" + input_cui_uri + """))
    }"""
    return query


def store_pharmacokinetic_ddi(effect):
    if effect in ['Excretion_rate', 'Excretory_function', 'Excretion', 'excretion rate', 'excretion_rate',
                  'Excretion rate', 'Excretion Rate']:
        effect = 'excretion'
    elif effect in ['Process_of_absorption', 'Absorption']:
        effect = 'absorption'
    elif effect in ['Serum_concentration', 'Serum_concentration_of', 'Serum_level', 'Serum_globulin_level',
                    'Metabolite', 'Active_metabolites', 'serum concentration']:
        effect = 'serum_concentration'
    elif effect in ['Metabolism']:
        effect = 'metabolism'
    else:
        return effect, True
    return effect, False


def rename_impact(impact):
    if impact in ['Increase', 'Higher', 'Worsening']:
        return 'increase'
    return 'decrease'


def get_Labels(input_cui_uri):
    labels = {}
    query = """select distinct ?Drug ?drugLabel \n 
    where {?Drug <http://research.tib.eu/p4-lucat/vocab/annLabel> ?drugLabel.\n 
    FILTER (?Drug in (""" + input_cui_uri + """ ))}\n"""

    results = execute_query(query, limit=0, page=0)
    for row in results["results"]["bindings"]:
        labels[row["Drug"]["value"].replace("http://research.tib.eu/p4-lucat/entity/", "")] = row["drugLabel"]["value"].lower()

    return list(labels.values())


def query_result_p4lucat(query, labels):
    results = execute_query(query, limit=0, page=0)
    prefix = 'http://research.tib.eu/p4-lucat/entity/'
    dd = {'EffectorDrugLabel': [], 'AffectedDrugLabel': [], 'Effect': [], 'Impact': [], 'precipitantDrug': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        effect = r['Effect']['value']
        effect, pharmadynamic = store_pharmacokinetic_ddi(effect)
        dd['Effect'].append(effect.lower())
        impact = r['Impact']['value']
        impact = rename_impact(impact)
        dd['Impact'].append(impact)
        dd['EffectorDrugLabel'].append(r['EffectorDrugLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['precipitantDrug'].append(r['precipitantDrug']['value'].replace(prefix, ''))
        dd['objectDrug'].append(r['objectDrug']['value'].replace(prefix, ''))

        if pharmadynamic:
            dd['Effect'].append(effect.lower())
            impact = r['Impact']['value']
            impact = rename_impact(impact)
            dd['Impact'].append(impact)
            dd['EffectorDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
            dd['AffectedDrugLabel'].append(r['EffectorDrugLabel']['value'].lower())
            dd['precipitantDrug'].append(r['objectDrug']['value'].replace(prefix, ''))
            dd['objectDrug'].append(r['precipitantDrug']['value'].replace(prefix, ''))

    set_DDIs = pd.DataFrame(dd)
    set_DDIs = set_DDIs.loc[set_DDIs.EffectorDrugLabel.isin(labels)]
    set_DDIs = set_DDIs.loc[set_DDIs.AffectedDrugLabel.isin(labels)]
    set_DDIs.drop_duplicates(inplace=True)
    return set_DDIs


def combine_col(corpus, cols):
    # corpus = corpus.apply(lambda x: x.astype(str).str.lower())
    name = '_'.join(cols)
    corpus[name] = corpus[cols].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    return corpus


def get_drug_label_by_category(drugs_cui, set_DDIs):
    d_label = set(set_DDIs.loc[set_DDIs.precipitantDrug.isin(drugs_cui)].EffectorDrugLabel.unique())
    d_label.update(set_DDIs.loc[set_DDIs.objectDrug.isin(drugs_cui)].AffectedDrugLabel.unique())
    return d_label


def extract_ddi(input_cui, input_cui_uri, labels):
    query = build_query_p4lucat(input_cui_uri)
    # print(query)
    union = query_result_p4lucat(query, labels)
    union = combine_col(union, ['Effect', 'Impact'])
    union = union.reset_index()
    union = union.drop(columns=['index'])
    set_dsd_label = get_drug_label_by_category(input_cui, union)
    return union, set_dsd_label


pyDatalog.create_terms('rdf_star_triple, inferred_rdf_star_triple, wedge, A, B, C, T, T2, wedge_pharmacokinetic')


def build_datalog_model(union):
    pyDatalog.clear()
    for d in union.values:
        # Extensional Database
        assert_fact('rdf_star_triple', d[0], d[1], d[2])
    # Intentional Database
    inferred_rdf_star_triple(A, B, T) <= rdf_star_triple(A, B, T)  # & (T._in(ddiTypeToxicity))
    inferred_rdf_star_triple(A, C, T2) <= inferred_rdf_star_triple(A, B, T) & rdf_star_triple(B, C, T2) & (
        T._in(ddiTypeToxicity)) & (T2._in(ddiTypeToxicity)) & (A != C)

    inferred_rdf_star_triple(A, B, T) <= rdf_star_triple(A, B, T)  # & (T._in(ddiTypeEffectiveness))
    inferred_rdf_star_triple(A, C, T2) <= inferred_rdf_star_triple(A, B, T) & rdf_star_triple(B, C, T2) & (
        T._in(ddiTypeEffectiveness)) & (T2._in(ddiTypeEffectiveness)) & (A != C)

    wedge(A, B, C, T, T2) <= inferred_rdf_star_triple(A, B, T) & inferred_rdf_star_triple(B, C, T2) & (A != C)

    wedge_pharmacokinetic(A, B, C, T, T2) <= inferred_rdf_star_triple(A, B, T) & inferred_rdf_star_triple(B, C, T2) & (
        T._in(pharmacokinetic_ddi)) & (T2._in(pharmacokinetic_ddi)) & (A != C)


def computing_wedge(set_drug_label, ddi_type):
    dict_frequency = dict()
    dict_frequency_k = dict()
    max_wedge = len(ddi_type) * comb(len(set_drug_label), 2)
    ddi_k = set.intersection(set(ddi_type), set(pharmacokinetic_ddi))
    max_wedge_k = len(ddi_k) * comb(len(set_drug_label), 2)
    # print(n_ddi, len(set_drug_label), max_wedge)
    for d in set_drug_label:
        w = wedge(A, d, C, T, T2)
        dict_frequency[d] = len(w) / max_wedge

        if max_wedge_k > 0:
            w_k = wedge_pharmacokinetic(A, d, C, T, T2)
            dict_frequency_k[d] = len(w_k) / max_wedge_k
        else:
            dict_frequency_k[d] = 0
    return dict_frequency, dict_frequency_k


ddiTypeToxicity = ["serum_concentration_increase", "metabolism_decrease", "absorption_increase", "excretion_decrease"]
ddiTypeEffectiveness = ["serum_concentration_decrease", "metabolism_increase", "absorption_decrease",
                        "excretion_increase"]
pharmacokinetic_ddi = ddiTypeToxicity + ddiTypeEffectiveness


def discovering_knowledge(union, set_dsd_label):
    dict_wedge = dict()
    plot_ddi = union[['EffectorDrugLabel', 'AffectedDrugLabel', 'Effect_Impact']]
    plot_ddi.drop_duplicates(keep='first', inplace=True)
    build_datalog_model(plot_ddi)
    ddi_type = plot_ddi.Effect_Impact.unique()
    dict_frequency, dict_frequency_k = computing_wedge(set_dsd_label, ddi_type)
    dict_frequency = dict(sorted(dict_frequency.items(), key=lambda item: item[1], reverse=True))
    dict_wedge['DDI_rate'] = dict_frequency
    max_value = max(dict_frequency.values())
    dict_wedge['most_DDI_drug'] = [key for key, value in dict_frequency.items() if value == max_value]

    dict_frequency_k = dict(sorted(dict_frequency_k.items(), key=lambda item: item[1], reverse=True))
    dict_wedge['pharmacokinetic_DDI_rate'] = dict_frequency_k
    max_value = max(dict_frequency_k.values())
    # dict_wedge['most_DDI_drug_pharmacokinetic'] = max(dict_frequency_k, key=dict_frequency_k.get)
    dict_wedge['most_DDI_drug_pharmacokinetic'] = [key for key, value in dict_frequency_k.items() if value == max_value]
    return dict_wedge


def compute_ddi_rate(treatment):
    list_treatment_evaluation = dict()
    for i in range(treatment.shape[0]):
        input_cui = treatment.treatment[i]
        input_cui_uri = create_filter_cui(input_cui)
        labels = get_Labels(input_cui_uri)
        union, set_dsd_label = extract_ddi(input_cui, input_cui_uri, labels)
        # for k in range(union.shape[0]):
        #     print(union.EffectorDrugLabel[k], union.AffectedDrugLabel[k], union.Effect[k], union.Impact[k], union.precipitantDrug[k], union.objectDrug[k], union.Effect_Impact[k])
        if union.shape[0] > 0:
            response = discovering_knowledge(union, set_dsd_label)
            # list_treatment_evaluation['Treatment_'+str(i)] = response
            list_treatment_evaluation[str(labels)] = response
        else:
            list_treatment_evaluation[str(labels)] = 'No DDIs'
    # for i in range(treatment.shape[0]):
    #     print(treatment.treatment[i])
    return list_treatment_evaluation


# if __name__ == '__main__':
#     input_data = {"Input": {"Variables": {
#         "Gender": "Male",
#         "Smoking Habit": "CurrentSmoker",
#         "Organ affected by the familiar cancer": "",
#         "Cancer Stage": "IIB",
#         "Histology": "",
#         "Molecular Markers": "ALK gene/Immunohistochemistry/Positive",
#         "PDL1 result": "PDL1 Positive"
#     }}}
#     treatment = treatment_generation.compute_treatment(input_data)
#     response = compute_ddi_rate(treatment)
#     r = json.dumps(response, indent=4)
#     print(r)
