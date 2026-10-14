"""Point d'entrée des essais matériels individuels."""

import argparse

from config import (
    MOTEUR_1_MOUVEMENTS_DEGRES,
    MOTEUR_2_MOUVEMENTS_DEGRES,
    SERVO_GPIO,
    STEPPER_1_GPIOS,
    STEPPER_2_GPIOS,
)
from devices import essayer_moteur, essayer_servo


def main():
    """Lance uniquement le composant demandé en ligne de commande."""
    # On demande un choix explicite pour ne pas démarrer plusieurs moteurs ensemble.
    parser = argparse.ArgumentParser(description="Essais isolés du trieur de pièces")
    # Cette option sélectionne le composant à essayer.
    parser.add_argument("essai", choices=("servo", "moteur1", "moteur2"))
    # On lit le choix transmis lors du lancement.
    choix = parser.parse_args().essai
    # Ce cas lance uniquement le test du servo.
    if choix == "servo":
        # Le GPIO du servo est configuré dans config.py.
        essayer_servo(SERVO_GPIO)
    # Ce cas lance uniquement le premier moteur pas à pas.
    elif choix == "moteur1":
        # Le moteur 1 reçoit ses quatre GPIO et son motif réglable.
        essayer_moteur(STEPPER_1_GPIOS, MOTEUR_1_MOUVEMENTS_DEGRES)
    # Ce cas lance uniquement le deuxième moteur pas à pas.
    else:
        # Le moteur 2 doit avoir son propre module ULN2003.
        essayer_moteur(STEPPER_2_GPIOS, MOTEUR_2_MOUVEMENTS_DEGRES)


# Ce garde empêche le programme de démarrer lors d'un import comme module.
if __name__ == "__main__":
    # L'appel lance l'essai choisi en exécution directe.
    main()
