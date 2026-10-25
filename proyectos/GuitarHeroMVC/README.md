Guitar Hero MVC

Una implementación profesional de Guitar Hero construida sobre Python 3.10+, la arquitectura de software Modelo-Vista-Controlador (MVC), estructuras de datos lineales desarrolladas desde cero mediante nodos y referencias explícitas en memoria (sin arreglos nativos para representar listas enlazadas) y procesamiento digital de señales de audio (DSP) impulsado por Librosa.

Donde y como se ejecuta este proyecto

Puedes ejecutar el proyecto desde la terminal o línea de comandos de tu sistema operativo (Windows, macOS o Linux) posicionándote en la carpeta raíz del proyecto (GuitarHeroMVC/).

Prerrequisitos

Asegúrate de contar con Python 3.10 o superior instalado y configurado en tus variables de entorno (PATH).

1. Instalación de Dependencias

Abre tu terminal en la raíz del proyecto y ejecuta:

pip install -r requirements.txt


Nota: Las dependencias principales incluyen flet (interfaz gráfica), pygame (reproducción de audio sin latencia), librosa (procesamiento digital de señales DSP), numpy y soundfile.

2. Ejecución de la Aplicación

Para iniciar el juego con la interfaz gráfica Flet:

python main.py


3. Ejecución de la Suite de Pruebas Unitarias

Para verificar la integridad de las Estructuras de Datos (TDAs) y la lógica de negocio sin depender de la interfaz gráfica:

python -m unittest discover tests/


O para ejecutar un módulo específico de pruebas:

python -m unittest tests/test_structures.py


Arquitectura del Sistema (MVC)

El proyecto está diseñado bajo un estricto desacoplamiento de responsabilidades en tres capas fundamentales:

GuitarHeroMVC/
│
├── models/                  # CAPA MODELO (Datos y Estado)
│   ├── structures.py        # TDAs Manuales (Node, DoublyLinkedList, Queue)
│   ├── music_library.py     # Gestor de biblioteca de canciones
│   ├── rhythm_engine.py     # Algoritmos DSP y detección de impactos
│   └── game_engine.py       # Puntuación, rachas y estado de la partida
│
├── views/                   # CAPA VISTA (Interfaz Gráfica)
│   └── desktop_view.py      # Interfaz responsiva en Flet (60 FPS)
│
├── controllers/             # CAPA CONTROLADOR (Lógica de Orquestación)
│   ├── app_controller.py    # Controlador principal y gestión de hilos
│   ├── game_controller.py   # Motor del bucle de juego y colisiones
│   └── audio_controller.py  # Controlador del reproductor Pygame
│
├── tests/                   # SUITE DE PRUEBAS UNITARIAS
│   ├── test_structures.py   # Tests de memoria y punteros en TDAs
│   └── test_gameplay.py     # Tests de colisiones y motor rítmico
│
├── assets/                  # Recursos multimedia (.mp3, imágenes)
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt           # Dependencias del proyecto
|
└── README.md                # Estructura y funcionalidad


Estructuras de Datos Manuales (TDAs Basados en Punteros)

Por requerimiento estricto del laboratorio de Estructura de Datos I, el juego no utiliza arreglos nativos de Python (list) para gestionar las notas musicales ni las colas de eventos. Toda la memoria se gestiona mediante referencias explícitas entre nodos genéricos.