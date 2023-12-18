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

### POST request example
```json
curl --location 'https://labs.tib.eu/sdm/p4_lucat_ddi_rules/rules' \
--header 'Content-Type: application/json' \
--data ' {
        "Gender": "Male",
        "SmokingHabit": "",
        "OrganAffectedByTheCancerOfFamiliar": ["others"],
        "CancerStage": "IIIB",
        "Histology": "Adenocarcinoma",
        "Molecular Markers": "",
        "PDL1Result": "Positive",
        "OncologicalTreatmentType": "Chemotherapy",
        "RulesHead": "OncologicalTreatment"
    }'
```

## Input
List of parameters for selecting a population.

```
{
  "Gender": "Male",
  "SmokingHabit": "Ex smoker (>1 year)",
  "OrganAffected": ["Malignant tumor of colon/Rectal Carcinoma"],
  "CancerStage": "IV",
  "Histology": "Adenocarcinoma",
  "Biomarkers": "No Molecular marker",
  "PDL1Result": "Unknown",
  "RulesHead": "OncologicalTreatment",
  "OncologicalTreatmentType": "Radiotherapy"
}
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
            "cisplatin": 0.4444444444444444,
            "ceftriaxone": 0.0,
            "vinorelbine": 0.0,
            "levofloxacin": 0.0
        },
        "most_DDI_drug": [
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0.3333333333333333,
            "ceftriaxone": 0.0,
            "vinorelbine": 0.0,
            "levofloxacin": 0.0
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
    "['vinorelbine', 'carboplatin', 'atenolol', 'enalapril', 'metformin', 'omeprazole', 'amlodipine', 'atorvastatin', 'diabetes mellitus, non-insulin-dependent', 'insulin, regular, human']": {
        "DDI_rate": {
            "atorvastatin": 0.18162393162393162,
            "amlodipine": 0.13034188034188035,
            "atenolol": 0.12606837606837606,
            "enalapril": 0.05128205128205128,
            "vinorelbine": 0.05128205128205128,
            "metformin": 0.05128205128205128,
            "omeprazole": 0.03205128205128205,
            "insulin, regular, human": 0.01282051282051282,
            "carboplatin": 0.004273504273504274
        },
        "most_DDI_drug": [
            "atorvastatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "atorvastatin": 0.25,
            "atenolol": 0.2037037037037037,
            "vinorelbine": 0.1388888888888889,
            "omeprazole": 0.1388888888888889,
            "amlodipine": 0.1388888888888889,
            "enalapril": 0.0,
            "carboplatin": 0.0,
            "insulin, regular, human": 0.0,
            "metformin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "atorvastatin"
        ]
    },
    "['cisplatin', 'vinorelbine', 'omeprazole']": {
        "DDI_rate": {
            "cisplatin": 0.3333333333333333,
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
            "paclitaxel": 0.25,
            "carboplatin": 0.25,
            "tramadol": 0.25
        },
        "most_DDI_drug": [
            "paclitaxel",
            "carboplatin",
            "tramadol"
        ],
        "pharmacokinetic_DDI_rate": {
            "tramadol": 0.3333333333333333,
            "paclitaxel": 0.1111111111111111,
            "carboplatin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "tramadol"
        ]
    },
    "['nivolumab', 'omeprazole', 'diabetes mellitus, non-insulin-dependent', 'insulin, regular, human']": "No DDIs",
    "['cisplatin', 'vinorelbine', 'enalapril', 'omeprazole', 'atorvastatin']": {
        "DDI_rate": {
            "atorvastatin": 0.28,
            "cisplatin": 0.12,
            "omeprazole": 0.04,
            "enalapril": 0.0,
            "vinorelbine": 0.0
        },
        "most_DDI_drug": [
            "atorvastatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "cisplatin": 0.2,
            "omeprazole": 0.2,
            "atorvastatin": 0.2,
            "enalapril": 0.0,
            "vinorelbine": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "cisplatin",
            "omeprazole",
            "atorvastatin"
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
            "pemetrexed": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "pemetrexed",
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "pemetrexed": 0,
            "carboplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "pemetrexed",
            "carboplatin"
        ]
    },
    "['carboplatin', 'antibiotics', 'omeprazole', 'daptomycin', 'vp-16']": {
        "DDI_rate": {
            "daptomycin": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "daptomycin",
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "daptomycin": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "daptomycin",
            "carboplatin"
        ]
    },
    "['simvastatin', 'cyclophosphamide', 'doxorubicin', 'vincristine']": {
        "DDI_rate": {
            "vincristine": 0.25,
            "cyclophosphamide": 0.25,
            "simvastatin": 0.16666666666666666,
            "doxorubicin": 0.16666666666666666
        },
        "most_DDI_drug": [
            "vincristine",
            "cyclophosphamide"
        ],
        "pharmacokinetic_DDI_rate": {
            "simvastatin": 0.08333333333333333,
            "vincristine": 0.0,
            "doxorubicin": 0.0,
            "cyclophosphamide": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "simvastatin"
        ]
    },
    "['paclitaxel', 'omeprazole', 'atorvastatin']": {
        "DDI_rate": {
            "paclitaxel": 0.6666666666666666,
            "atorvastatin": 0.6666666666666666,
            "omeprazole": 0.6666666666666666
        },
        "most_DDI_drug": [
            "paclitaxel",
            "atorvastatin",
            "omeprazole"
        ],
        "pharmacokinetic_DDI_rate": {
            "paclitaxel": 0.6666666666666666,
            "atorvastatin": 0.6666666666666666,
            "omeprazole": 0.6666666666666666
        },
        "most_DDI_drug_pharmacokinetic": [
            "paclitaxel",
            "atorvastatin",
            "omeprazole"
        ]
    },
    "['vinorelbine', 'carboplatin', 'metformin']": {
        "DDI_rate": {
            "carboplatin": 0.2222222222222222,
            "vinorelbine": 0.0,
            "metformin": 0.0
        },
        "most_DDI_drug": [
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "vinorelbine": 0.0,
            "metformin": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "vinorelbine",
            "metformin",
            "carboplatin"
        ]
    },
    "['cisplatin', 'pemetrexed', 'omeprazole', 'simvastatin']": {
        "DDI_rate": {
            "pemetrexed": 0.8333333333333334,
            "cisplatin": 0.8333333333333334,
            "simvastatin": 0.5,
            "omeprazole": 0.5
        },
        "most_DDI_drug": [
            "pemetrexed",
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "pemetrexed": 1.0,
            "simvastatin": 1.0,
            "cisplatin": 1.0,
            "omeprazole": 1.0
        },
        "most_DDI_drug_pharmacokinetic": [
            "pemetrexed",
            "simvastatin",
            "cisplatin",
            "omeprazole"
        ]
    },
    "['carboplatin', 'atenolol', 'atenolol 50 mg oral tablet', 'vp-16']": "No DDIs",
    "['carboplatin', 'paclitaxel']": {
        "DDI_rate": {
            "paclitaxel": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "paclitaxel",
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "paclitaxel": 0,
            "carboplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "paclitaxel",
            "carboplatin"
        ]
    },
    "['gemcitabine', 'carboplatin']": {
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
            "paclitaxel": 0.6666666666666666,
            "carboplatin": 0.6666666666666666,
            "bevacizumab": 0.6666666666666666
        },
        "most_DDI_drug": [
            "paclitaxel",
            "carboplatin",
            "bevacizumab"
        ],
        "pharmacokinetic_DDI_rate": {
            "paclitaxel": 0,
            "carboplatin": 0,
            "bevacizumab": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "paclitaxel",
            "carboplatin",
            "bevacizumab"
        ]
    },
    "['cisplatin', 'pemetrexed']": {
        "DDI_rate": {
            "pemetrexed": 0.0,
            "cisplatin": 0.0
        },
        "most_DDI_drug": [
            "pemetrexed",
            "cisplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "pemetrexed": 0,
            "cisplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "pemetrexed",
            "cisplatin"
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
            "pemetrexed": 0.0,
            "carboplatin": 0.0
        },
        "most_DDI_drug": [
            "pemetrexed",
            "carboplatin"
        ],
        "pharmacokinetic_DDI_rate": {
            "pemetrexed": 0,
            "carboplatin": 0
        },
        "most_DDI_drug_pharmacokinetic": [
            "pemetrexed",
            "carboplatin"
        ]
    },
    "['pembrolizumab', 'abemaciclib']": "No DDIs",
    "['ipilimumab', 'osimertinib']": "No DDIs",
    "['nivolumab', 'daratumumab']": {
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
        "Input": {"OncologicalDrugs": ["C0015133","C0079083","C0377401","C0377401","C0008838","C0078257"],
                  "Non_OncologicalDrugs": ["C0009214","C0028978","C0064636","C0207683","C1871526"], "Foods": ["C0001975", "C0019588", "C0947567", "C0006644", "C0032821", "C0813171"]}
    }
```
## Output
List of DFIs and foods effects.
```
{
    "DFIs": [
        "grapefruit_products can decrease serum_concentration of etoposide",
        "st_johns_wort can decrease serum_concentration of etoposide",
        "grapefruit_products can decrease serum_concentration of vinorelbine",
        "st_johns_wort can decrease serum_concentration of vinorelbine"
    ],
    "FoodEffects": [
        "The effectiveness of etoposide is decreased because grapefruit_products can decrease serum_concentration of etoposide",
        "The effectiveness of etoposide is decreased because st_johns_wort can decrease serum_concentration of etoposide",
        "The effectiveness of vinorelbine is decreased because grapefruit_products can decrease serum_concentration of vinorelbine",
        "The effectiveness of vinorelbine is decreased because st_johns_wort can decrease serum_concentration of vinorelbine"
    ]
}
```

