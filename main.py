import re
import time
from pathlib import Path
from core.router import LocalRouter
from core.registry import SkillRegistry
from skills.obsidian_skill import ObsidianSkill
from skills.system_skill import SystemSkill
from skills.web_skill import WebSkill
from skills.editor_skill import EditorSkill
from skills.voice_skill import VoiceSkill
from skills.feedback_skill import FeedbackSkill
from skills.diagnostico_skill import DiagnosticoSkill
from skills.ml_search_skill import MLSearchSkill

ROOT_DIR = Path(__file__).resolve().parent

def main():
    print("=" * 60)
    print(" 🚀 ASISTENTE AUTÓNOMO FULL-STACK (MODO VOZ FLUIDA ACTIVO) ")
    print("=" * 60)

    router = LocalRouter()
    registry = SkillRegistry()

    obsidian = ObsidianSkill()
    system = SystemSkill()
    web = WebSkill()
    editor = EditorSkill(ROOT_DIR)
    voice = VoiceSkill()
    feedback = FeedbackSkill()
    diagnostico = DiagnosticoSkill()
    ml_search = MLSearchSkill(router.model)

    # Registrar Habilidades
    
    registry.registrar_skill("guardar_memoria", obsidian.guardar_memoria, "Guarda memoria en Obsidian (categoria, titulo, contenido).")
    registry.registrar_skill("buscar_web", web.buscar_web, "Investiga información en la web.")
    registry.registrar_skill("consultar_github", web.consultar_github_repo, "Consulta el README de repositorios públicos de GitHub.")
    registry.registrar_skill("escribir_codigo", editor.crear_o_actualizar_archivo, "Crea o modifica archivos de código.")
    registry.registrar_skill("leer_codigo", editor.leer_archivo, "Lee un archivo de código.")
    registry.registrar_skill("comando_sistema", system.ejecutar_comando, "Ejecuta comandos en la terminal.")
    registry.registrar_skill("git_status", system.estado_git, "Muestra el estado de Git de forma segura.")
    registry.registrar_skill("reproducir_voz", voice.hablar, "Habla con voz sintética local.")
    registry.registrar_skill("registrar_feedback", feedback.registrar_feedback, "Registra un reporte de feedback y autoevaluación (tarea, resultado, areas_mejora).")
    registry.registrar_skill("analizar_error", diagnostico.analizar_excepcion, "Analiza fallos de código y trazas de error.")
    registry.registrar_skill("busqueda_inteligente", ml_search.buscar_semantico, "Realiza una búsqueda semántica avanzada en las notas de Obsidian.")

    memorias_previas = obsidian.leer_memoria_completa()

    prompt_sistema = (
        "Eres un Agente de IA Autónomo Full-Stack con total libertad para debatir, programar y conversar por voz con Wilson.\n"
        "MEMORIA PERSISTENTE DE OBSIDIAN:\n" + memorias_previas[:1500] + "\n\n"
        "HERRAMIENTAS:\n"
        "- BUSQUEDA_INTELIGENTE(consulta)\n"
        "- ANALIZAR_ERROR(tipo_error, mensaje, traza)\n"
        "- REGISTRAR_FEEDBACK(tarea, resultado, areas_mejora)\n"
        "- GUARDAR_MEMORIA(categoria, titulo, contenido)\n"
        "- BUSCAR_WEB(consulta)\n"
        "- CONSULTAR_GITHUB(repo_owner_name)\n"
        "- ESCRIBIR_CODIGO(ruta_relativa, contenido)\n"
        "- LEER_CODIGO(ruta_relativa)\n"
        "- COMANDO_SISTEMA(comando)\n"
        "- GIT_STATUS()\n"
        "- REPRODUCIR_VOZ(texto)\n\n"
        "REGLAS:\n"
        "1. Mantén una charla fluida, analítica y cercana.\n"
        "2. Si defines acuerdos o ideas importantes, guárdalas en Obsidian de forma autónoma.\n"
        "3. Para usar herramientas responde estrictamente en formato: ACCION:NOMBRE(argumentos)\n"
    )
    router.historial.append({"role": "system", "content": prompt_sistema})

    print(f"\n✅ Motor: {router.model}")
    print("✅ Sistema de voz local y memoria en Obsidian listos.")
    print("\nEscribe tu solicitud o háblale al micrófono (escribe 'voz' para entrar en modo conversacional continuo):\n" + "-" * 60)

    # Mensaje inicial hablado por el asistente
    saludo_inicial = "Hola Wilson, estoy listo. ¿Qué vamos a programar hoy o de qué tema charlamos?"
    voice.hablar(saludo_inicial)

    modo_voz_continuo = False

    while True:
        if modo_voz_continuo:
            # Bucle de voz en tiempo real con control de presencia
            entrada_usuario = voice.escuchar_prompt(timeout_segundos=6)
            if not entrada_usuario:
                # El usuario no respondió en el tiempo límite: entra en modo suspensión / presencia
                voice.hablar("¿Estás ahí Wilson? Holaaa... te quedaste en silencio.")
                print("💤 [Entrando en suspensión a la escucha de tu voz...]")
                # Esperar hasta que escuche una nueva frase del usuario
                while True:
                    reintento = voice.escuchar_prompt(timeout_segundos=8)
                    if reintento:
                        voice.hablar("¡Ah, estabas ahí! Qué bueno que volviste. Retomemos lo que teníamos pendiente.")
                        entrada_usuario = reintento
                        break
                    time.sleep(1)
        else:
            entrada_usuario = input("\n👤 Tú (Texto / escribe 'voz' para activar micrófono): ").strip()
            if entrada_usuario.lower() == "voz":
                modo_voz_continuo = True
                print("\n🎙️ [Modo Voz Continua Activado. Habla con el asistente con total libertad]")
                continue

        if not entrada_usuario:
            continue
        if entrada_usuario.lower() in ["salir", "exit", "apagar voz"]:
            voice.hablar("Cerrando sesión. ¡Hasta pronto Wilson!")
            break

        respuesta = router.procesar_mensaje(entrada_usuario)

        if "ACCION:" in respuesta:
            match = re.search(r"ACCION:(\w+)\((.*)\)", respuesta)
            if match:
                accion = match.group(1).lower()
                args_raw = match.group(2).strip()
                args = [a.strip() for a in args_raw.split(",")]

                print(f"\n⚙️ [Enrutador]: Activando '{accion}'...")

                if accion == "guardar_memoria" and len(args) >= 3:
                    res = registry.ejecutar_skill("guardar_memoria", args[0], args[1], ",".join(args[2:]))
                elif accion == "buscar_web":
                    res = registry.ejecutar_skill("buscar_web", args_raw)
                elif accion == "consultar_github":
                    res = registry.ejecutar_skill("consultar_github", args_raw)
                elif accion == "escribir_codigo" and len(args) >= 2:
                    res = registry.ejecutar_skill("escribir_codigo", args[0], ",".join(args[1:]))
                elif accion == "leer_codigo":
                    res = registry.ejecutar_skill("leer_codigo", args_raw)
                elif accion == "comando_sistema":
                    res = registry.ejecutar_skill("comando_sistema", args_raw)
                elif accion == "git_status":
                    res = registry.ejecutar_skill("git_status")
                elif accion == "registrar_feedback" and len(args) >= 3:
                    res = registry.ejecutar_skill("registrar_feedback", args[0], args[1], ",".join(args[2:]))    
                elif accion == "reproducir_voz":
                    res = registry.ejecutar_skill("reproducir_voz", args_raw)
                elif accion == "analizar_error" and len(args) >= 3:
                    res = registry.ejecutar_skill("analizar_error", args[0], args[1], args[2])
                elif accion == "busqueda_inteligente":
                    res = registry.ejecutar_skill("busqueda_inteligente", args_raw)    
                else:
                    res = f"Acción '{accion}' no reconocida."

                print(f"📌 [Resultado]:\n{res}")
                respuesta_final = router.procesar_mensaje(f"Resultado de la herramienta: {res}")
                print(f"\n🤖 Asistente:\n{respuesta_final}")
                voice.hablar(respuesta_final[:250]) # Hablar un resumen de la respuesta
            else:
                print(f"\n🤖 Asistente:\n{respuesta}")
                voice.hablar(respuesta[:250])
        else:
            print(f"\n🤖 Asistente:\n{respuesta}")
            voice.hablar(respuesta[:250])

if __name__ == "__main__":
    main()