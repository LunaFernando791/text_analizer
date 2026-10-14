import logging

from django.shortcuts import render

from .services import analyze_text

logger = logging.getLogger(__name__)


def home(request):
    resultado = None
    texto_entrada = ""
    estado = ""

    if request.method == "POST":
        texto_entrada = request.POST.get("texto", "").strip()

        if not texto_entrada:
            resultado = "Por favor, introduce algo."
            estado = "error"
        else:
            try:
                resultado = analyze_text(texto_entrada)
                estado = "ok"
            except Exception:
                logger.exception("No se pudo analizar el texto enviado.")
                resultado = (
                    "No se pudo analizar el texto. Revisa la configuración del modelo "
                    "y la consola para ver más detalles."
                )
                estado = "error"

    return render(
        request,
        "moderation/home.html",
        {
            "resultado": resultado,
            "texto_entrada": texto_entrada,
            "estado": estado,
        },
    )
