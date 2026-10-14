"""Réglages faciles à adapter après les premiers essais sur le mécanisme."""

# Numéros GPIO en mode BCM, pas les numéros physiques du connecteur.
SERVO_GPIO = 23  # Le signal du servo utilise le GPIO23.
STEPPER_1_GPIOS = (17, 18, 27, 22)  # Ces GPIO pilotent le premier module ULN2003.
STEPPER_2_GPIOS = (5, 6, 13, 19)  # Ces GPIO pilotent le second module ULN2003.

# Positions relatives du servo, de -1 à +1.
SERVO_GAUCHE = -0.5  # Cette valeur place le servo vers le côté gauche.
SERVO_DROITE = 0.5  # Cette valeur place le servo vers le côté droit.
SERVO_AMPLITUDE_OSCILLATION = 0.05  # Cette valeur règle l'écart des petits mouvements.
SERVO_TEMPS_MOUVEMENT = 0.6  # Cette durée laisse le servo atteindre sa position.
SERVO_PAUSE = 0.5  # Cette durée sépare les mouvements du servo.

# Le signe négatif demande le sens inverse ; le motif reste à confirmer.
MOTEUR_1_MOUVEMENTS_DEGRES = (4.0, -2.0)  # Cette séquence reprend le motif fourni, à confirmer.
MOTEUR_2_MOUVEMENTS_DEGRES = (180.0,)  # Cette séquence teste le demi-tour envisagé.

# Valeur nominale approximative en demi-pas pour un tour de sortie du 28BYJ-48.
DEMI_PAS_PAR_TOUR = 4096  # Cette valeur sert de base de conversion degrés-vers-pas.
DELAI_ENTRE_DEMI_PAS = 0.003  # Cette durée règle la vitesse des moteurs.
PAUSE_ENTRE_MOUVEMENTS = 0.5  # Cette durée sépare les rotations successives.
