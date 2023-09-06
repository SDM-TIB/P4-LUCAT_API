import json
import pandas as pd
pd.options.mode.chained_assignment = None
from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, load, ask
from SPARQLWrapper import SPARQLWrapper, JSON

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
    select distinct ?EffectorLabel ?AffectedDrugLabel ?Effect  ?Impact ?precipitant ?objectDrug
        where {
        {{?ddi a p4-lucat:PharmacokyneticDrugDrugInteraction.  BIND('Pharmacokinetics' as ?type)} 
        UNION {?sim a p4-lucat:PharmacodynamicDrugDrugInteraction . 
                            ?sim <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?ddi.BIND('Pharmadynamics' as ?type) }}
        ?ddi p4-lucat:precipitantDrug ?precipitant . 
        ?ddi p4-lucat:objectDrug ?objectDrug .
        ?ddi p4-lucat:effect ?o . 
        ?o <http://research.tib.eu/p4-lucat/vocab/annLabel> ?Effect . 
        ?ddi p4-lucat:impact ?Impact .
        ?precipitant <http://research.tib.eu/p4-lucat/vocab/annLabel> ?EffectorLabel.
        ?objectDrug <http://research.tib.eu/p4-lucat/vocab/annLabel> ?AffectedDrugLabel.

    FILTER (?precipitant in (""" + input_cui_uri + """ ) && ?objectDrug in (""" + input_cui_uri + """))
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
        labels[row["Drug"]["value"].replace("http://research.tib.eu/p4-lucat/entity/", "")] = row["drugLabel"][
            "value"].lower()
    return list(labels.values())


def query_result_p4lucat(query, labels):
    results = execute_query(query, limit=0, page=0)
    prefix = 'http://research.tib.eu/p4-lucat/entity/'
    dd = {'EffectorLabel': [], 'AffectedDrugLabel': [], 'Effect': [], 'Impact': [], 'precipitant': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        effect = r['Effect']['value']
        effect, pharmadynamic = store_pharmacokinetic_ddi(effect)
        dd['Effect'].append(effect.lower())
        impact = r['Impact']['value']
        impact = rename_impact(impact)
        dd['Impact'].append(impact)
        dd['EffectorLabel'].append(r['EffectorLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['precipitant'].append(r['precipitant']['value'].replace(prefix, ''))
        dd['objectDrug'].append(r['objectDrug']['value'].replace(prefix, ''))

        if pharmadynamic:
            dd['Effect'].append(effect.lower())
            impact = r['Impact']['value']
            impact = rename_impact(impact)
            dd['Impact'].append(impact)
            dd['EffectorLabel'].append(r['AffectedDrugLabel']['value'].lower())
            dd['AffectedDrugLabel'].append(r['EffectorLabel']['value'].lower())
            dd['precipitant'].append(r['objectDrug']['value'].replace(prefix, ''))
            dd['objectDrug'].append(r['precipitant']['value'].replace(prefix, ''))

    set_DDIs = pd.DataFrame(dd)
    set_DDIs = set_DDIs.loc[set_DDIs.EffectorLabel.isin(labels)]
    set_DDIs = set_DDIs.loc[set_DDIs.AffectedDrugLabel.isin(labels)]
    set_DDIs.drop_duplicates(inplace=True)
    return set_DDIs


def combine_col(corpus, cols):
    # corpus = corpus.apply(lambda x: x.astype(str).str.lower())
    name = '_'.join(cols)
    corpus[name] = corpus[cols].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    return corpus


def get_drug_label_by_category(drugs_cui, set_DDIs):
    d_label = set(set_DDIs.loc[set_DDIs.precipitant.isin(drugs_cui)].EffectorLabel.unique())
    d_label.update(set_DDIs.loc[set_DDIs.objectDrug.isin(drugs_cui)].AffectedDrugLabel.unique())
    return d_label


def build_query_dfi(input_cui_uri):
    query = """prefix p4-lucat: <http://research.tib.eu/p4-lucat/vocab/>
select distinct ?EffectorLabel ?AffectedDrugLabel ?Effect  ?Impact ?precipitant ?objectDrug
        where {
        ?dfi a p4-lucat:DrugFoodInteraction .
        ?dfi p4-lucat:precipitantFood ?food . 
        ?dfi p4-lucat:objectDrug ?objectDB .
        ?dfi p4-lucat:effect ?eff .
        ?dfi p4-lucat:impact ?imp .

        ?eff p4-lucat:effect ?Effect .        
        ?imp p4-lucat:impact ?Impact .

        ?food p4-lucat:hasCUIAnnotation ?precipitant .
        ?food p4-lucat:foodLabel ?EffectorLabel .

        ?objectDB p4-lucat:hasCUIAnnotation ?objectDrug .
        #?objectDB p4-lucat:drugLabel ?AffectedDrugLabel .
        ?objectDrug p4-lucat:annLabel ?AffectedDrugLabel .
FILTER (?precipitant in (""" + input_cui_uri + """ ) && ?objectDrug in (""" + input_cui_uri + """))
}
"""
    return query


def query_result_dfi(query, labels):
    results = execute_query(query, limit=0, page=0)
    prefix = 'http://research.tib.eu/p4-lucat/entity/'
    dd = {'EffectorLabel': [], 'AffectedDrugLabel': [], 'Effect': [], 'Impact': [], 'precipitant': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        effect = r['Effect']['value']
        effect, pharmadynamic = store_pharmacokinetic_ddi(effect)
        dd['Effect'].append(effect.lower())
        impact = r['Impact']['value']
        impact = rename_impact(impact)
        dd['Impact'].append(impact)
        dd['EffectorLabel'].append(r['EffectorLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['precipitant'].append(r['precipitant']['value'].replace(prefix, ''))
        dd['objectDrug'].append(r['objectDrug']['value'].replace(prefix, ''))

    set_DFI = pd.DataFrame(dd)
    set_DFI = set_DFI.loc[set_DFI.EffectorLabel.isin(labels)]
    set_DFI = set_DFI.loc[set_DFI.AffectedDrugLabel.isin(labels)]
    set_DFI.drop_duplicates(inplace=True)
    return set_DFI


def get_label_food(input_cui_uri):
    labels = {}
    query = """prefix p4-lucat: <http://research.tib.eu/p4-lucat/vocab/>
    select distinct ?Food ?foodLabel
        where {
        ?food_uri p4-lucat:hasCUIAnnotation ?Food .
        ?food_uri p4-lucat:foodLabel ?foodLabel .
        FILTER (?Food in (""" + input_cui_uri + """ ))}"""

    results = execute_query(query, limit=0, page=0)
    for row in results["results"]["bindings"]:
        labels[row["Food"]["value"].replace("http://research.tib.eu/p4-lucat/entity/", "")] = row["foodLabel"][
            "value"].lower()
    return list(labels.values())


def extract_ddi_dfi(file):
    onco_drugs = file["Input"]["OncologicalDrugs"]
    non_onco_drugs = file["Input"]["Non_OncologicalDrugs"]
    foods = file["Input"]["Foods"]
    input_cui = onco_drugs + non_onco_drugs
    input_cui_uri = create_filter_cui(input_cui)
    """extracting DDIs"""
    labels = get_Labels(input_cui_uri)
    query = build_query_p4lucat(input_cui_uri)
    union = query_result_p4lucat(query, labels)
    union = combine_col(union, ['Effect', 'Impact'])
    union = union.reset_index()
    union = union.drop(columns=['index'])
    set_dsd_label = get_drug_label_by_category(input_cui, union)
    """extracting DFIs"""
    input_cui = input_cui + foods
    input_cui_uri = create_filter_cui(input_cui)

    label_food = get_label_food(create_filter_cui(foods))
    labels = labels + label_food
    query = build_query_dfi(input_cui_uri)
    dfi = query_result_dfi(query, labels)
    dfi = combine_col(dfi, ['Effect', 'Impact'])
    dfi = dfi.reset_index()
    dfi = dfi.drop(columns=['index'])
    # set_food_label = get_drug_label_by_category(foods, dfi)
    set_food_label = set(dfi.EffectorLabel.unique())

    ddi_dfi = pd.concat([union, dfi])
    ddi_dfi = ddi_dfi.reset_index()
    ddi_dfi = ddi_dfi.drop(columns=['index'])

    return ddi_dfi, union, dfi, set_dsd_label, set_food_label


pyDatalog.create_terms('ddi_triple, deduced_ddi_triple, dfi_triple, deduced_dfi_triple, A, B, C, T, T2')


def build_datalog_model(ddi, dfi):
    pyDatalog.clear()
    for d in ddi.values:
        # Extensional Database
        assert_fact('ddi_triple', d[0], d[1], d[2])
    for d in dfi.values:
        # Extensional Database
        assert_fact('dfi_triple', d[0], d[1], d[2])
    # Intentional Database
    deduced_ddi_triple(A, B, T) <= ddi_triple(A, B, T)
    deduced_ddi_triple(A, C, T2) <= deduced_ddi_triple(A, B, T) & ddi_triple(B, C, T2) & (
        T._in(ddiTypeToxicity)) & (T2._in(ddiTypeToxicity)) & (A != C)
    deduced_ddi_triple(A, B, T) <= ddi_triple(A, B, T)
    deduced_ddi_triple(A, C, T2) <= deduced_ddi_triple(A, B, T) & ddi_triple(B, C, T2) & (
        T._in(ddiTypeEffectiveness)) & (T2._in(ddiTypeEffectiveness)) & (A != C)
    # === Intentional Database. DFI ===
    deduced_dfi_triple(A, B, T) <= dfi_triple(A, B, T)
    deduced_dfi_triple(A, C, T2) <= deduced_dfi_triple(A, B, T) & deduced_ddi_triple(B, C, T2) & (
        T._in(ddiTypeToxicity)) & (T2._in(ddiTypeToxicity)) & (A != C)
    deduced_dfi_triple(A, B, T) <= dfi_triple(A, B, T)
    deduced_dfi_triple(A, C, T2) <= deduced_dfi_triple(A, B, T) & deduced_ddi_triple(B, C, T2) & (
        T._in(ddiTypeEffectiveness)) & (T2._in(ddiTypeEffectiveness)) & (A != C)


def get_indirect_ddi(indirect_ddi, dsd, deduced_ddi):
    for i in range(len(deduced_ddi)):
        t = deduced_ddi[i][1].split('_')
        effect = '_'.join(t[:-1])
        impact = t[-1]
        x = {'EffectorLabel': [deduced_ddi[i][0]], 'AffectedDrugLabel': dsd,
             'Effect': effect, 'Impact': impact, 'Effect_Impact': deduced_ddi[i][1]}
        indirect_ddi = pd.concat([indirect_ddi, pd.DataFrame(data=x)])
    return indirect_ddi


def get_deduced_interaction(ddi, dfi, set_dsd_label):
    set_ddi = ddi[['EffectorLabel', 'AffectedDrugLabel', 'Effect_Impact', 'Effect', 'Impact']]
    set_dfi = dfi[['EffectorLabel', 'AffectedDrugLabel', 'Effect_Impact', 'Effect', 'Impact']]
    build_datalog_model(set_ddi, set_dfi)
    indirect_ddi = pd.DataFrame(columns=['EffectorLabel', 'AffectedDrugLabel', 'Effect', 'Impact', 'Effect_Impact'])
    indirect_dfi = pd.DataFrame(columns=['EffectorLabel', 'AffectedDrugLabel', 'Effect', 'Impact', 'Effect_Impact'])
    for dsd in set_dsd_label:
        deduced_ddi = deduced_ddi_triple(C, dsd, T)
        indirect_ddi = get_indirect_ddi(indirect_ddi, dsd, deduced_ddi)
        deduced_dfi = deduced_dfi_triple(C, dsd, T)
        indirect_dfi = get_indirect_ddi(indirect_dfi, dsd, deduced_dfi)

    graph_ddi = pd.concat([set_ddi, indirect_ddi])
    graph_ddi.drop_duplicates(keep='first', inplace=True)
    graph_dfi = pd.concat([set_dfi, indirect_dfi])
    graph_dfi.drop_duplicates(keep='first', inplace=True)
    return graph_ddi, graph_dfi


def get_interaction_in_text(set_DDIs):
    list_ddi = []
    list_effect = []
    for i in range(set_DDIs.shape[0]):
        ddi = set_DDIs.iloc[i]['Effect_Impact']
        ddi_type = set_DDIs.iloc[i]['EffectorLabel'] + ' can ' + set_DDIs.iloc[i]['Impact'] + ' ' + set_DDIs.iloc[i][
                       'Effect'] + ' of ' + set_DDIs.iloc[i]['AffectedDrugLabel']
        if ddi in ddiTypeToxicity:
            tox_increase = "The toxicity of  " + set_DDIs.iloc[i][
                'AffectedDrugLabel'] + " is increased because " + ddi_type
            list_effect.append(tox_increase)
        elif ddi in ddiTypeEffectiveness:
            effectiv_decrease = "The effectiveness of " + set_DDIs.iloc[i][
                'AffectedDrugLabel'] + " is decreased because " + ddi_type
            list_effect.append(effectiv_decrease)
        list_ddi.append(ddi_type)

    return list_effect, list_ddi


ddiTypeToxicity = ["serum_concentration_increase", "metabolism_decrease", "absorption_increase", "excretion_decrease"]
ddiTypeEffectiveness = ["serum_concentration_decrease", "metabolism_increase", "absorption_decrease",
                        "excretion_increase"]
pharmacokinetic_ddi = ddiTypeToxicity + ddiTypeEffectiveness


def get_DDI_DFI(input_list):
    ddi_dfi, ddi, dfi, set_dsd_label, set_food_label = extract_ddi_dfi(input_list)
    df_ddi, df_dfi = get_deduced_interaction(ddi, dfi, set_dsd_label)
    response = dict()
    list_effect, list_ddi = get_interaction_in_text(df_ddi)
    response["DDIs"] = list_ddi
    response["DrugEffects"] = list_effect
    list_effect, list_dfi = get_interaction_in_text(df_dfi)
    response["DFIs"] = list_dfi
    response["FoodEffects"] = list_effect
    return response


if __name__ == '__main__':
    input_list = {
        "Input": {"OncologicalDrugs": ["C0015133","C0079083","C0377401","C0377401","C0008838","C0078257"],
                  "Non_OncologicalDrugs": ["C0009214","C0028978","C0064636","C0207683","C1871526"], "Foods": ["C0001975", "C0019588", "C0947567", "C0006644", "C0032821", "C0813171"]}
    }
    ddi_dfi, ddi, dfi, set_dsd_label, set_food_label = extract_ddi_dfi(input_list)
    df_ddi, df_dfi = get_deduced_interaction(ddi, dfi, set_dsd_label)

    response = dict()
    list_effect, list_ddi = get_interaction_in_text(df_ddi)
    response["DDIs"] = list_ddi
    response["DrugEffects"] = list_effect
    list_effect, list_dfi = get_interaction_in_text(df_dfi)
    response["DFIs"] = list_dfi
    response["FoodEffects"] = list_effect
    r = json.dumps(response, indent=4)
    print(r)
