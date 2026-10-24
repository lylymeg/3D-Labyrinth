# 🕹️ Moteur Raycasting Pseudo-3D (Rétro FPS - Pygame)

Un moteur de rendu 3D rétro inspiré des pionniers du genre (comme *Wolfenstein 3D*) développé de zéro en **Python** avec **Pygame**, sans aucun asset externe.

---

## 📸 Fonctionnalités

- 👁️ **Projection 3D en temps réel :** Simulation d'un environnement en relief calculée mathématiquement à partir d'une grille 2D.
- 📐 **Correction de l'effet Fish-eye :** Ajustement trigonométrique pour stabiliser la perspective géométrique.
- 🗺️ **Mini-map interactive :** Affichage simultané de la position du joueur vue du dessus dans un coin de l'écran.
- 🔦 **Effet d'ombrage par distance :** Les murs s'assombrissent subtilement en fonction de leur éloignement pour renforcer l'immersion.

---

## 🚀 Lancement

```bash
pip install pygame
python main.py