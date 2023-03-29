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
<<<<<<< HEAD
|  |               Variables               | Values  |            Metrics             |
|:-------:|:----------------------------------------:|:------:|:------------------------------:|
|  |                Gender                 |   Male  | (Head Coverage, [0.026717557]) |
|  |             Smoking habit             |         |    (PCA Confidence, [1.0])     |
|  | Organ affected by the familiar cancer |         |                                |
|  |             Cancer stage              |  IIIA   |                                |
|  |               Histology               |         |                                |
|  |           Molecular markers           |         |                                |
  
=======
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
>>>>>>> updated README.md
