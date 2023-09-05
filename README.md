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


## Input
List of parameters for selecting a population.

```
	{"Input": {"Variables": {
        "Gender": "",
        "Smoking Habit": "",
        "Organ affected by the familiar cancer": "",
        "Cancer Stage": "IIIB",
        "Histology": "",
        "Molecular Markers": "",
        "PDL1 result": "",
        "Oncological Treatment Type": "Chemotherapy",
        "RulesHead": "OncologicalTreatment"
    }}}
```

# Output
|                All Rules                | PCA Confidence Score |            F1 Score             | Explanations                                                                                                                                                                                                                                                                                                                          | 
|:---------------------------------------:|:--------------------:|:-------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|IF a patient is in stage IIIB THEN the patient could have received oncological treatment  Chemotherapy-Radiotherapy |0.485507246|0.0432676788998173| The PCA Confidence score is 0.485507246. There are 141 patients  in stage IIIB. There are 203 patients could have received oncological treatment  Chemotherapy-Radiotherapy . There are 67 out of 141 patients  in stage IIIB and also 67 out of 203 patients could have received oncological treatment  Chemotherapy-Radiotherapy .  |
|IF a patient has oncological treatment Adjuvant  THEN the patient could have received oncological treatment  Radiotherapy | 1 | 0.0397482616882085 | The PCA Confidence score is 1.0. There are 60 patients has oncological treatment Adjuvant. There are 636 patients could have received oncological treatment  Radiotherapy . There are 60 out of 60 patients has oncological treatment Adjuvant  and also 60 out of 636 patients could have received oncological treatment  Radiotherapy .|


|                                               Positive Outcome Rules                                                | PCA Confidence Score |            F1 Score             | Explanations                                                                                                                                                                                                                                                                                                                             | 
|:-------------------------------------------------------------------------------------------------------------------:|:--------------------:|:-------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IF a patient is in stage IIIB THEN the patient could have received oncological treatment  Chemotherapy-Radiotherapy |0.485507246|0.0432676788998173| The PCA Confidence score is 0.485507246. There are 141 patients  in stage IIIB. There are 203 patients could have received oncological treatment  Chemotherapy-Radiotherapy .There are 67 out of 141 patients  in stage IIIB and also 67 out of 203 patients could have received oncological treatment  Chemotherapy-Radiotherapy .      |
|IF a patient has oncological treatment Adjuvant  THEN the patient could have received oncological treatment  Radiotherapy | 1 | 0.0397482616882085 | The PCA Confidence score is 1.0.There are 60 patients has oncological treatment Adjuvant  .There are 636 patients could have received oncological treatment  Radiotherapy . There are 60 out of 60 patients has oncological treatment Adjuvant  and also 60 out of 636 patients could have received oncological treatment  Radiotherapy .|


