import mysql.connector
from bs4 import BeautifulSoup
import requests



conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='losandes'
)

def buscar_palabra(palabra_clave):
    url = "https://www.losandes.com.pe/"
    response = requests.get(url)
    # resultados = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_elements = soup.find_all(class_='jeg_post_title')

        for title_element in title_elements:
            link = title_element.find('a')['href']
            title_text = title_element.find('a').text.strip()

            if not palabra_clave or palabra_clave.lower() in title_text.lower():
                contenido_enlace = cargar_contenido(link)
                if contenido_enlace:
                    soup_enlace = BeautifulSoup(contenido_enlace, 'html.parser')
                    elements = soup_enlace.select('.content-inner h3, .content-inner p')
                    contenido = '\n'.join(element.text.strip() for element in elements)
                    entry_header = soup_enlace.find('div', class_='entry-header')
                    if entry_header:
                        h1_element = entry_header.find('h1', class_='jeg_post_title')
                        fecha = entry_header.find('div', class_='jeg_meta_date').find('a').text.strip()
                        if h1_element:
                            titulo_entrada = h1_element.text.strip()
                            insertar_resultado(titulo_entrada, fecha, contenido)
                            # resultados.append({
                            #     "titulo": titulo_entrada,
                            #     "fecha": fecha,
                            #     "contenido": contenido
                            # })
    # return resultados

def cargar_contenido(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
    

def insertar_resultado(titulo, fecha, contenido):
    cursor = conexion.cursor()
    sql = "INSERT INTO noticias (titulo, fecha, contenido) VALUES (%s, %s, %s)"
    valores = (titulo, fecha, contenido)
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        print("Resultado insertado con éxito")
    except Exception as e:
        conexion.rollback()
        print(f"Error al insertar el resultado: {e}")
    finally:
        cursor.close()

palabra_clave = ""
buscar_palabra(palabra_clave)
# resultados = buscar_palabra(palabra_clave)
# print(resultados)

# Cierra la conexión a la base de datos cuando hayas terminado
conexion.close()