from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

def load_data():
    with open('music_videos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('music_videos.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/datatable')
def datatable():
    videos = load_data()
    return render_template('datatable.html', videos=videos)

# CRUD endpoints
@app.route('/api/v1/spots', methods=['GET'])
def get_all_videos():
    videos = load_data()
    return {
        "status": "OK",
        "message": "Dohvaćeni svi glazbeni spotovi",
        "response": videos
    }, 200

@app.route('/api/v1/spots/<id>', methods=['GET'])
def get_video(id):
    videos = load_data()
    video = next((v for v in videos if v['id'] == id), None)
    if not video:
        return {
            "status": "Not Found",
            "message": f"Video s ID-em {id} nije pronađen",
            "response": None
        }, 404
    return {
        "status": "OK",
        "message": "Video uspješno dohvaćen",
        "response": video
    }, 200

@app.route('/api/v1/spots', methods=['POST'])
def create_video():
    videos = load_data()
    new_video = request.get_json()
    
    # Validate required fields
    required_fields = ["Naslov", "Redatelj", "Label", "Datum", "Trajanje_sekunde", 
                      "Zanr", "pregledi", "komentari", "lajkovi", "izvodaci"]
    
    if not all(field in new_video for field in required_fields):
        return {
            "status": "Bad Request",
            "message": "Nedostaju obavezna polja",
            "response": None
        }, 400
        
    videos.append(new_video)
    save_data(videos)
    return {
        "status": "Created",
        "message": "Novi video uspješno dodan",
        "response": new_video
    }, 201

@app.route('/api/v1/spots/<id>', methods=['PUT'])
def update_video(id):
    videos = load_data()
    video_data = request.get_json()
    video_index = next((index for (index, v) in enumerate(videos) if v['id'] == id), None)
    
    if video_index is None:
        return {
            "status": "Not Found",
            "message": f"Video s ID-em {id} nije pronađen",
            "response": None
        }, 404
        
    videos[video_index].update(video_data)
    save_data(videos)
    return {
        "status": "OK",
        "message": "Video uspješno ažuriran",
        "response": videos[video_index]
    }, 200

@app.route('/api/v1/spots/<id>', methods=['DELETE'])
def delete_video(id):
    videos = load_data()
    video_index = next((index for (index, v) in enumerate(videos) if v['id'] == id), None)
    
    if video_index is None:
        return {
            "status": "Not Found",
            "message": f"Video s ID-em {id} nije pronađen",
            "response": None
        }, 404
        
    deleted_video = videos.pop(video_index)
    save_data(videos)
    return {
        "status": "OK",
        "message": "Video uspješno obrisan",
        "response": deleted_video
    }, 200

# Additional GET endpoints
@app.route('/api/v1/spots/by-genre/<genre>', methods=['GET'])
def get_videos_by_genre(genre):
    videos = load_data()
    filtered_videos = [v for v in videos if genre.lower() in v['Zanr'].lower()]
    return {
        "status": "OK",
        "message": f"Pronađeni spotovi žanra: {genre}",
        "response": filtered_videos
    }, 200

@app.route('/api/v1/spots/by-label/<label>', methods=['GET'])
def get_videos_by_label(label):
    videos = load_data()
    filtered_videos = [v for v in videos if label.lower() in v['Label'].lower()]
    return {
        "status": "OK",
        "message": f"Pronađeni spotovi izdavačke kuće: {label}",
        "response": filtered_videos
    }, 200

@app.route('/api/v1/spots/most-viewed', methods=['GET'])
def get_most_viewed_videos():
    videos = load_data()
    sorted_videos = sorted(videos, key=lambda x: x['pregledi'], reverse=True)
    limit = request.args.get('limit', default=10, type=int)
    return {
        "status": "OK",
        "message": f"Dohvaćeno {limit} najgledanijih spotova",
        "response": sorted_videos[:limit]
    }, 200

@app.route('/api/docs', methods=['GET'])
def get_api_docs():
    with open('openapi.json', 'r', encoding='utf-8') as f:
        spec = json.load(f)
    return {
        "status": "OK",
        "message": "OpenAPI specifikacija uspješno dohvaćena",
        "response": spec
    }, 200

if __name__ == '__main__':
    app.run(debug=True)

