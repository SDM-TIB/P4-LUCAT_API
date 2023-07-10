import re
from SPARQLWrapper import SPARQLWrapper, JSON


rule = []
out_val = []
text1 = []
text2 = []
text3 = []
text4 = []

body_dict = {'key': ['?a', '  <hasStage>', '  <IIIB>', '  <hasOncologicalTreatment>', '   <Immunotherapy>  ', '  <IIIA>', '  <hasOncologicalSurgery>', '  <hasBio>', '   <Chemotherapy>  ', '   <Surgery>  ', '   <Radical>  ', '  <Radiotherapy>  ', '   <Pneumonectomy>  ', '  <Chemotherapy-Radiotherapy>', '  <Neoadjuvant>   ', '   <Adjuvant>  ', '  <Lymph_node_excision>  ', '   <Lobectomy>  ', '  <Prophylactic>   ', '  <IA>   ', '  <IA1>   ', '  <IA2>   ', '  <IB>   ', '  <IIA>   ', '  <IIB>   ', '  <III>   ', '  <IIIA>   ', '  <IIIB>   ', '  <IIIC>   ', '  <IV>   ', '  <IVA>   ', '  <IVB>   ', '  <HormonalTherapy>   ', '   <ALK>  ', '  <PDL1>  ', '  <KRAS>   ', '   <EGFR>  ', '   <BRAF>  ', '   <Pleurodesis>  '], 'value': ['IF a patient ', 'is in stage ', 'IIIB ', 'has oncological treatment  ', 'Immunotherapy ', 'IIIA ', 'has oncological surgery  ', 'is positive for biomarker  ', 'Chemotherapy ', 'Surgery ', 'Radical ', 'Radiotherapy ', 'Pneumonectomy ', 'Chemotherapy-Radiotherapy ', 'Neoadjuvant ', 'Adjuvant ', 'Lymph node excision ', 'Lobectomy ', 'Prophylactic ', 'IA ', 'IA1 ', 'IA2 ', 'IB ', 'IIA ', 'IIB ', 'III ', 'IIIA ', 'IIIB ', 'IIIC ', 'IV ', 'IVA ', 'IVB ', 'HormonalTherapy ', 'ALK ', 'PDL1 ', 'KRAS ', 'EGFR ', 'BRAF ', 'Pleurodesis ']}
head_dict = {'key': ['?a', '  <hasStage>', '  <IIIB>', '  <hasOncologicalTreatment>', '  <Immunotherapy>', '  <IIIA>', '  <hasOncologicalSurgery>', '  <hasBio>', '   <Chemotherapy>', '   <Surgery>', '   <Radical>', '  <Radiotherapy>', '   <Pneumonectomy>', '  <Chemotherapy-Radiotherapy>', '  <Neoadjuvant>', '   <Adjuvant>', '  <Lymph_node_excision>', '   <Lobectomy>', '  <Prophylactic>', '  <IA>', '  <IA1>', '  <IA2>', '  <IB>', '  <IIA>', '  <IIB>', '  <III>', '  <IIIA>', '  <IIIB>', '  <IIIC>', '  <IV>', '  <IVA>', '  <IVB>', '  <HormonalTherapy>', '   <ALK>', '  <PDL1>', '  <KRAS>', '   <EGFR>', '   <BRAF>', '   <Pleurodesis>'], 'value': ['THEN the patient could ', 'be in stage ', 'IIIB ', 'have received oncological treatment  ', 'Immunotherapy ', 'IIIA ', 'have received oncological surgery  ', 'be positive for biomarker  ', 'Chemotherapy ', 'Surgery ', 'Radical ', 'Radiotherapy ', 'Pneumonectomy ', 'Chemotherapy-Radiotherapy ', 'Neoadjuvant ', 'Adjuvant ', 'Lymph node excision ', 'Lobectomy ', 'Prophylactic ', 'IA ', 'IA1 ', 'IA2 ', 'IB ', 'IIA ', 'IIB ', 'III ', 'IIIA ', 'IIIB ', 'IIIC ', 'IV ', 'IVA ', 'IVB ', 'HormonalTherapy ', 'ALK ', 'PDL1 ', 'KRAS ', 'EGFR ', 'BRAF ', 'Pleurodesis ']}



