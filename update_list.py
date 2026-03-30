import subprocess
import os

# Configuración de archivos y canales
M3U_FILE = "tvnicaragua.m3u8"
canales_dinamicos = {
    "Canal 13": "x7u200z",
    "Canal 6": "xa1xkxq"
}

def get_live_link(video_id, nombre_canal):
    try:
        url = f"https://www.dailymotion.com/video/{video_id}"
        # Usamos un User-Agent de Android para evitar bloqueos de Dailymotion
        cmd = [
            "yt-dlp", 
            "--user-agent", "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/114.0 Firefox/114.0",
            "-g", 
            "-f", "best", 
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error extrayendo {nombre_canal} ({video_id}): {e}")
        return None

def actualizar_lista():
    if not os.path.exists(M3U_FILE):
        print(f"Error: No se encontró el archivo {M3U_FILE}")
        return

    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Procesar la lista
    for i in range(len(lineas)):
        linea_actual = lineas[i]
        
        # Revisamos si la línea contiene el nombre de alguno de nuestros canales
        for nombre, video_id in canales_dinamicos.items():
            if f"#EXTINF:-1,{nombre}" in linea_actual.replace(" ", "") or f",{nombre}" in linea_actual:
                print(f"Actualizando {nombre}...")
                nuevo_link = get_live_link(video_id, nombre)
                
                if nuevo_link and (i + 1) < len(lineas):
                    # Reemplazamos la línea siguiente (la URL) con el nuevo link
                    lineas[i + 1] = nuevo_link + "\n"
                    print(f"OK: {nombre} actualizado correctamente.")
                break

    # Guardar los cambios
    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.writelines(lineas)

if __name__ == "__main__":
    actualizar_lista()
