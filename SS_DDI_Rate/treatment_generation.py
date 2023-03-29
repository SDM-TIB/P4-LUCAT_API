import json
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import os

# KG = os.environ["ENDPOINT"]
KG = 'https://labs.tib.eu/sdm/p4lucat_kg/sparql'


def query_generation(input_data):
    where_clause = {
        "Gender": """?patient <http://research.tib.eu/p4-lucat/vocab/hasGender> ?gender. """,
        "Smoking Habit": """?patient <http://research.tib.eu/p4-lucat/vocab/hasSmokingHabit> ?smoking.  """,
        "Organ affected by the familiar cancer": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                                    ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                    ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer.  """,
        "Cancer Stage": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. """,
        "Histology": """OPTIONAL{?patient <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?histologycui.
                                 ?histologycui a <http://research.tib.eu/p4-lucat/vocab/Histology> .
                                 ?histologycui <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology.""",
        "ALK gene/Immunohistochemistry/Positive": """OPTIONAL{?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "ALK"))
                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "IHQ positivo")).} \n""",
        "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation": """OPTIONAL{?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "ALK"))
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "FISH traslocado")).} \n""",
        "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "T790M -")). }\n""",
        "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                                                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (ucase(str(?biomarker_result))= "T790M +").} \n""",
        "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Exón 19")). }\n""",
        "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Exón 21")).} \n""",
        "BRAF gene/Detected (finding)": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                           ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                           ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "BRAF"))
                                           ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Se detecta")). }\n""",
        "KRAS gene/Not detected": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "KRAS"))
                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "No se detecta")).} \n""",
        "PDL1 Positive": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Positivo")).} \n""",
        "PDL1 Negative": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Negativo")).} \n""",
        "PDL1 Unkown": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Desconocido")).} \n""",
    }

    query_select_clause = "SELECT DISTINCT ?patient"
    query_where_clause = """\n WHERE { \n ?patient a <http://research.tib.eu/p4-lucat/vocab/LCPatient> .\n"""

    if "Gender" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Gender"] + "FILTER (regex(?gender,\"" + \
                             input_data["Input"]["Variables"]["Gender"] + "\"))." + " \n"
    if "Smoking Habit" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Smoking Habit"] + "FILTER (regex(?smoking,\"" + \
                             input_data["Input"]["Variables"]["Smoking Habit"] + "\"))." + " \n"
    if "Organ affected by the familiar cancer" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause[
            "Organ affected by the familiar cancer"] + "FILTER (regex(?familycancer,\"" + \
                             input_data["Input"]["Variables"][
                                 "Organ affected by the familiar cancer"] + "\" ))." + " \n"
    if "Cancer Stage" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Cancer Stage"] + "FILTER (regex(?stage,\"" + \
                             input_data["Input"]["Variables"]["Cancer Stage"] + "\"))." + " \n"
    if "Histology" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Histology"] + "FILTER (regex(?histology,\"" + \
                             input_data["Input"]["Variables"]["Histology"] + "\")).}" + " \n"
    if "ALK gene/Immunohistochemistry/Positive" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["ALK gene/Immunohistochemistry/Positive"] + " \n"
    if "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation" in input_data["Input"]["Variables"][
        "Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause[
            "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative" in input_data["Input"]["Variables"][
        "Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma" in \
            input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation" in input_data["Input"]["Variables"][
        "Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation" in input_data["Input"]["Variables"][
        "Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation"] + " \n"
    if "KRAS gene/Not detected" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["KRAS gene/Not detected"] + " \n"
    if "BRAF gene/Detected (finding)" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["BRAF gene/Detected (finding)"] + " \n"
    if "PDL1 Positive" in input_data["Input"]["Variables"]["PDL1 result"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Positive"] + " \n"
    if "PDL1 Negative" in input_data["Input"]["Variables"]["PDL1 result"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Negative"] + " \n"
    if "PDL1 Unknown" in input_data["Input"]["Variables"]["PDL1 result"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Unknown"] + " \n"

    sparqlQuery = query_select_clause + " " + query_where_clause + '}'
    # print(sparqlQuery)

    results = execute_query(sparqlQuery, limit=0, page=0)
    filter_pat_list = ''
    for r in results["results"]["bindings"]:
        filter_pat_list += '<' + r["patient"]["value"] + '>,'

    if len(filter_pat_list) > 0:
        return filter_pat_list[:-1]
    return filter_pat_list


def execute_query(query, limit=0, page=0):
    if limit != 0:
        query += "LIMIT " + str(limit)
    query += " OFFSET " + str(page)
    sparql_ins = SPARQLWrapper(KG)
    # sparql_ins.setMethod(POST)
    sparql_ins.setQuery(query)
    sparql_ins.setReturnFormat(JSON)
    return sparql_ins.query().convert()


def get_non_oncological_treatment(filter_pat_list):
    query = """prefix p4-lucat: <http://research.tib.eu/p4-lucat/vocab/>
    SELECT DISTINCT ?patient ?drug_cui WHERE {
    ?patient p4-lucat:hasNonOncologicalDrug ?nonOnco .
    FILTER(?patient in (""" + filter_pat_list + """)) .
    ?nonOnco p4-lucat:drugLabel ?drugLabel .
    ?nonOnco p4-lucat:hasCUIAnnotation ?drug_cui .
    }"""

    df = []
    results = execute_query(query, limit=0, page=0)
    for r in results['results']['bindings']:
        pat_id = r['patient']['value'].replace('http://research.tib.eu/p4-lucat/entity/', '')
        pat_id = pat_id.replace('_LCPatient', '')
        row = {'patient_id': int(pat_id),
               'CUI_ID': r['drug_cui']['value'].replace('http://research.tib.eu/p4-lucat/entity/', '')
               }
        df.append(row)
    drug_no_onco = pd.DataFrame.from_dict(df)
    drug_no_onco = drug_no_onco.groupby(by=['patient_id']).agg(lambda x: x.tolist()).reset_index()
    return drug_no_onco


def get_oncological_treatment(filter_pat_list):
    query = """SELECT DISTINCT  ?LCPatient_CT ?drug_cui  WHERE {
    ?LCPatient_CT <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient .
    FILTER(?patient in (""" + filter_pat_list + """)) .
    ?LCPatient_CT <http://research.tib.eu/p4-lucat/vocab/hasDrugID> ?drug_id .
    ?drug_id <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?drug_cui .
    }
    """
    df = []
    results = execute_query(query, limit=0, page=0)
    for r in results['results']['bindings']:
        [pat_id, line] = r['LCPatient_CT']['value'].replace('http://research.tib.eu/p4-lucat/entity/', '').split('_')
        row = {'CUI_ID': r['drug_cui']['value'].replace('http://research.tib.eu/p4-lucat/entity/', ''),
               'patient_id': int(pat_id), 't_line': int(line)}
        df.append(row)

    onco_treatment = pd.DataFrame.from_dict(df)
    onco_treatment = onco_treatment.groupby(by=['patient_id', 't_line']).agg(lambda x: x.tolist()).reset_index()
    onco_treatment.drop(columns=['t_line'], inplace=True)
    return onco_treatment


def create_treatment(drug_no_onco, onco_treatment):
    result = pd.concat([onco_treatment, drug_no_onco], axis=1)
    result.drop(columns=['patient_id'], inplace=True)
    result['treatment'] = result.applymap(lambda x: [] if x is np.nan else x).apply(lambda x: sum(x, []), axis=1)
    # result.columns=['oncological', 'nonOncological', 'treatment']
    result = result[['treatment']]

    # == sort cancer treatment and remove duplicate ==
    index = []
    for i in range(result.shape[0]):
        drugs = result.treatment[i]
        drugs.sort()
        if len(drugs) == 1:
            index.append(i)
        result.at[i, 'treatment'] = drugs
    result = result.drop(index)
    result = result.loc[result.astype(str).drop_duplicates().index].reset_index()
    result = result.drop(columns=['index'])
    return result


def compute_treatment(input_data):
    filter_pat_list = query_generation(input_data)
    drug_no_onco = get_non_oncological_treatment(filter_pat_list)
    onco_treatment = get_oncological_treatment(filter_pat_list)
    # for i in range(onco_treatment.shape[0]):
    #     print(onco_treatment.CUI_ID[i], onco_treatment.patient_id[i])
    treatment = create_treatment(drug_no_onco, onco_treatment)
    return treatment


# if __name__ == '__main__':
#     input_data = {"Input": {"Variables": {
#         "Gender": "Male",
#         "Smoking Habit": "CurrentSmoker",
#         "Organ affected by the familiar cancer": "",
#         "Cancer Stage": "IIA",
#         "Histology": "",
#         "Molecular Markers": "ALK gene/Immunohistochemistry/Positive",
#         "PDL1 result": "PDL1 Positive"
#     }}}
#     res = compute_treatment(input_data)
