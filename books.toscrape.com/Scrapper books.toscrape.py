from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import pandas


def frenar_y_scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def agregar_textos_a_lista(lista_textos, lista_a_exportar):
    for texto in lista_textos:
        lista_a_exportar.append(texto.text)


xpath_titulos_libros = "//article/h3/a"
xpath_precio_libros = "//article/div/p[@class='price_color']"
xpath_texto_paginacion = "//li[@class='current']"
xpath_boton_next = "//li[@class='next']/a"

lista_titulos_exportar = []
lista_precio_exportar = []

servicio = Service("msedgedriver.exe")
driver = webdriver.Edge(service=servicio)

driver.get("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html")
time.sleep(2)

frenar_y_scroll()

paginacion = driver.find_element(By.XPATH, xpath_texto_paginacion)
texto_paginacion = paginacion.text
lista_partes_texto = texto_paginacion.split(" ")
paginas = int(lista_partes_texto[3])

for i in range(paginas-1):
    lista_titulos_html = driver.find_elements(By.XPATH, xpath_titulos_libros)
    lista_precio_html = driver.find_elements(By.XPATH, xpath_precio_libros)

    agregar_textos_a_lista(lista_titulos_html, lista_titulos_exportar)
    agregar_textos_a_lista(lista_precio_html, lista_precio_exportar)

    boton_next = driver.find_element(By.XPATH, xpath_boton_next)
    boton_next.click()
    time.sleep(2)
    
    frenar_y_scroll()


tabla = pandas.DataFrame({
    "Titulos":lista_titulos_exportar,
    "Precios":lista_precio_exportar,
})

tabla.to_excel("scrapper libros.xlsx",index=False)

print("Excel exportado con exito!")

input()
driver.close()