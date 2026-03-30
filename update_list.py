import subprocess
import os

M3U_FILE = "tvnicaragua.m3u8"
canales_dinamicos = {
    "Canal 13": "x7u200z",
    "Canal 6": "xa1xkxq"
}

def get_live_link(video_id):
    try:
        url = f"https://www.dailymotion.com/video/{video_id}"
        result = subprocess.run(
            ["yt-dlp", "-g", url],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error con ID {video_id}: {e}")
        return None

if os.path.exists(M3U_FILE):
    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nuevas_lineas = []
    for linea in lineas:
        nuevas_lineas.append(linea)
        for nombre, video_id in canales_dinamicos.items():
            if f", {nombre}" in linea or f",{nombre}" in linea:
                link = get_live_link(video_id)
                if link:
                    # Buscamos la siguiente línea para reemplazarla
                    index = lineas.index(linea)
                    if index + 1 < len(lineas):
                        lineas[index + 1] = link + "\n"
    
    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.writelines(lineas)
else:
    print(f"Error: No se encontro el archivo {M3U_FILE}")
    exit(1)
