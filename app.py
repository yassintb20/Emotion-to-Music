from flask import Flask, render_template, request
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyngrok import ngrok
from neo4j import GraphDatabase

# Configuration de l'API Spotify
client_id = '96a6dc2af02843e99864659e8bb1cfa9'  # Remplacez par ton client_id Spotify
client_secret = '12969d11213f43778dacf9dc85fccbb3'  # Remplacez par ton client_secret Spotify

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Configuration de la base de données Neo4j
uri = "bolt://6.tcp.eu.ngrok.io:19520"  # L'URL de ton instance Neo4j
username = "neo4j"  # Ton nom d'utilisateur
password = "emotionDB"  # Ton mot de passe
driver = GraphDatabase.driver(uri, auth=(username, password))

# Initialisation de Flask
app = Flask(__name__)

# Fonction pour détecter l'émotion à partir de l'URL d'une image
def detect_emotion(image_url):
    try:
        analysis = DeepFace.analyze(image_url, actions=['emotion'], enforce_detection=False)
        if analysis:
            emotion = analysis[0]['dominant_emotion']
            return emotion
        else:
            return None
    except Exception as e:
        print(f"Erreur de DeepFace: {e}")
        return None

# Fonction pour obtenir une playlist Spotify en fonction de l'émotion
def get_spotify_playlist(emotion):
    search_query = emotion.lower()
    results = sp.search(q=search_query, type='playlist', limit=10)

    playlists = []
    for playlist in results['playlists']['items']:
        if playlist:
            playlists.append({
                'name': playlist['name'],
                'url': playlist['external_urls']['spotify'],
                'description': playlist['description'],
                'image': playlist['images'][0]['url'] if playlist['images'] else None
            })

    return playlists

# Fonction pour sauvegarder l'émotion dans la base de données Neo4j
def save_emotion_to_neo4j(image_url, emotion):
    try:
        with driver.session() as session:
            # Vérifier si l'image existe déjà
            query = (
                "MATCH (i:Image {url: $image_url}) "
                "RETURN i"
            )
            result = session.run(query, image_url=image_url)

            # Si l'image existe déjà, récupérer l'émotion et établir la relation
            if result.single():
                # L'image existe déjà, on peut directement ajouter la relation
                query = (
                    "MATCH (i:Image {url: $image_url}), (e:Emotion {name: $emotion}) "
                    "MERGE (i)-[:HAS_EMOTION]->(e)"
                )
                session.run(query, image_url=image_url, emotion=emotion)
                print(f"Relation HAS_EMOTION ajoutée pour l'image existante: {image_url}")
            else:
                # Si l'image n'existe pas, créer un nouveau nœud pour l'image et l'émotion
                query = (
                    "MERGE (i:Image {url: $image_url}) "
                    "MERGE (e:Emotion {name: $emotion}) "
                    "MERGE (i)-[:HAS_EMOTION]->(e)"
                )
                session.run(query, image_url=image_url, emotion=emotion)
                print(f"Emotion '{emotion}' sauvegardée pour l'image: {image_url}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde dans Neo4j: {e}")

# Route principale
@app.route("/", methods=["GET", "POST"])
def home():
    emotion = None
    playlists = []
    error = None
    image_url = None

    if request.method == "POST":
        image_url = request.form.get("image_url")

        # Vérifier si l'URL de l'image est valide
        if not image_url.startswith("http"):
            error = "Veuillez entrer une URL valide."
        else:
            # Détecter l'émotion
            emotion = detect_emotion(image_url)
            if not emotion:
                error = "Impossible de détecter une émotion. Essayez une autre image."
            else:
                # Sauvegarder l'émotion dans Neo4j
                save_emotion_to_neo4j(image_url, emotion)

                # Obtenir la playlist Spotify
                playlists = get_spotify_playlist(emotion)

    return render_template("index.html", emotion=emotion, playlists=playlists, image_url=image_url, error=error)

if __name__ == "__main__":
    # Ouvrir un tunnel ngrok sur le port 5000
    public_url = ngrok.connect(5000)
    print(" * Ngrok tunnel \"{}\" -> \"http://127.0.0.1:5000\"".format(public_url))

    # Démarrer l'application Flask
    app.run(port=5000)
https://ce72-34-86-51-68.ngrok-free.app/