# 5) Get the recommendations of a set of drugs. 
## Input
List of drugs CUIs
```
	{
    "Input": {"Drugs": ["C0009214","C0028978","C0064636","C0207683","C1871526"]}
    }
```
## Output
List of recommendations for each drug.
```
{
    "Recommendations": [
        {
            "EffectorLabel": "alcohol",
            "AffectedDrugLabel": "codeine",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "food",
            "AffectedDrugLabel": "omeprazole",
            "Recommendation": "Take",
            "Time": "30-60 minutes before"
        },
        {
            "EffectorLabel": "food",
            "AffectedDrugLabel": "codeine",
            "Recommendation": "Take",
            "Time": null
        },
        {
            "EffectorLabel": "food",
            "AffectedDrugLabel": "lamotrigine",
            "Recommendation": "Take",
            "Time": null
        },
        {
            "EffectorLabel": "ginkgo_biloba",
            "AffectedDrugLabel": "nafamostat",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "garlic",
            "AffectedDrugLabel": "nafamostat",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "bilberry",
            "AffectedDrugLabel": "nafamostat",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "ginger",
            "AffectedDrugLabel": "nafamostat",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "piracetam",
            "AffectedDrugLabel": "nafamostat",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "danshen",
            "AffectedDrugLabel": "nafamostat",
            "Recommendation": "Avoid",
            "Time": null
        },
        {
            "EffectorLabel": "food",
            "AffectedDrugLabel": "raltegravir",
            "Recommendation": "Take",
            "Time": null
        }
    ]
}
```
