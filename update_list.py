import requests
import re
import os

M3U_FILE = "tvnicaragua.m3u8"

# Las webs oficiales que tienen el reproductor incrustado
canales_web = {
    "Canal 6": "https://canal6.com.ni/en-vivo/",
    "Canal 13": "https://www.vivanicaragua.com.ni/vivanicaragua13-en-vivo/"
}

def extraer_id_real(url_pagina):
    try:
        # Simulamos un navegador para que la web no nos bloquee
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url_pagina, headers=headers, timeout=15)
        
        # Buscamos el patrón video=XXXXXX que viste en el HTML
        match = re.search(r'video=([a-zA-Z0-9]+)', response.text)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error al conectar con la web: {e}")
        return None

def actualizar_lista():
    if not os.path.exists(M3U_FILE):
        print(f"No se encontro el archivo {M3U_FILE}")
        return

    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    hubo_cambios = False
    for i in range(len(lineas)):
        linea = lineas[i]
        
        for nombre, url_web in canales_web.items():
            if f"EXTINF:-1,{nombre}" in linea or f",{nombre}" in linea:
                print(f"Verificando {nombre}...")
                id_actualizado = extraer_id_real(url_web)
                
                if id_actualizado:
                    nuevo_link = f"https://geo.dailymotion.com/player.html?video={id_actualizado}"
                    
                    # Solo actualizamos si el link en el archivo es diferente al que encontramos
                    if (i + 1) < len(lineas) and lineas[i+1].strip() != nuevo_link:
                        lineas[i + 1] = nuevo_link + "\n"
                        hubo_cambios = True
                        print(f"-> Nuevo ID detectado para {nombre}: {id_actualizado}")
                    else:
                        print(f"-> {nombre} ya tiene el ID mas reciente.")
                break

    if hubo_cambios:
        with open(M3U_FILE, "w", encoding="utf-8") as f:
            f.writelines(lineas)
        print("Archivo M3U actualizado con los IDs de la web oficial.")
    else:
        print("No fue necesario actualizar nada.")

if __name__ == "__main__":
    actualizar_lista()
