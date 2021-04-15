import flask
from flask import request, jsonify, Response

from database_helpers import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the QbE-STD API endpoint</h1>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/results', methods=['GET'])
def api_id():

    if 'query_id' in request.args or 'test_id' in request.args:

        results_df = fetch_qbestd_results()

        if 'query_id' in request.args:
            q_id = request.args['query_id']
            keep_rows = results_df["query"] == q_id

        else:
            t_id = request.args['test_id']
            keep_rows = results_df["test"] == t_id

        return_df = results_df[keep_rows]

        return Response(return_df.to_json(orient="records"), mimetype='application/json')

    else:

        return "Error: No id field provided. Please specify a query_id or test_id."

app.run()
