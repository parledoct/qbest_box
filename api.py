import flask, sqlite3
from flask import request, jsonify, Response, g

from database_helpers import *
from s3_helpers import *
from audio_helpers import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def home():
    results = query_db('select * from qbestd_results')

    return '<h1>Welcome to the QbE-STD API (Version 1).</h1><a target="_blank" href="https://documenter.getpostman.com/view/15421866/TzJrDf1G">View API Documentation on Postman.</a>'

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
        collection_info = query_db("SELECT * FROM  collection_names WHERE c_id == ?", [collection_id], one=True)

        if(collection_info is None):
            resp = jsonify({"error": "No collection exists with identifier '{}'".format(collection_id)})
        else:
            resp = jsonify(dict(collection_info))

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

    uploaded_files = flask.request.files.getlist("file")

    for f in uploaded_files:
        wav_bytes = f.read()

        # Resample to 16 kHz and convert to mono
        wav_bytes = process_audio(wav_bytes)

        upload_file(
            bucket = 'audio', 
            path   = f.filename, 
            data   = wav_bytes,
            size   = bytes_len(wav_bytes)
        )

    # Return 201 CREATED
    return "", 201

app.run(host='0.0.0.0')
