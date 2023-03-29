# P4-LUCAT_API

The P4-LUCAT knowledge graph contains the data for Lung cancer patients. The main goal of a lung cancer data ecosystem in P4-LUCAT is to perform analysis that give oncologists insights
to improve the management of patients with lung cancer during their treatment, follow-up, and last period of life through data-driven techniques.

# 1) Drug-Drug Interactions (DDI) API

We are interested in computing the correlation between a DDI in treatment and the number of patients with a specific response to the treatment.
The treatment responses are evaluated in four categories: complete therapeutic response and stable disease are positive responses to treatment,
while partial therapeutic response and disease progression are negative responses. In this particular API, the lung cancer patients are extracted from the P4-LUCAT KG
based on the selected population from the Input form. For this particular population of lung cancer patients the API will output the following:
Treatment
Response
Oncological Drugs
Non-Oncological Drugs
Drug-Drug Interactions

# Input
<html>
Gender: <input> <br />
Smoking habit: <input> <br />
Organ affected by the cancer of a familiar: <input> <br />
Cancer stage: <input> <br />
Histology: <input> <br />
Molecular markers and associated results: <input> <br />
PDL1 result: <input> <br />
Oncological Treatment Type: <input> <br />

# Output

JSON format:


    {
        "1111529_LCPatient": {
            "231_Treatment": [
                {
                    "Disease_Progression": [
                        {
                            "OncologicalDrugs": "Pemetrexed",
                            "NonOncologicalDrugs": null,
                            "DDI_Literature": "DB00338_interactsWith_Literature_DB00642",
                            "DDI_DeductiveSystem": "DB00958_interactsWith_DeductiveSystem_DB00331_excretion",
                            "DDI_DrugBank": "DB00958_interactsWith_DrugBank_DB00331_excretion"
                        },
                        {
                            "OncologicalDrugs": "Pemetrexed",
                            "NonOncologicalDrugs": null,
                            "DDI_Literature": "DB00338_interactsWith_Literature_DB00642",
                            "DDI_DeductiveSystem": "DB00958_interactsWith_DeductiveSystem_DB00331_serum_concentration",
                            "DDI_DrugBank": "DB00958_interactsWith_DrugBank_DB00331_excretion"
                        }]}]}}


# 2) Horn Rules API

Mining Horn rules on top of knowledge graphs. The Horn rule consists of an atom that has variables at the subject or object position.
The Horn rule consists of a body with multiple atoms and a head with a single atom. In this particular API, the lung cancer patients are extracted from the P4-LUCAT KG
based on the selected population from the Input form. For this particular population of lung cancer patients the API will output the Horn rules that follow the selected population
and all the computed Metrics associated with this rules.


# Input
<html>
Gender: <input> <br />
Smoking habit: <input> <br />
Organ affected by the cancer of a familiar: <input> <br />
Cancer stage: <input> <br />
Histology: <input> <br />
Molecular markers and associated results: <input> <br />
PDL1 result: <input> <br />
Oncological Treatment Type: <input> <br />

# Output
|  |               Variables               |    Values    |                Metrics                |
|:-------:|:-------------------------------------:|:------------:|:-------------------------------------:|
|  |                Gender                 |     Male     |    (Head Coverage, [0.118357488])     |
|  |             Smoking habit             |              |    (PCA Confidence, [0.220720721])    |
|  | Organ affected by the familiar cancer |              |                                       |
|  |             Cancer stage              |     IIIA     |                                       |
|  |               Histology               |              |                                       |
|  |           Molecular markers           |              |                                       |
|  |              PDL1 result              |              |                                       |
|  |      Oncological Treatment Type       | Chemotherapy |                                       |



# 3) Compute the DDI rate of drugs for each treatment taken in a population.

