import json
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import os
KG = os.environ["ENDPOINT"]
# KG = 'https://labs.tib.eu/sdm/p4lucat_kg/sparql'


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
    select distinct ?EffectorLabel ?AffectedDrugLabel ?Recommendation ?Time ?precipitant ?objectDrug
        where {

        ?dfr a p4-lucat:DrugFoodRecommendation.
        ?dfr p4-lucat:precipitantFood ?food. 
        ?dfr p4-lucat:objectDrug ?objectDB .
        ?dfr p4-lucat:recommendation ?Recommendation .
        optional{?dfr p4-lucat:time ?Time .}

        ?food p4-lucat:hasCUIAnnotation ?precipitant .
        ?food p4-lucat:foodLabel ?EffectorLabel .
        ?objectDB p4-lucat:hasCUIAnnotation ?objectDrug .
        ?objectDrug p4-lucat:annLabel ?AffectedDrugLabel .
    FILTER (?objectDrug in (""" + input_cui_uri + """))
    }"""
    return query


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
    dd = {'EffectorLabel': [], 'AffectedDrugLabel': [], 'Recommendation': [], 'Time': [], 'precipitant': [],
          'objectDrug': []}
    for r in results['results']['bindings']:
        dd['EffectorLabel'].append(r['EffectorLabel']['value'].lower())
        dd['AffectedDrugLabel'].append(r['AffectedDrugLabel']['value'].lower())
        dd['Recommendation'].append(r['Recommendation']['value'].replace(prefix, ''))

        if 'Time' in r.keys():
            dd['Time'].append(r['Time']['value'])
        else:
            dd['Time'].append(None)
        dd['precipitant'].append(r['precipitant']['value'].replace(prefix, ''))
        dd['objectDrug'].append(r['objectDrug']['value'].replace(prefix, ''))

    set_dfr = pd.DataFrame(dd)
    set_dfr = set_dfr.loc[set_dfr.AffectedDrugLabel.isin(labels)]
    set_dfr.drop_duplicates(inplace=True)
    return set_dfr


def combine_col(corpus, cols):
    name = '_'.join(cols)
    corpus[name] = corpus[cols].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    return corpus


def extract_dfr(file):
    input_cui = file["Input"]["Drugs"]
    input_cui_uri = create_filter_cui(input_cui)
    """extracting DDIs"""
    labels = get_Labels(input_cui_uri)
    query = build_query_p4lucat(input_cui_uri)
    # print(query)
    dfr = query_result_p4lucat(query, labels)
    dfr = dfr.reset_index()
    dfr = dfr.drop(columns=['index'])
    return dfr


def get_DFR(input_list):
    dfr = extract_dfr(input_list)
    dfr = dfr.iloc[:, :-2]
    dict_dfr = dfr.to_dict('records')
    response = dict()
    response['Recommendations'] = dict_dfr
    return response


if __name__ == '__main__':
    input_list = {
        "Input": {"Drugs": ["C0009214","C0028978","C0064636","C0207683","C1871526"]}
    }
    dfr = extract_dfr(input_list)
    dfr = dfr.iloc[:, :-2]
    dict_dfr = dfr.to_dict('records')
    response = dict()
    response['Recommendations'] = dict_dfr
    r = json.dumps(response, indent=4)
    print(r)
