import requests
from bs4 import BeautifulSoup
from datetime import date
from time import sleep
import csv

print('\nEmpezando el scrap...SEA PACIENTE!!!!\n')

#Obtengo el valor del dolar blue
url = "https://www.infobae.com/economia/divisas/dolar-hoy/?gclid=CjwKCAjwzo2mBhAUEiwAf7wjkjACSsty-ixJoqE5qrAcN4jtjvHTugGhT8JcPkyB7B38GhjLoZ-RoxoCQwgQAvD_BwE"
dom_dolar = requests.get(url).text
dom_dolar = BeautifulSoup(dom_dolar, features = 'html.parser')
precio_dolar_blue = dom_dolar.find_all(class_='exchange-dolar-amount')[2].get_text()[1:].replace('.', '')
print("El precio del dólar blue de hoy es: $", precio_dolar_blue)

#URL para scrap de los libros
url = 'https://cuspide.com/100-mas-vendidos/'
response = requests.get(url)
sleep(2)
response.encoding = 'utf-8'
html = response.text

fecha = date.today()
archivo = open('libros.csv', 'w', encoding = 'utf-8', newline='')
archivo_salida = csv.writer(archivo)
archivo_salida.writerow(['título', 'url', 'precio_pesos', 'precio_dolar', 'precio_dolar_blue', 'fecha'])
archivo_errores = open('log_errores.txt', 'w', encoding='utf-8')

#Parsea y obtiene
dom = BeautifulSoup(html, features = 'html.parser')
cien_cuspide = dom.find_all(class_="name product-title woocommerce-loop-product__title")

#Busca libros, links y datos de los 100 libros 
orden = 0
for libro in cien_cuspide:
    titulo = libro.text.title()
    print('\nLibro Nro: ', orden+1)
    print('TITULO DEL LIBRO: ',titulo)
    url = libro.a['href']
    print('URL:  ',url)
    try:
        response_p = requests.get(url)
        sleep(1)
        response_p.encoding = 'utf-8'
        html_precio = response_p.text
        dom_precio = BeautifulSoup(html_precio, features = 'html.parser')
        precio_libro = dom_precio.find(class_="price product-page-price").bdi.text.strip('$').replace('.','').replace(',','.')
        print('PRECIO DEL LIBRO EN PESOS:',precio_libro)
        precio_libro_usd = dom_precio.find('span', style='font-size: 1.3em').text.replace('.','').replace(',','.')
        print('PRECIO DEL LIBRO EN USD:',precio_libro_usd)
        dolar_blue = str(round(float(precio_libro) / float(precio_dolar_blue),2))
        print("PRECIO DEL LIBRO DOLAR BLUE:", dolar_blue)
        archivo_salida.writerow([titulo, url, precio_libro, precio_libro_usd, dolar_blue, fecha])
    except:
        requests.exceptions.HTTPError
        print('Los datos del Libro ',titulo,' no se cargarán por error el sitio web del artículo')
        archivo_errores.write(f'Los datos del Libro {titulo}, no se cargarán por error el sitio web del artículo\nurl: {url}\n')
    orden +=1
    
print('\nTRABAJO FINALIZADO!!!\n')
archivo.close()
archivo_errores.close()