A wedge is a path with two edges where edges represent DDIs. The middle-vertex is both the object drug of one interaction, and the precipitant drug of the other interaction.
A wedge w is defined as the following: w = vertex triplet(a,b,c), where:
![wedge](https://latex.codecogs.com/svg.latex?%5Cleft%5C%7B%20a%2Cb%2Cc%20%5Cright%5C%7D%20%5Csubseteq%20V%20and%20%5Cleft%5C%7B%28a%2Cb%29%2C%28b%2Cc%29%5Cright%5C%7D%20%5Csubseteq%20E)

The node 'b' is the middle-vertex of w.

# ![wedge_description](https://github.com/SDM-TIB/CLARIFY_KG_Exploration_API/blob/main/images/wedge_example.png "wedge_description")

A graph traversal method computes the wedges, and the distribution of the middle-vertex of wedges.
Maximal possible number of wedges centered at vertex v is defined as:
![Max_wedge](https://latex.codecogs.com/svg.latex?Max_%7Bwedge%7D%20%3D%20x%20*%20%5Cbinom%7Bn-1%7D%7B2%7D%20%3D%20x%20*%20%5Cfrac%7B%28n-1%29%21%7D%7B2%21%28n-3%29%21%7D)

where n: represents the number of vertex in the graph, and x: represents the set of types of DDIs.
The wedge rate centred at each drug is computed by:
![wedge_rate](https://latex.codecogs.com/svg.latex?%5Cfrac%7BW_%7Bv%7D%7D%7BMax_%7Bwedge%7D%7D)

The wedge rate represents drugs whose presence in the treatment may negatively impact effectiveness and toxicity.
Higher values in wedge rate mean drugs that correspond to the middle vertex of several wedges and may negatively impact the treatment.

A toxic drug is computed in terms of how many times this drug is a middle-vertex of the wedges in the directed graph that represent the interactions between the drugs of treatment.

- Based on the paper: [Capturing Knowledge about Drug-Drug Interactions to Enhance Treatment Effectiveness](https://doi.org/10.1145/3460210.3493560).
## Input
List of parameters for selecting a population.

```
	{"Input": {"Variables": {
        "Gender": "Male",
        "Smoking Habit": "CurrentSmoker",
        "Organ affected by the familiar cancer": "",
        "Cancer Stage": "IIB",
        "Histology": "",
        "Molecular Markers": "ALK gene/Immunohistochemistry/Positive",
        "PDL1 result": "PDL1 Positive"
    }}}
```
## Output
The DDI rate for each drug and the most DDI drug are computed for each treatment.

```
{
    "['cisplatin', 'vinorelbine', 'ceftriaxone', 'levofloxacin']": {
        "DDI_rate": {
            "cisplatin": 1.7777777777777777,
            "ceftriaxone": 0.8888888888888888,
            "levofloxacin": 0.8888888888888888,
            "vinorelbine": 0.0
        },
        "most_DDI_drug": [
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0.3333333333333333,
            "ceftriaxone": 0.3333333333333333,
            "levofloxacin": 0.3333333333333333,
            "vinorelbine": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "cisplatin",
            "ceftriaxone",
            "levofloxacin"
        ]
    },
    "['cisplatin', 'vinorelbine', 'enalapril', 'atenolol 50 mg oral tablet']": {
        "DDI_rate": {
            "vinorelbine": 0.0,
            "cisplatin": 0.0
        },
        "most_DDI_drug": [
            "vinorelbine",
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "vinorelbine": 0,
            "cisplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "vinorelbine",
            "cisplatin"
        ]
    },
    "['vinorelbine', 'carboplatin', 'atenolol', 'enalapril', 'metformin', 'omeprazole', 'amlodipine', 'atorvastatin', 'diabetes mellitus, non-insulin-dependent', 'regular insulin, human']": {
        "DDI_rate": {
            "atenolol": 0.2839506172839506,
            "atorvastatin": 0.23765432098765432,
            "metformin": 0.20987654320987653,
            "amlodipine": 0.08333333333333333,
            "carboplatin": 0.06481481481481481,
            "enalapril": 0.05246913580246913,
            "vinorelbine": 0.043209876543209874,
            "regular insulin, human": 0.024691358024691357,
            "omeprazole": 0.018518518518518517
        },
        "most_DDI_drug": [
            "atenolol"
        ],
        "pharmacokinetic_DDI_rate": {
            "atenolol": 0.5555555555555556,
            "atorvastatin": 0.5555555555555556,
            "omeprazole": 0.16666666666666666,
            "vinorelbine": 0.16666666666666666,
            "amlodipine": 0.16666666666666666,
            "metformin": 0.08333333333333333,
            "carboplatin": 0.08333333333333333,
            "regular insulin, human": 0.0,
            "enalapril": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "atenolol",
            "atorvastatin"
        ]
    },
    "['cisplatin', 'vinorelbine', 'omeprazole']": {
        "DDI_rate": {
            "cisplatin": 0.4444444444444444,
            "vinorelbine": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug": [
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "vinorelbine": 0.0,
            "cisplatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "vinorelbine",
            "cisplatin",
            "omeprazole"
        ]
    },
    "['carboplatin', 'paclitaxel', 'tramadol']": {
        "DDI_rate": {
            "carboplatin": 0.7619047619047619,
            "tramadol": 0.38095238095238093,
            "paclitaxel": 0.19047619047619047
        },
        "most_DDI_drug": [
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "tramadol": 0.3333333333333333,
            "carboplatin": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "tramadol"
        ]
    },
    "['nivolumab', 'omeprazole', 'diabetes mellitus, non-insulin-dependent', 'regular insulin, human']": "No DDIs",
    "['cisplatin', 'vinorelbine', 'enalapril', 'omeprazole', 'atorvastatin']": {
        "DDI_rate": {
            "atorvastatin": 0.23333333333333334,
            "cisplatin": 0.16666666666666666,
            "omeprazole": 0.03333333333333333,
            "vinorelbine": 0.0,
            "enalapril": 0.0
        },
        "most_DDI_drug": [
            "atorvastatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "omeprazole": 0.2,
            "atorvastatin": 0.2,
            "cisplatin": 0.2,
            "vinorelbine": 0.0,
            "enalapril": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "omeprazole",
            "atorvastatin",
            "cisplatin"
        ]
    },
    "['paclitaxel', 'omeprazole']": {
        "DDI_rate": {
            "paclitaxel": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug": [
            "paclitaxel",
            "omeprazole"
        ],
        "pharmacokinetic_DDI_rate": {
            "paclitaxel": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "paclitaxel",
            "omeprazole"
        ]
    },
    "['atezolizumab', 'albuterol', 'enalapril']": {
        "DDI_rate": {
            "enalapril": 0.0,
            "albuterol": 0.0
        },
        "most_DDI_drug": [
            "enalapril",
            "albuterol"
        ],
        "pharmacokinetic_DDI_rate": {
            "enalapril": 0,
            "albuterol": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "enalapril",
            "albuterol"
        ]
    },
    "['carboplatin', 'pemetrexed', 'simvastatin']": {
        "DDI_rate": {
            "carboplatin": 0.0,
            "pemetrexed": 0.0
        },
        "most_DDI_drug": [
            "carboplatin",
            "pemetrexed"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0,
            "pemetrexed": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "pemetrexed"
        ]
    },
    "['cyclophosphamide', 'doxorubicin', 'antibiotics', 'omeprazole', 'vincristine', 'daptomycin']": {
        "DDI_rate": {
            "vincristine": 1.06,
            "doxorubicin": 0.52,
            "omeprazole": 0.48,
            "cyclophosphamide": 0.16,
            "daptomycin": 0.0
        },
        "most_DDI_drug": [
            "vincristine"
        ],
        "pharmacokinetic_DDI_rate": {
            "omeprazole": 0.3,
            "doxorubicin": 0.1,
            "vincristine": 0.1,
            "daptomycin": 0.0,
            "cyclophosphamide": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "omeprazole"
        ]
    },
    "['paclitaxel', 'simvastatin']": {
        "DDI_rate": {
            "simvastatin": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug": [
            "simvastatin",
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "simvastatin": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "simvastatin",
            "paclitaxel"
        ]
    },
    "['vinorelbine', 'carboplatin', 'omeprazole', 'atorvastatin']": {
        "DDI_rate": {
            "vinorelbine": 0.0,
            "carboplatin": 0.0,
            "atorvastatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug": [
            "vinorelbine",
            "carboplatin",
            "atorvastatin",
            "omeprazole"
        ],
        "pharmacokinetic_DDI_rate": {
            "vinorelbine": 0.0,
            "carboplatin": 0.0,
            "atorvastatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "vinorelbine",
            "carboplatin",
            "atorvastatin",
            "omeprazole"
        ]
    },
    "['cisplatin', 'pemetrexed', 'metformin']": {
        "DDI_rate": {
            "pemetrexed": 1.3333333333333333,
            "metformin": 0.8888888888888888,
            "cisplatin": 0.6666666666666666
        },
        "most_DDI_drug": [
            "pemetrexed"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0.6666666666666666,
            "pemetrexed": 0.6666666666666666,
            "metformin": 0.6666666666666666
        },
        "most_DDI_drug_pharmacokinetic": [
            "cisplatin",
            "pemetrexed",
            "metformin"
        ]
    },
    "['carboplatin', 'omeprazole', 'simvastatin', 'vp-16']": {
        "DDI_rate": {
            "simvastatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug": [
            "simvastatin",
            "omeprazole"
        ],
        "pharmacokinetic_DDI_rate": {
            "simvastatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "simvastatin",
            "omeprazole"
        ]
    },
    "['carboplatin', 'paclitaxel', 'atenolol', 'atenolol 50 mg oral tablet']": {
        "DDI_rate": {
            "paclitaxel": 0.8888888888888888,
            "atenolol": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "atenolol": 0.0,
            "carboplatin": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "atenolol",
            "carboplatin",
            "paclitaxel"
        ]
    },
    "['gemcitabine', 'carboplatin', 'omeprazole']": {
        "DDI_rate": {
            "carboplatin": 0.0,
            "gemcitabine": 0.0
        },
        "most_DDI_drug": [
            "carboplatin",
            "gemcitabine"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0,
            "gemcitabine": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "gemcitabine"
        ]
    },
    "['vinorelbine', 'carboplatin']": {
        "DDI_rate": {
            "vinorelbine": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "vinorelbine",
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "vinorelbine": 0,
            "carboplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "vinorelbine",
            "carboplatin"
        ]
    },
    "['bevacizumab', 'carboplatin', 'paclitaxel']": {
        "DDI_rate": {
            "bevacizumab": 1.3333333333333333,
            "carboplatin": 1.3333333333333333,
            "paclitaxel": 1.3333333333333333
        },
        "most_DDI_drug": [
            "bevacizumab",
            "carboplatin",
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "bevacizumab": 0,
            "carboplatin": 0,
            "paclitaxel": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "bevacizumab",
            "carboplatin",
            "paclitaxel"
        ]
    },
    "['cisplatin', 'pemetrexed']": {
        "DDI_rate": {
            "cisplatin": 0.0,
            "pemetrexed": 0.0
        },
        "most_DDI_drug": [
            "cisplatin",
            "pemetrexed"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0,
            "pemetrexed": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "cisplatin",
            "pemetrexed"
        ]
    },
    "['cisplatin', 'docetaxel']": {
        "DDI_rate": {
            "docetaxel": 0.0,
            "cisplatin": 0.0
        },
        "most_DDI_drug": [
            "docetaxel",
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "docetaxel": 0,
            "cisplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "docetaxel",
            "cisplatin"
        ]
    },
    "['carboplatin', 'paclitaxel']": {
        "DDI_rate": {
            "carboplatin": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug": [
            "carboplatin",
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0,
            "paclitaxel": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "paclitaxel"
        ]
    },
    "['carboplatin', 'vp-16']": "No DDIs",
    "['cisplatin', 'vinorelbine']": {
        "DDI_rate": {
            "vinorelbine": 0.0,
            "cisplatin": 0.0
        },
        "most_DDI_drug": [
            "vinorelbine",
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "vinorelbine": 0,
            "cisplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "vinorelbine",
            "cisplatin"
        ]
    },
    "['carboplatin', 'pemetrexed']": {
        "DDI_rate": {
            "carboplatin": 0.0,
            "pemetrexed": 0.0
        },
        "most_DDI_drug": [
            "carboplatin",
            "pemetrexed"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0,
            "pemetrexed": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "pemetrexed"
        ]
    },
    "['daratumumab', 'nivolumab']": {
        "DDI_rate": {
            "nivolumab": 0.0,
            "daratumumab": 0.0
        },
        "most_DDI_drug": [
            "nivolumab",
            "daratumumab"
        ],
        "pharmacokinetic_DDI_rate": {
            "nivolumab": 0,
            "daratumumab": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "nivolumab",
            "daratumumab"
        ]
    },
    "['other', 'docetaxel']": "No DDIs"
}
```

## POST request example

```
curl --location --request POST 'http://194.95.157.232:5000/treatment_DDI_rate' \
--header 'Content-Type: application/json' \
--data-raw '{"Input": {"Variables": {
        "Gender": "Male",
        "Smoking Habit": "CurrentSmoker",
        "Organ affected by the familiar cancer": "",
        "Cancer Stage": "IIB",
        "Histology": "",
        "Molecular Markers": "ALK gene/Immunohistochemistry/Positive",
        "PDL1 result": "PDL1 Positive"
    }}}'
```