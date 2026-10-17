# Claw Machine de Noël 🎄 : la pince qui pêche un chèque-cadeau

Scène Blender 100 % procédurale : une pince de fête foraine chromée plonge dans une
pile de cadeaux de Noël et en ressort le chèque-cadeau **Le Renard – Hotel & Spa** (recto/verso).
L'esthétique (fond blanc de studio, vitrine en verre et alu, chrome, câble spiralé
noir, fil rouge) reprend les photos de référence.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `claw_machine.py` | Script qui construit toute la scène (modèles, matériaux, physique, lumières, caméra, animation) |
| `claw_machine.blend` | Scène déjà générée, textures incluses (enregistrée avec Blender 5.2) |
| `textures/cheque_recto.png` | Recto du chèque-cadeau (face visible caméra) |
| `textures/cheque_verso.png` | Verso du chèque-cadeau |

## Lancer

**Dans Blender (4.2 ou plus récent)** : onglet *Scripting* > *Open* > `claw_machine.py` > ▶ *Run Script*.
La scène est entièrement reconstruite (le fichier ouvert est réinitialisé).

**En ligne de commande :**

```bash
blender -b -P claw_machine.py          # génère claw_machine.blend à côté du script
blender -b claw_machine.blend -a       # rend l'animation dans ./render/
```

## Contenu de la scène

- **Vitrine** : vitres latérales et avant, cadre en alu brossé, plafond diffusant, fond crème
  chaud en dégradé (halo doré derrière la pile), sol en acrylique brillant.
- **Pince** : corps tourné chromé, 3 griffes en lame d'acier articulées (empties `Claw_Hinge_*`),
  biellettes, fil de levage rouge, câble spiralé noir qui s'étire (contrainte *Stretch To*).
- **Cadeaux** : boîtes emballées (papiers rayés, à pois, arlequin, kraft…) avec rubans et nœuds,
  boules de Noël, bougies en céramique, sucres d'orge. Ils sont posés par simulation
  *rigid body*, puis figés.
- **Chèque-cadeau** : carte cartonnée à coins arrondis (105 × 159 mm), recto et verso imprimés,
  papier couché satiné avec léger grain. Le script lit les images du dossier `textures/`
  (garde-le à côté du script).
- **Ambiance** : deux guirlandes lumineuses chaudes au fond (bokeh), lumière douce de boîte
  à lumière, cartes réfléchissantes invisibles pour les reflets du chrome, AgX contrasté,
  profondeur de champ calée sur le chèque-cadeau.

## Animation (24 i/s, 168 images = 7 s)

| Images | Action |
| --- | --- |
| 1 → 42 | Le chariot amène la pince au-dessus du chèque-cadeau, avec balancement |
| 42 → 52 | Ouverture des griffes |
| 52 → 78 | Descente dans les cadeaux |
| 78 → 92 | Fermeture : la carte est pincée par le haut (contrainte *Child Of* activée image 90) |
| 98 → 140 | Remontée avec le chèque-cadeau, balancement pendulaire |
| 140 → 168 | Tenue finale |

## Réglages rapides (en haut du script)

- `SEED` : autre disposition et répartition des cadeaux
- `N_GIFTS`, `N_BALLS`, `N_JARS`, `N_CANES` : quantité d'objets
- `FAIRY_LIGHTS`, `FRONT_GLASS` : guirlandes et vitre avant
- `BACKDROP_TOP`, `BACKDROP_GLOW` : couleurs du fond (crème chaud en haut, halo doré en bas)
- `SAMPLES`, `RES_X`, `RES_Y`, `USE_GPU` : qualité et format (4:5 par défaut)
- `CARD_XY`, `CARD_SIZE`, `CARD_CORNER` : position, format et arrondi du chèque-cadeau

Pour changer de visuel, remplace simplement `textures/cheque_recto.png` et `cheque_verso.png`
(même format portrait), puis relance le script.
