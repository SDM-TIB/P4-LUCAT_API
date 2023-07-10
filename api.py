#!/usr/bin/env python3
#
# Description: POST service for exploration of
# data of Lung Cancer in the iASiS KG.
#

import sys
from flask import Flask, abort, request, make_response
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import os
from DDI import Dashboard_DDI
from Rules import Dashboard_Rules
from SS_DDI_Rate import treatment_generation, ddi_rate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LIMIT=10


# KG = os.environ["ENDPOINT"]
KG="https://labs.tib.eu/sdm/p4lucat_kg/sparql"

EMPTY_JSON = "{}"

app = Flask(__name__)


@app.route('/DDI', methods=['POST'])
def run_ddi_api():
    if (not request.json):
        abort(400)
  
    input_list = request.json
    if len(input_list) == 0:
        logger.info("Error in the input format")
        r = "{results: 'Error in the input format'}"
    else:
        response = Dashboard_DDI.run_api(input_list, KG)
        r = json.dumps(response, indent=4)            
    logger.info("Sending the results: ")
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response



@app.route('/rules', methods=['POST'])
def run_rules_api():
    if (not request.json):
        abort(400)
  
    input_list = request.json
    if len(input_list) == 0:
        logger.info("Error in the input format")
        r = "{results: 'Error in the input format'}"
    else:
        main, pos, neg = Dashboard_Rules.run_api(input_list)
        r = {'main': main, 'pos': pos, 'neg': neg}
    logger.info("Sending the results: ")
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response


@app.route('/treatment_DDI_rate', methods=['POST'])
def ddi_wedge():
    if (not request.json):
        abort(400)
    input_list = request.json
    if len(input_list) == 0:
        r = "{results: 'Error in the input format'}"
    else:
        response = ddi_rate.compute_ddi_rate(treatment_generation.compute_treatment(input_list))
        r = json.dumps(response, indent=4)
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response


def main(*args):
    if len(args) == 1:
        myhost = args[0]
    else:
        myhost = "0.0.0.0"
    app.run(debug=False, host=myhost)
    
if __name__ == '__main__':
     main(*sys.argv[1:])
