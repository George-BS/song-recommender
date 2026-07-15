from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sqlite3


app = FastAPI()


# Gets the directory where the script is located
root_dir = Path(__file__).resolve().parent.parent
print(root_dir)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow every origin (development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection():
    conn=sqlite3.connect(f"{root_dir}/database/song_recommendations_db.db")
    conn.row_factory = sqlite3.Row
    return conn



@app.get("/songs")
def all_songs():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM songs limit 50")
    songs= []

    song_objects = cursor.fetchall()
    conn.close()

    for s in song_objects:
        songs.append(dict(s))

    return songs