|                                               Negative Outcome Rules                                                | PCA Confidence Score |            F1 Score             | Explanations    | 
|:-------------------------------------------------------------------------------------------------------------------:|:--------------------:|:-------------------------------:|:----------------|
| IF a patient is in stage IIIB THEN the patient could have received oncological treatment  Chemotherapy-Radiotherapy |0.485507246|0.0432676788998173|The PCA Confidence score is 0.485507246.There are 141 patients  in stage IIIB. There are 203 patients could have received oncological treatment  Chemotherapy-Radiotherapy . There are 67 out of 141 patients  in stage IIIB and also 67 out of 203 patients could have received oncological treatment  Chemotherapy-Radiotherapy .|


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
            "cisplatin": 0.7083333333333334,
            "levofloxacin": 0.16666666666666666,
            "ceftriaxone": 0.16666666666666666,
            "vinorelbine": 0.0
        },
        "most_DDI_drug": [
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0.4166666666666667,
            "levofloxacin": 0.3333333333333333,
            "ceftriaxone": 0.3333333333333333,
            "vinorelbine": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "cisplatin"
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
            "atorvastatin": 0.24131944444444445,
            "atenolol": 0.19618055555555555,
            "metformin": 0.1284722222222222,
            "amlodipine": 0.10590277777777778,
            "enalapril": 0.059027777777777776,
            "vinorelbine": 0.057291666666666664,
            "carboplatin": 0.03819444444444445,
            "regular insulin, human": 0.027777777777777776,
            "omeprazole": 0.026041666666666668
        },
        "most_DDI_drug": [
            "atorvastatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "atorvastatin": 0.5833333333333334,
            "atenolol": 0.4166666666666667,
            "vinorelbine": 0.1388888888888889,
            "omeprazole": 0.1388888888888889,
            "amlodipine": 0.1388888888888889,
            "carboplatin": 0.07407407407407407,
            "metformin": 0.07407407407407407,
            "regular insulin, human": 0.0,
            "enalapril": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
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
            "carboplatin": 0.6,
            "paclitaxel": 0.3333333333333333,
            "tramadol": 0.26666666666666666
        },
        "most_DDI_drug": [
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "tramadol": 0.4444444444444444,
            "carboplatin": 0.1111111111111111,
            "paclitaxel": 0.1111111111111111
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
            "atorvastatin": 0.2,
            "cisplatin": 0.2,
            "omeprazole": 0.2,
            "vinorelbine": 0.0,
            "enalapril": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "atorvastatin",
            "cisplatin",
            "omeprazole"
        ]
    },
    "['paclitaxel', 'omeprazole']": {
        "DDI_rate": {
            "omeprazole": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug": [
            "omeprazole",
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "omeprazole": 0.0,
            "paclitaxel": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "omeprazole",
            "paclitaxel"
        ]
    },
    "['atezolizumab', 'albuterol', 'enalapril']": {
        "DDI_rate": {
            "albuterol": 0.0,
            "enalapril": 0.0
        },
        "most_DDI_drug": [
            "albuterol",
            "enalapril"
        ],
        "pharmacokinetic_DDI_rate": {
            "albuterol": 0,
            "enalapril": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "albuterol",
            "enalapril"
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
            "vincristine": 0.9125,
            "doxorubicin": 0.3875,
            "cyclophosphamide": 0.275,
            "omeprazole": 0.125,
            "daptomycin": 0.0
        },
        "most_DDI_drug": [
            "vincristine"
        ],
        "pharmacokinetic_DDI_rate": {
            "omeprazole": 0.3333333333333333,
            "doxorubicin": 0.16666666666666666,
            "vincristine": 0.16666666666666666,
            "cyclophosphamide": 0.06666666666666667,
            "daptomycin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "omeprazole"
        ]
    },
    "['paclitaxel', 'simvastatin']": {
        "DDI_rate": {
            "paclitaxel": 0.0,
            "simvastatin": 0.0
        },
        "most_DDI_drug": [
            "paclitaxel",
            "simvastatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "paclitaxel": 0.0,
            "simvastatin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "paclitaxel",
            "simvastatin"
        ]
    },
    "['vinorelbine', 'carboplatin', 'omeprazole', 'atorvastatin']": {
        "DDI_rate": {
            "carboplatin": 0.0,
            "vinorelbine": 0.0,
            "atorvastatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug": [
            "carboplatin",
            "vinorelbine",
            "atorvastatin",
            "omeprazole"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0.0,
            "vinorelbine": 0.0,
            "atorvastatin": 0.0,
            "omeprazole": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "vinorelbine",
            "atorvastatin",
            "omeprazole"
        ]
    },
    "['cisplatin', 'pemetrexed', 'metformin']": {
        "DDI_rate": {
            "pemetrexed": 0.75,
            "cisplatin": 0.5,
            "metformin": 0.25
        },
        "most_DDI_drug": [
            "pemetrexed"
        ],
        "pharmacokinetic_DDI_rate": {
            "metformin": 0.5,
            "pemetrexed": 0.5,
            "cisplatin": 0.3333333333333333
        },
        "most_DDI_drug_pharmacokinetic": [
            "metformin",
            "pemetrexed"
        ]
    },
    "['carboplatin', 'omeprazole', 'simvastatin', 'vp-16']": {
        "DDI_rate": {
            "omeprazole": 0.0,
            "simvastatin": 0.0
        },
        "most_DDI_drug": [
            "omeprazole",
            "simvastatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "omeprazole": 0.0,
            "simvastatin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "omeprazole",
            "simvastatin"
        ]
    },
    "['carboplatin', 'paclitaxel', 'atenolol', 'atenolol 50 mg oral tablet']": {
        "DDI_rate": {
            "paclitaxel": 0.5,
            "carboplatin": 0.0,
            "atenolol": 0.0
        },
        "most_DDI_drug": [
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0.0,
            "paclitaxel": 0.0,
            "atenolol": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "paclitaxel",
            "atenolol"
        ]
    },
    "['gemcitabine', 'carboplatin', 'omeprazole']": {
        "DDI_rate": {
            "gemcitabine": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "gemcitabine",
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "gemcitabine": 0,
            "carboplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "gemcitabine",
            "carboplatin"
        ]
    },
    "['vinorelbine', 'carboplatin']": {
        "DDI_rate": {
            "carboplatin": 0.0,
            "vinorelbine": 0.0
        },
        "most_DDI_drug": [
            "carboplatin",
            "vinorelbine"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0,
            "vinorelbine": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "vinorelbine"
        ]
    },
    "['bevacizumab', 'carboplatin', 'paclitaxel']": {
        "DDI_rate": {
            "carboplatin": 1.3333333333333333,
            "bevacizumab": 1.3333333333333333,
            "paclitaxel": 1.3333333333333333
        },
        "most_DDI_drug": [
            "carboplatin",
            "bevacizumab",
            "paclitaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "carboplatin": 0,
            "bevacizumab": 0,
            "paclitaxel": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "carboplatin",
            "bevacizumab",
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
            "cisplatin": 0.0,
            "docetaxel": 0.0
        },
        "most_DDI_drug": [
            "cisplatin",
            "docetaxel"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0,
            "docetaxel": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "cisplatin",
            "docetaxel"
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
            "daratumumab": 0.0,
            "nivolumab": 0.0
        },
        "most_DDI_drug": [
            "daratumumab",
            "nivolumab"
        ],
        "pharmacokinetic_DDI_rate": {
            "daratumumab": 0,
            "nivolumab": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "daratumumab",
            "nivolumab"
        ]
    },
    "['other', 'docetaxel']": "No DDIs"
}
```

# 4) Get the DFIs and DDIs.
## Input
List of drugs CUIs and foods CUIs
```
	{
        "Input": {"OncologicalDrugs": ["C0068334", "C0031937", "C0022209", "C4519536", "C3852938", "C0002333"],
                  "Non_OncologicalDrugs": ["C0000956", "C0008024", "C0002823", "C0005640"], "Foods": ["C0001975", "C0019588", "C0947567", "C0006644", "C0032821", "C0813171"]}
    }
