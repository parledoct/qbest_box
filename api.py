import flask, os
from flask import request, jsonify, Response

from database_helpers import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the QbE-STD API endpoint</h1>"

@app.route('/api/v1/info', methods=['GET'])
def api_info():

    if 'file_id' in request.args:

        file_id   = request.args['file_id']
        file_info = fetch_file_info(file_id)

        resp = jsonify(file_info.to_dict(orient='records')[0])
        resp.status_code = 200

        return resp

    if 'collection_id' in request.args:

        collection_id   = request.args['collection_id']
        collection_info = fetch_collection_info(collection_id)

        resp = jsonify(collection_info)
        resp.status_code = 200

        return resp

@app.route('/api/v1/files', methods=['GET'])
def api_files():

    if 'collection_id' in request.args:

        collection_id = request.args['collection_id']
        file_ids      = list(fetch_file_ids(collection_id))

        return jsonify(
            {
                "collection_id": collection_id,
                "file_ids": file_ids
            }
        )

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

@app.route("/api/v1/upload/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    with open(os.path.join("data/tmp", filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201

app.run()
