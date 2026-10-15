"""Point d'entrée de l'API de tri des pièces."""
from fastapi import FastAPI
from gpiozero import AngularServo

from config import SERVO2_GPIO
from routes.servo import router as servo_router
from routes.moteur import router as moteur_router

# Création du serveur API
app = FastAPI()
app.include_router(servo_router)
app.include_router(moteur_router)

# Initialisation du servo2 (en attente d'intégration).
servo2 = AngularServo(SERVO2_GPIO, min_angle=-90, max_angle=90)


def main():
    pass

# Ce garde empêche le programme de démarrer lors d'un import comme module.
if __name__ == "__main__":
    # L'appel lance l'essai choisi en exécution directe.
    main()
