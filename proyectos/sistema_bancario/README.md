🏦 Sistema de Atención de Tickets Bancarios (Estilo BNB)

Un sistema integral para la gestión y llamadas automatizadas de tickets en ventanilla estilo banco (BNB). Diseñado bajo el patrón de arquitectura Modelo-Vista-Controlador (MVC) e implementando de manera nativa la estructura de datos lineal Lista Simplemente Enlazada (TDA) mediante punteros en memoria.

👨‍💻 Autor y Derechos de Propiedad Intelectual

Autor / Desarrollador: Wilson Leonel Mojica Cuellar

Institución: Universidad Autónoma Gabriel René Moreno (UAGRM)

Ubicación: Santa Cruz de la Sierra, Bolivia

Copyright: © 2026 Wilson Leonel Mojica Cuellar. Todos los derechos reservados.

📌 Características Principales

Estructura de Datos Nativa (TDA): Administración estricta de colas mediante punteros de memoria (cabeza y siguiente) sin utilizar arrays o listas dinámicas nativas para la lógica core.

Anuncio de Voz Sintetizada (TTS): Integración nativa offline con pyttsx3 que deletrea con claridad fluida el ticket y la ventanilla asignada en un hilo de ejecución independiente (threading).

Interfaz Moderna (GUI): UI construida con Tkinter sobre un tema oscuro refinado (Dark Mode).

Gestión por Áreas: Emisión de tickets correlativos categorizados por Atención al Cliente (AC), Cajas (CA) y Plataforma (PL).

Distribución Lista para Producción: Ejecutable autónomo .exe e instalador guiado para entornos Microsoft Windows.

📐 Arquitectura de Software (MVC)

El proyecto está organizado de manera estrictamente modular:

sistema_bancario/
│
├── models/                  # CAPA MODELO (Lógica del TDA)
│   ├── __init__.py
│   ├── nodo_ticket.py       # Estructura del Nodo en Memoria
│   └── lista_tickets.py     # TDA Lista Enlazada y operaciones
│
├── controllers/             # CAPA CONTROLADOR
│   ├── __init__.py
│   └── controlador_banco.py # Coordinador MVC e hilo de audio TTS
│
├── views/                   # CAPA VISTA
│   ├── __init__.py
│   └── vista_banco.py       # Interfaz gráfica con Tkinter
│
├── main.py                  # Punto de entrada principal
├── LICENSE.txt              # Términos de la licencia de funcionamiento
└── setup_script.iss         # Guión de compilación para Inno Setup



🚀 Instalación y Ejecución

Opción 1: Ejecución desde el Código Fuente

Requisitos previos: Tener instalado Python 3.10 o superior.

Clonas o descargas el repositorio en tu equipo.

Instalas las dependencias requeridas:

pip install pyinstaller pyttsx3



Ejecutas el punto de entrada principal:

python main.py



Opción 2: Instalador de Windows (Setup.exe)

Si descargaste el paquete redistribuible:

Ejecuta el archivo Output/Sistema_Bancario_BNB_Setup_v1.0.exe.

Acepta la Licencia de Funcionamiento.

Elige si deseas crear un acceso directo en el Escritorio.

Abre la aplicación desde el Menú Inicio o Escritorio.

🛠️ Compilación y Empaquetado

Para reconstruir el ejecutable .exe e instalador:

Generar Ejecutable Autónomo:

pyinstaller --noconsole --onefile --name "Sistema_Bancario_BNB" main.py



Compilar Instalador de Windows:
Abre setup_script.iss en Inno Setup Compiler y presiona F9.

📄 Licencia

Este software se distribución bajo la Licencia Propietaria de Derechos Reservados / Uso Académico. Consulta el archivo LICENSE.txt para obtener más detalles sobre el uso autorizado y condiciones de titularidad.