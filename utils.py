import random

PHRASES = [
    "¡Ánimo! Todo va a mejorar.",
    "No te rindas, cada día es una nueva oportunidad.",
    "Eres capaz de lograr lo que te propones."
]

COMPLETION_PHRASES = [
    "¡Bien hecho! Cada hábito te acerca a tus metas.",
    "¡Sigue así, estás haciendo un gran trabajo!",
    "¡Increíble! Otro hábito completado con éxito.",
    "¡Felicidades! Estás construyendo una versión mejorada de ti mismo.",
    "¡Eres imparable! Mantén el ritmo."
]

NEGATIVE_PHRASES = [
    "Recuerda, cada día trae nuevas oportunidades.",
    "No te rindas, eres más fuerte de lo que crees.",
    "Incluso las tormentas más fuertes terminan. ¡Tú también lo lograrás!",
    "Respira profundo, todo mejorará pronto.",
    "Eres valioso y mereces ser feliz. ¡Sigue adelante!"
]


def get_random_motivation():
    return random.choice(PHRASES)

def get_random_completion_phrase():
    return random.choice(COMPLETION_PHRASES)
