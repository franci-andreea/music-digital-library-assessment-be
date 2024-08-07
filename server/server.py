import database
from flask import Flask, jsonify
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/artists/<artist_id>', methods=["GET"])
def get_artist(artist_id):
    document = db_data.find_one({'_id': ObjectId(artist_id)})
    document['_id'] = str(document['_id'])

    if document is None:
        return jsonify({'error': 'no document was found!'}), 404

    return jsonify({'data':document}), 200

@app.route('/artists/<artist_id>/albums', methods=["GET"])
def get_artist_albums(artist_id):
    document = db_data.find_one({'_id': ObjectId(artist_id)})
    
    if document is None:
        return jsonify({'error': 'no document was found!'}), 404
    
    return jsonify({'data':{'artist_name': document["name"], 'albums': document["albums"]}}), 200

@app.route('/artists/<artist_id>/albums/<album_name>', methods=["GET"])
def get_artist_album(artist_id, album_name):
    document = db_data.find_one({'_id': ObjectId(artist_id)})

    if document is None:
        return jsonify({'error':'no document was found!'}), 404
    
    for album in document["albums"]:
        if album_name == album['title']:
            return jsonify({'data':{'artist_name': document["name"], 'album': album}}), 200

    return jsonify({'error':'this artist does not have an album named like that!'}), 404

@app.route('/albums', methods=["GET"])
def get_albums():
    doc_list = db_data.find()
    albums = []
    for document in doc_list:
        for album in document["albums"]:
            albums.append({'artist_id':str(document['_id']),'artist_name':document["name"], 'album_name':album})

    return jsonify({'data':albums}), 200

@app.route('/suggestions/', methods=["GET"])
def no_suggestions():
    return jsonify({'data':[]}), 200

@app.route('/suggestions/<search_input>', methods=["GET"])
def get_suggestions(search_input):
    doc_list = db_data.find()
    search_input = search_input.lower()
    suggestions = []
    for document in doc_list:
        if search_input in document["name"].lower():
            suggestions.append({'artist_id':str(document['_id']), 'artist_name':document["name"], 'album_name': ''})
        for album in document["albums"]:
            if search_input in album["title"].lower():
                suggestions.append({'artist_id':str(document['_id']), 'artist_name':document["name"], 'album_name': album["title"]})
    
    return jsonify({'data':suggestions}), 200


if __name__ == "__main__":
    app.run(debug=False)
