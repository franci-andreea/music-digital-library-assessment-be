import database
from flask import Flask, request, jsonify

app = Flask(__name__)

db = database.setup()
db_data = db["data"]

@app.route('/', methods=["GET"])
def home():
    return jsonify({'data':"hello, world!"}), 200

@app.route('/artists', methods=["GET"])
def get_artists():
    doc_list = db_data.find()
    json_list = []
    for document in doc_list:
        document['_id'] = str(document['_id'])
        json_list.append(document)

    return jsonify({'data': json_list}), 200

if __name__ == "__main__":
    app.run(debug=True)
