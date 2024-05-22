
# Solucion del Problema del Enrutamiento de Vehiculos (VRP) con una Interfaz Gráfica de Usuario en Python

## Descripción
Este proyecto proporciona una solución al Problema del Enrutamiento de Vehículos (VRP) utilizando la biblioteca de Google OR-Tools para la optimización combinatoria. Se ha desarrollado una interfaz gráfica de usuario (GUI) en Python usando Tkinter para facilitar la carga de datos desde un archivo CSV y la visualización de los resultados.

## Requisitos
- Python 3.6 o superior
- Las siguientes bibliotecas de Python:
    - tkinter
    - pandas
    - ortools

## Instalación 

1. Clona o descarga el archivo [vrp_proyecto_final_v4.py](https://github.com/DarioRiveraHaro/vrp_proyecto_final/blob/main/vrp_proyecto_final_v4.py) en tu máquina local.
2. Instala las dependencias necesarias ejecutando:
```bash
  pip install pandas ortools
```
## Uso 

1. Ejecuta el script 'vrp_proyecto_final_v4.py':
```bash
  python vrp_proyecto_final_v4.py
```
2. En la interfaz de usuario, haz clic en el botón "Resolver VRP" para cargar un archivo CSV que contenga la matriz de distancias. El archivo CSV debe tener el siguiente formato:
- Cada celda representa la distancia entre dos nodos.
- Las filas y columnas deben estar alineadas correctamente para representar una matriz cuadrada.
3.Una vez cargado el archivo CSV, el algoritmo resolverá el VRP y mostrará los resultados en el área de texto desplazable dentro de la interfaz.

## Estructura del código 
- create_data_model(): Abre un cuadro de diálogo para seleccionar un archivo CSV y carga los datos en una matriz de distancias.
- print_solution(data, manager, routing, solution, output_text): Imprime la solución del VRP, incluyendo la ruta de cada vehículo y la distancia total recorrida.
- solve_vrp(output_text): Resuelve el VRP utilizando Google OR-Tools y muestra los resultados en la GUI.
- main(): Configura la GUI utilizando Tkinter y define la disposición de los widgets.

## Archivos
- vrp_proyecto_final_v4.py: Contiene el código necesario para ejecutar la aplicacion.

## Detalles Técnicos 

1. Carga de datos: Los datos se cargan desde un archivo CSV seleccionado por el usuario. El archivo debe contener una matriz de distancias que será utilizada por el algoritmo de Google OR-Tools.
2. Configuración del modelo: Se utiliza pywrapcp.RoutingModel para configurar el problema de enrutamiento con el número de vehículos, los nodos de inicio y final, y la matriz de distancias.
3. Definición de la función de costo: Se define una función de callback para calcular las distancias entre nodos, que se registra en el modelo de enrutamiento.
4. Solución del problema: Se configura el algoritmo para buscar la solución utilizando una estrategia inicial (PATH_CHEAPEST_ARC) y otros parámetros de búsqueda predeterminados.
5. Visualización de resultados: Los resultados, incluyendo las rutas de los vehículos y las distancias totales, se muestran en el área de texto desplazable de la GUI.

## Ejemplo de Uso
Supongamos que tienes un archivo CSV llamado 'distancias.csv' con el siguiente contenido:
```bash
  0,29,20,21
  29,0,15,17
  20,15,0,28
  21,17,28,0
```
Este archivo representa una matriz de distancias de 4 nodos. Cuando se selecciona este archivo a través de la GUI, el programa resolverá el VRP y mostrará los resultados en la interfaz.

## Notas
- Asegúrate de que el archivo CSV esté correctamente formateado y representa una matriz cuadrada.
- La GUI está diseñada para ser intuitiva y fácil de usar, permitiendo la resolución rápida de problemas de enrutamiento.

## Contacto
Para cualquier consulta o comentario, puedes contactarme en [dario.rivera6182@alumnos.udg.mx].