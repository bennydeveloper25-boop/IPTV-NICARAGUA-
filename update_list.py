import subprocess

# Nombre exacto de tu lista
M3U_FILE = "tvnicaragua.m3u8"

# Diccionario con los canales y sus IDs de Dailymotion
canales_dinamicos = {
    "Canal 13": "x7u200z",
    "Canal 6": "xa1xkxq"
}

def get_live_link(video_id):
    try:
        url = f"https://www.dailymotion.com/video/{video_id}"
        # Usamos yt-dlp para extraer el m3u8 real
        result = subprocess.run(
            ["yt-dlp", "-g", url],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except:
        return None

def actualizar_lista():
    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nuevas_lineas = []
    i = 0
    while i < len(lineas):
        linea_actual = lineas[i]
        nuevas_lineas.append(linea_actual)
        
        # Revisamos si la línea es uno de nuestros canales dinámicos
        for nombre, video_id in canales_dinamicos.items():
            if f", {nombre}" in linea_actual or f",{nombre}" in linea_actual:
                nuevo_link = get_live_link(video_id)
                if nuevo_link:
                    nuevas_lineas.append(nuevo_link + "\n")
                    i += 1 # Saltamos el link viejo que estaba en la lista
                break
        i += 1

    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

actualizar_lista()
