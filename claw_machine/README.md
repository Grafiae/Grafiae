# Claw Machine Le Renard 🎄 : la pince qui pêche un chèque-cadeau

Scène Blender 100 % procédurale. Une borne d'arcade vert bouteille trône dans un salon
d'hôtel. La caméra part d'un plan large et zoome vers la pince, qui plonge dans une pile
de cadeaux de Noël et en ressort le chèque-cadeau **Le Renard – Hotel & Spa** (recto/verso).

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `claw_machine.py` | Script qui construit toute la scène (modèles, matériaux, physique, lumières, caméra, animation) |
| `claw_machine.blend` | Scène déjà générée, textures incluses (enregistrée avec Blender 5.2) |
| `textures/cheque_recto.png` | Recto du chèque-cadeau (face visible caméra) |
| `textures/cheque_verso.png` | Verso du chèque-cadeau |
| `preview/` | Rendus d'aperçu (plan large, plan serré, GIF basse résolution) |

## Lancer

**Dans Blender (4.2 ou plus récent)** : onglet *Scripting* > *Open* > `claw_machine.py` > ▶ *Run Script*.
La scène est entièrement reconstruite (le fichier ouvert est réinitialisé).

**En ligne de commande :**

```bash
blender -b -P claw_machine.py          # génère claw_machine.blend à côté du script
blender -b claw_machine.blend -a       # rend l'animation dans ./render/
```

## Contenu de la scène

- **Borne d'arcade** : laque vert bouteille, néons verts sur les arêtes avant, fronton avec
  l'enseigne lumineuse « LE RENARD », caisson lumineux au plafond de la vitrine, fond intérieur
  vert, rebord crème, pupitre avec joystick à boule rouge, bouton et monnayeur chromé, portes
  moulurées à serrures, socle et roulettes.
- **Pince** : corps tourné chromé, 3 griffes en lame d'acier articulées (empties `Claw_Hinge_*`),
  fil de levage rouge, câble spiralé noir qui s'étire (contrainte *Stretch To*), chariot et
  traverse qui suivent la pince sous le plafond.
- **Cadeaux** : boîtes emballées (papiers rayés, à pois, arlequin, kraft…) avec rubans et nœuds,
  boules de Noël, bougies en céramique, sucres d'orge, guirlandes lumineuses au fond de la
  vitrine. Ils sont posés par simulation *rigid body*, puis figés.
- **Chèque-cadeau** : carte cartonnée à coins arrondis (105 × 159 mm), recto et verso imprimés.
  Le script lit les images du dossier `textures/` (garde-le à côté du script).
- **Salon d'hôtel** : parquet en chêne, murs à boiseries moulurées (plinthe, cimaise, corniche),
  deux appliques en laiton à abat-jour, tapis de velours rouge.
- **Lumière** : caisson lumineux de la borne, lumière de fenêtre douce, tache de soleil chaude
  sur le tapis, appliques, néons ; AgX contrasté, profondeur de champ calée sur la carte.

## Animation (24 i/s, 192 images = 8 s)

| Images | Action |
| --- | --- |
| 1 → 150 | Zoom caméra : plan large de la borne dans la pièce → plan serré sur la pince |
| 1 → 48 | Le chariot amène la pince au-dessus du chèque-cadeau, avec balancement |
| 48 → 58 | Ouverture des griffes |
| 58 → 86 | Descente dans les cadeaux |
| 86 → 100 | Fermeture : la carte est pincée par le haut (contrainte *Child Of* activée image 98) |
| 106 → 150 | Remontée avec le chèque-cadeau, balancement pendulaire |
| 150 → 192 | Tenue finale en plan serré |

## Réglages rapides (en haut du script)

- `MACHINE_GREEN`, `NEON_COLOR`, `NEON_STRENGTH` : couleur de la laque et des néons
- `MARQUEE_TEXT` : texte de l'enseigne
- `CAM_WIDE`, `CAM_CLOSE` (section caméra) : départ et arrivée du zoom (position, cible, focale)
- `SEED` : autre disposition et répartition des cadeaux
- `N_GIFTS`, `N_BALLS`, `N_JARS`, `N_CANES` : quantité d'objets
- `FAIRY_LIGHTS`, `FRONT_GLASS` : guirlandes et vitre avant
- `SAMPLES`, `RES_X`, `RES_Y`, `USE_GPU` : qualité et format (4:5 par défaut)
- `CARD_XY`, `CARD_SIZE`, `CARD_CORNER` : position, format et arrondi du chèque-cadeau

Pour changer de visuel, remplace simplement `textures/cheque_recto.png` et `cheque_verso.png`
(même format portrait), puis relance le script.
