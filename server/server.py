import database
from flask import Flask, request, jsonify
from bson.objectid import ObjectId

app = Flask(__name__)

db = database.setup()
db_data = db["data"]


@app.route('/artists', methods=["GET"])
def get_artists():
    doc_list = db_data.find()
    json_list = []
    for document in doc_list:
        document['_id'] = str(document['_id'])
        json_list.append(document)

    return jsonify({'data': json_list}), 200

@app.route('/artists/<artist_id>')
def get_artist(artist_id):
    document = db_data.find_one({'_id':ObjectId(artist_id)})
    document['_id'] = str(document['_id'])

    if document is None:
        return jsonify({'error':'no document was found!'}), 404

    return jsonify({'data':document}), 200

if __name__ == "__main__":
    app.run(debug=False)
