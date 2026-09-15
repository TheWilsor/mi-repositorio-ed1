# Gestor de Tareas con Lista Enlazada (TDA) & Tkinter

Este proyecto es una aplicación de escritorio desarrollada en **Python** para la gestión de tareas. Aplica el concepto de **Tipo de Dato Abstracto (TDA)** mediante una **Lista Enlazada Simple** como estructura de datos dinámica subyacente y utiliza el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** con **Tkinter** para la interfaz gráfica.

---

##  Contexto del Proyecto

### Estructura de Datos (TDA)
- **Nodo**: Contiene los atributos `descripcion` (cadena de texto), `estado` (`'pendiente'` o `'completada'`) y `siguiente` (puntero al nodo contiguo).
- **Lista Enlazada**: Controla la inserción y el recorrido dinámico de nodos.

### Funcionalidades
1. **Agregar Tarea**: Permite añadir elementos al inicio o al final de la lista.
2. **Marcar como Completada**: Modifica el estado de la tarea seleccionada.
3. **Eliminar Tarea**: Desvincula y remueve el nodo de la lista enlazada.
4. **Mostrar Tareas**: Renderiza la lista completa en la interfaz visual.

---

##  Stack Tecnológico & Arquitectura

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** Tkinter (Biblioteca estándar)
- **Estándar de Código:** PEP 8

### Estructura del Proyecto (MVC)
```text
lista_enlazadas_mvc/
│
├── models/
│   ├── __init__.py
│   ├── nodo.py             # Clase Nodo
│   └── lista_enlazada.py   # TDA Lista Enlazada
│
├── controllers/
│   ├── __init__.py
│   └── controlador_tareas.py # Lógica de interacción y manejo de errores
│
├── views/
│   ├── __init__.py
│   └── vista_tareas.py     # Interfaz visual con Tkinter
│
├── main.py                 # Punto de entrada
└── README.md

## RUN Ejecución del Proyecto

Sigue estos pasos para correr la aplicación y probar su funcionalidad:

1. **Abrir la carpeta del proyecto:** Haz clic derecho sobre la carpeta `lista_enlazadas_mvc` en el explorador de VS Code.
2. **Abrir la terminal:** Selecciona la opción **Abrir en terminal integrado** (*Open in Integrated Terminal*).
3. **Verificar ubicación:** La terminal se abrirá posicionándose directamente dentro de la carpeta del proyecto.
4. **Iniciar la aplicación:** Copia y pega el siguiente comando en la terminal y presiona `Enter`:

```bash
python main.py