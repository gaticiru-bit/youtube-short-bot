import os
from moviepy import ColorClip, TextClip, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def generar_video():
    print("Generando video Short con moviepy...")
    
    duracion = 5
    fondo = ColorClip(size=(1080, 1920), color=(20, 20, 50), duration=duracion)
    
    # Sintaxis actualizada para MoviePy v2.x
    txt_clip = TextClip(
        text="Short Automático\nGitHub Actions", 
        font_size=70, 
        color='white'
    )
    txt_clip = txt_clip.with_position('center').with_duration(duracion)
    
    video = CompositeVideoClip([fondo, txt_clip])
    
    output_file = "short_output.mp4"
    video.write_videofile(output_file, fps=24, codec='libx264', audio=False)
    print("¡Video generado con éxito!")
    return output_file

def subir_a_youtube(video_path):
    print("Conectando con la API de YouTube...")
    
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Faltan credenciales en las variables de entorno (Secrets).")

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": "Short Automático #Shorts",
            "description": "Video generado y subido automáticamente usando Python y GitHub Actions.",
            "tags": ["Shorts", "Automatizacion", "Python"],
            "categoryId": "22" # People & Blogs
        },
        "status": {
            "privacyStatus": "private" # Cambialo a "public" cuando confirmes que anda joya
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

    print("Subiendo video a YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progreso de subida: {int(status.progress() * 100)}%")

    print(f"¡Short subido con éxito! ID del video: {response.get('id')}")

if __name__ == "__main__":
    video_path = generar_video()
    subir_a_youtube(video_path)