def query_generation(rule):
    endpoint = "https://labs.tib.eu/sdm/p4lucat_kg/sparql"

    where_clause = {
        "Chemotherapy-Radiotherapy": """?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Chemotherapy-Radiotherapy>. """,
        "Neoadjuvant": """?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Neoadjuvant>. """,
        "Adjuvant": """?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Adjuvant>. """,
        "Chemotherapy":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Chemotherapy>.""",
        "Immunotherapy":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Immunotherapy>.""",
        "Radical":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Radical>.""",
        "Radiotherapy":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Radiotherapy>.""",
        "Prophylactic": """?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Prophylactic>.""",
        "Surgery":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalTreatment> <http://research.tib.eu/p4-lucat/entity/Surgery>.""",
        "PDL1":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasBio> <http://research.tib.eu/p4-lucat/entity/PDL1>.""",
        "ALK": """?patient <http://research.tib.eu/p4-lucat/vocab/hasBio> <http://research.tib.eu/p4-lucat/entity/ALK>.""",
        "EGFR": """?patient <http://research.tib.eu/p4-lucat/vocab/hasBio> <http://research.tib.eu/p4-lucat/entity/EGFR>.""",
        "BRAF": """?patient <http://research.tib.eu/p4-lucat/vocab/hasBio> <http://research.tib.eu/p4-lucat/entity/BRAF>.""",
        "Lymph_node_excision":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalSurgery> <http://research.tib.eu/p4-lucat/entity/Lymph_node_excision>.""",
        "Lobectomy":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalSurgery> <http://research.tib.eu/p4-lucat/entity/Lobectomy>.""",
        "Pneumonectomy":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalSurgery> <http://research.tib.eu/p4-lucat/entity/Pneumonectomy>.""",
        "Pleurodesis": """?patient <http://research.tib.eu/p4-lucat/vocab/hasOncologicalSurgery> <http://research.tib.eu/p4-lucat/entity/Pleurodesis>.""",
        "IIIA":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IIIA>.""",
        "IIIB":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IIIB>.""",
        "IIIC": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IIIC>.""",
        "IV":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IV>.""",
        "IVA": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IVA>.""",
        "IVB": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IVB>.""",
        "IA":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IA>.""",
        "IB":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IB>.""",
        "IIA":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IIA>.""",
        "IIB":"""?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> <http://research.tib.eu/p4-lucat/entity/IIB>."""}


    query_select_clause = "SELECT (COUNT(DISTINCT ?patient) AS ?numOutcome) "
    query_where_clause = """\n WHERE { \n ?patient a <http://research.tib.eu/p4-lucat/vocab/LCPatient> .\n"""


    for i in rule:
        query_where_clause = query_where_clause + where_clause[i] + " \n"

    query_where_clause_out = """OPTIONAL {?patient <http://research.tib.eu/p4-lucat/vocab/hasRelapse> ?relapse.}
                                OPTIONAL {?patient <http://research.tib.eu/p4-lucat/vocab/hasProgression> ?progression.}
                                OPTIONAL {?patient <http://research.tib.eu/p4-lucat/vocab/hasToxicity> ?toxicity.}
                                FILTER (BOUND(?relapse) || BOUND(?progression) || BOUND(?toxicity))"""
    sparql_query = query_select_clause + query_where_clause + "\n" + query_where_clause_out + "\n }"
    # print(sparql_query)
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]
    for row in data:
        newrow = (row["numOutcome"]["value"])
        out_val.append(newrow)

    return out_val


def process(df1):

    # df1 = pd.DataFrame.from_dict(data_dict)

    for index, row in df1.iterrows():
        b = re.findall(r"\b(?!(?:has.*|a)\b)\w+\b", row['Body'])
        h = re.findall(r"\b(?!(?:has.*|a)\b)[\w-]+\b", row['Head'])
        rule = b + h
        outval = query_generation(rule)

    supp = df1['Positive_Examples'].tolist()
    outval = [eval(i) for i in outval]

    res = [i / j for i, j in zip(outval, supp)]
    df1['Outcome'] = res
    # print(df1)
    return df1


def outcome(dataframe):
    # Create a new DataFrame for positive outcomes (outcome > 50)
    pos = dataframe[dataframe['Outcome'] > 0.50]
    # Create a new DataFrame for negative outcomes (outcome <= 50)
    neg = dataframe[dataframe['Outcome'] <= 0.50]
    return pos, neg



def mainPosNeg(data_dict):
    data = process(data_dict)
    pos, neg = outcome(data)
    return pos, neg


