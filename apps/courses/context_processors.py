DESCRIPTION = (
    "Buscador de ramos para la Universidad Católica, "
    "ideal para planificar tu horario y encontrar electivos. "
    "Una alternativa a Buscacursos UC."
)

IMG_PATH = "/dist/favicon.ico"


def defaults(_request):
    "Loads the default template variables"
    return {"fallback_description": DESCRIPTION, "fallback_img_path": IMG_PATH}
