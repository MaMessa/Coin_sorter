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
    # On demande un choix explicite pour sélectionner un essai ou le cycle complet.
    parser = argparse.ArgumentParser(description="Essais isolés du trieur de pièces")
    # Cette option sélectionne un appareil seul ou les trois appareils à la suite.
    parser.add_argument("essai", choices=("servo", "moteur1", "moteur2", "cycle"))
    # On lit le choix transmis lors du lancement.
    choix = parser.parse_args().essai
    # Ce cas exécute une fois le test du servo.
    if choix == "servo":
        # Le GPIO du servo est configuré dans config.py.
        essayer_servo(SERVO_GPIO)
    # Ce cas exécute une fois le premier moteur pas à pas.
    elif choix == "moteur1":
        # Le moteur 1 reçoit ses quatre GPIO et son motif réglable.
        essayer_moteur(STEPPER_1_GPIOS, MOTEUR_1_MOUVEMENTS_DEGRES)
    # Ce cas exécute une fois le deuxième moteur pas à pas.
    elif choix == "moteur2":
        # Le moteur 2 doit avoir son propre module ULN2003.
        essayer_moteur(STEPPER_2_GPIOS, MOTEUR_2_MOUVEMENTS_DEGRES)
    # Ce cas recommence les trois mouvements tant que l'utilisateur ne l'arrête pas.
    else:
        # Cette boucle exécute les moteurs l'un après l'autre pour éviter leur démarrage simultané.
        while True:
            # Le servo fait d'abord son mouvement droite-gauche.
            essayer_servo(SERVO_GPIO)
            # Le premier moteur exécute le motif angulaire réglé dans config.py.
            essayer_moteur(STEPPER_1_GPIOS, MOTEUR_1_MOUVEMENTS_DEGRES)
            # Le deuxième moteur effectue son demi-tour réglé dans config.py.
            essayer_moteur(STEPPER_2_GPIOS, MOTEUR_2_MOUVEMENTS_DEGRES)


# Ce garde empêche le programme de démarrer lors d'un import comme module.
if __name__ == "__main__":
    # L'appel lance l'essai choisi en exécution directe.
    main()
