"""Commandes simples pour les essais isolés du servo et des deux moteurs."""

import time

from gpiozero import OutputDevice, Servo

from config import (
    DEMI_PAS_PAR_TOUR,
    DELAI_ENTRE_DEMI_PAS,
    PAUSE_ENTRE_MOUVEMENTS,
    SERVO_AMPLITUDE_OSCILLATION,
    SERVO_GAUCHE,
    SERVO_PAUSE,
    SERVO_DROITE,
    SERVO_TEMPS_MOUVEMENT,
)

# Les huit états commandent les bobines en mode demi-pas.
SEQUENCE_DEMI_PAS = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
)


def essayer_servo(gpio):
    """Effectue une fois le mouvement droite-gauche du servo."""
    # Le pilote génère les impulsions de commande adaptées à un servo courant.
    servo = Servo(gpio, min_pulse_width=0.001, max_pulse_width=0.002)
    try:
        # Une valeur positive place le servo du côté droit.
        servo.value = SERVO_DROITE
        # On laisse au servo le temps réglable d'atteindre cette position.
        time.sleep(SERVO_TEMPS_MOUVEMENT)
        # On écarte légèrement le servo autour de la position droite.
        servo.value = SERVO_DROITE - SERVO_AMPLITUDE_OSCILLATION
        # Cette pause permet d'observer le petit mouvement.
        time.sleep(SERVO_PAUSE)
        # Le servo revient près de sa position droite.
        servo.value = SERVO_DROITE + SERVO_AMPLITUDE_OSCILLATION
        # Cette pause rend le deuxième écart visible.
        time.sleep(SERVO_PAUSE)
        # Une valeur négative place le servo du côté gauche.
        servo.value = SERVO_GAUCHE
        # On laisse au servo le temps réglable d'atteindre cette position.
        time.sleep(SERVO_TEMPS_MOUVEMENT)
        # On écarte légèrement le servo autour de la position gauche.
        servo.value = SERVO_GAUCHE + SERVO_AMPLITUDE_OSCILLATION
        # Cette pause permet d'observer le petit mouvement.
        time.sleep(SERVO_PAUSE)
        # Le servo s'écarte dans l'autre sens autour de la gauche.
        servo.value = SERVO_GAUCHE - SERVO_AMPLITUDE_OSCILLATION
        # Cette pause rend le dernier mouvement visible.
        time.sleep(SERVO_PAUSE)
    finally:
        # On libère le servo même lorsque Ctrl+C interrompt la boucle.
        servo.close()


def essayer_moteur(gpios, mouvements_degres, delai_entre_pas=DELAI_ENTRE_DEMI_PAS):
    """Exécute une séquence de rotations signées sur un 28BYJ-48."""
    # Chaque sortie commande une entrée du pilote ULN2003.
    sorties = [OutputDevice(gpio, initial_value=False) for gpio in gpios]
    # Cette variable mémorise l'étape courante de la séquence électrique.
    index_phase = 0
    try:
        # Chaque valeur définit l'angle et le sens d'un mouvement.
        for angle in mouvements_degres:
            # On convertit les degrés en quantité de demi-pas.
            nombre_de_pas = round(abs(angle) * DEMI_PAS_PAR_TOUR / 360.0)
            # Un angle positif avance et un angle négatif recule dans la séquence.
            direction = 1 if angle >= 0 else -1
            # Chaque passage commande une phase du moteur.
            for _ in range(nombre_de_pas):
                # Le modulo garde l'index dans la suite des huit phases.
                index_phase = (index_phase + direction) % len(SEQUENCE_DEMI_PAS)
                # On choisit l'état électrique des quatre entrées.
                phase = SEQUENCE_DEMI_PAS[index_phase]
                # On applique la phase aux quatre sorties du module.
                for sortie, active in zip(sorties, phase):
                    # La sortie suit l'état demandé par cette phase.
                    sortie.value = bool(active)
                # Le délai règle la vitesse et laisse le moteur suivre les pas.
                time.sleep(delai_entre_pas)
            # La pause sépare les mouvements pour les rendre observables.
            time.sleep(PAUSE_ENTRE_MOUVEMENTS)
    finally:
        # Cette boucle coupe et libère les quatre GPIO même si l'essai est interrompu.
        for sortie in sorties:
            # On coupe la bobine pour limiter son échauffement après l'essai.
            sortie.off()
            # On libère la broche afin qu'elle puisse être réutilisée.
            sortie.close()
