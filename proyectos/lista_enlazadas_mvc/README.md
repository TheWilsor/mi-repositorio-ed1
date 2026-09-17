# Gestor de Tareas con Lista Enlazada Simple (TDA) & Tkinter

Este proyecto es una aplicación de escritorio desarrollada en **Python** para la gestión dinámica de tareas. Aplica el concepto de **Tipo de Dato Abstracto (TDA)** mediante una **Lista Enlazada Simple** como estructura de datos subyacente y utiliza el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** con **Tkinter** para organizar la interfaz gráfica en 3 paneles clasificados.

---

## 📌 Contexto & Lógica del Proyecto

### Estructura de Datos (TDA)
- **Nodo**: Contiene los atributos `descripcion` (cadena de texto), `estado` (`'pendiente'` o `'completada'`) y `siguiente` (puntero de enlace al nodo contiguo).
- **Lista Enlazada**: Controla la inserción secuencial buscando el primer puntero libre y gestiona la desvinculación/reconexión directa de punteros al eliminar.

### Funcionalidades
1. **Agregar Tarea (Inserción por Punteros)**: Consulta si la cabeza está libre; si no, recorre la cadena hasta encontrar el último puntero libre (`siguiente is None`) e inserta el nuevo nodo al final.
2. **Marcar como Completada**: Modifica el atributo `estado` del nodo recorrido en memoria y actualiza la visualización.
3. **Eliminar Tarea (Desvinculación)**: Recorre secuencialmente la lista y reconecta los punteros del nodo anterior directamente con el nodo posterior, dejando el nodo seleccionado desconectado de la lista.
4. **Visualización Clasificada en 3 Paneles**: Recorre la lista enlazada unificada y despliega la información numerada automáticamente en tres secciones independientes:
   - **1. Todas las Tareas** (Muestra el estado `[ ]` o `[✓]`)
   - **2. Pendientes**
   - **3. Completadas**

---

## 🛠️ Stack Tecnológico & Arquitectura

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** Tkinter (Biblioteca estándar)
- **Estándar de Código:** PEP 8

### Estructura del Proyecto (MVC)
```text
lista_enlazadas_mvc/
│
├── models/
│   ├── __init__.py
│   ├── nodo.py             # Clase Nodo
│   └── lista_enlazada.py   # TDA Lista Enlazada
│
├── controllers/
│   ├── __init__.py
│   └── controlador_tareas.py # Lógica de interacción y manejo de errores
│
├── views/
│   ├── __init__.py
│   └── vista_tareas.py     # Interfaz visual con Tkinter
│
├── main.py                 # Punto de entrada
└── README.md

## RUN Ejecución del Proyecto

Sigue estos pasos para correr la aplicación y probar su funcionalidad:

1. **Abrir la carpeta del proyecto:** Haz clic derecho sobre la carpeta `lista_enlazadas_mvc` en el explorador de VS Code.
2. **Abrir la terminal:** Selecciona la opción **Abrir en terminal integrado** (*Open in Integrated Terminal*).
3. **Verificar ubicación:** La terminal se abrirá posicionándose directamente dentro de la carpeta del proyecto.
4. **Iniciar la aplicación:** Copia y pega el siguiente comando en la terminal y presiona `Enter`:

```bash
python main.py