# Claw Machine de Noël 🎄 : la pince qui pêche une enveloppe

Scène Blender 100 % procédurale : une pince de fête foraine chromée plonge dans une
pile de cadeaux de Noël et en ressort une enveloppe en papier scellée à la cire.
L'esthétique (fond blanc de studio, vitrine en verre et alu, chrome, câble spiralé
noir, fil rouge) reprend les photos de référence.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `claw_machine.py` | Script qui construit toute la scène (modèles, matériaux, physique, lumières, caméra, animation) |
| `claw_machine.blend` | Scène déjà générée (enregistrée avec Blender 5.2) |

## Lancer

**Dans Blender (4.2 ou plus récent)** : onglet *Scripting* > *Open* > `claw_machine.py` > ▶ *Run Script*.
La scène est entièrement reconstruite (le fichier ouvert est réinitialisé).

**En ligne de commande :**

```bash
blender -b -P claw_machine.py          # génère claw_machine.blend à côté du script
blender -b claw_machine.blend -a       # rend l'animation dans ./render/
```

## Contenu de la scène

- **Vitrine** : vitres latérales et avant, cadre en alu brossé, plafond diffusant, fond blanc
  légèrement émissif (effet studio), sol en acrylique brillant.
- **Pince** : corps tourné chromé, 3 griffes en lame d'acier articulées (empties `Claw_Hinge_*`),
  biellettes, fil de levage rouge, câble spiralé noir qui s'étire (contrainte *Stretch To*).
- **Cadeaux** : boîtes emballées (papiers rayés, à pois, arlequin, kraft…) avec rubans et nœuds,
  boules de Noël, bougies en céramique, sucres d'orge. Ils sont posés par simulation
  *rigid body*, puis figés.
- **Enveloppe** : papier crème avec grain, rabat, plis, cachet de cire rouge irrégulier.
- **Ambiance** : deux guirlandes lumineuses chaudes au fond (bokeh), lumière douce de boîte
  à lumière, cartes réfléchissantes invisibles pour les reflets du chrome, AgX contrasté,
  profondeur de champ calée sur l'enveloppe.

## Animation (24 i/s, 168 images = 7 s)

| Images | Action |
| --- | --- |
| 1 → 42 | Le chariot amène la pince au-dessus de l'enveloppe, avec balancement |
| 42 → 52 | Ouverture des griffes |
| 52 → 78 | Descente dans les cadeaux |
| 78 → 92 | Fermeture : l'enveloppe est pincée (contrainte *Child Of* activée image 90) |
| 98 → 140 | Remontée avec l'enveloppe, balancement pendulaire |
| 140 → 168 | Tenue finale |

## Réglages rapides (en haut du script)

- `SEED` : autre disposition et répartition des cadeaux
- `N_GIFTS`, `N_BALLS`, `N_JARS`, `N_CANES` : quantité d'objets
- `FAIRY_LIGHTS`, `FRONT_GLASS` : guirlandes et vitre avant
- `SAMPLES`, `RES_X`, `RES_Y`, `USE_GPU` : qualité et format (4:5 par défaut)
- `ENV_XY`, `ENV_SIZE` : position et format de l'enveloppe

Astuce : pour personnaliser l'enveloppe (logo, texte), remplace le matériau
`EnvelopePaper` par une texture image, ou ajoute un objet texte enfant de `Envelope`.