```
## Output
List of DFIs and DDIs and list of drugs and foods effects.
```
	{
    "DDIs": [
        "nabumetone can decrease hemorrhage of acenocoumarol",
        "acenocoumarol can decrease hemorrhage of nabumetone",
        "acenocoumarol can decrease hemorrhage of ancrod",
        "ancrod can decrease hemorrhage of acenocoumarol",
        "acenocoumarol can decrease contusions of chenodeoxycholic acid",
        "chenodeoxycholic acid can decrease contusions of acenocoumarol",
        "acenocoumarol can decrease hemorrhage of chenodeoxycholic acid",
        "chenodeoxycholic acid can decrease hemorrhage of acenocoumarol",
        "ancrod can decrease contusions of chenodeoxycholic acid",
        "chenodeoxycholic acid can decrease contusions of ancrod",
        "ancrod can decrease hemorrhage of chenodeoxycholic acid",
        "chenodeoxycholic acid can decrease hemorrhage of ancrod",
        "dicumarol can decrease hemorrhage of ancrod",
        "ancrod can decrease hemorrhage of dicumarol",
        "dicumarol can decrease contusions of chenodeoxycholic acid",
        "chenodeoxycholic acid can decrease contusions of dicumarol",
        "dicumarol can decrease hemorrhage of chenodeoxycholic acid",
        "chenodeoxycholic acid can decrease hemorrhage of dicumarol",
        "nabumetone can decrease hemorrhage of ancrod",
        "ancrod can decrease hemorrhage of nabumetone",
        "nabumetone can decrease hemorrhage of dicumarol",
        "dicumarol can decrease hemorrhage of nabumetone",
        "pindolol can decrease aspects of adverse effects of acenocoumarol",
        "acenocoumarol can decrease aspects of adverse effects of pindolol",
        "pindolol can decrease aspects of adverse effects of dicumarol",
        "dicumarol can decrease aspects of adverse effects of pindolol",
        "alprazolam can decrease aspects of adverse effects of pindolol",
        "pindolol can decrease aspects of adverse effects of alprazolam",
        "isoniazid can decrease malignant carcinoid syndrome of pindolol",
        "pindolol can decrease malignant carcinoid syndrome of isoniazid"
    ],
    "DrugEffects": [],
    "DFIs": [
        "alcohol can decrease additive_drug_effects of pindolol",
        "alcohol can decrease gastrointestinal_irritation of nabumetone",
        "histamine can decrease headaches of isoniazid",
        "st_johns_wort can decrease serum_concentration of letermovir",
        "st_johns_wort can decrease serum_concentration of glecaprevir",
        "alcohol can decrease isoniazid of isoniazid",
        "alcohol can decrease central_nervous_system_depressants of alprazolam"
    ],
    "FoodEffects": [
        "The effectiveness of letermovir is decreased because st_johns_wort can decrease serum_concentration of letermovir",
        "The effectiveness of glecaprevir is decreased because st_johns_wort can decrease serum_concentration of glecaprevir"
    ]
}
```
