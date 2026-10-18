# Claw Machine Le Renard 🎄 : la pince qui pêche un chèque-cadeau

Scène Blender 100 % procédurale. Une borne d'arcade vert bouteille est posée dans l'encadrement
d'une grande porte double d'hôtel, sur un tapis rouge, comme sur la photo de référence. La caméra part d'un plan large et zoome vers la pince, qui plonge dans une pile
de cadeaux de Noël et en ressort le chèque-cadeau **Le Renard – Hotel & Spa** (recto/verso).

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `claw_machine.py` | Script qui construit toute la scène (modèles, matériaux, physique, lumières, caméra, animation) |
| `claw_machine.blend` | Scène déjà générée, textures incluses (enregistrée avec Blender 5.2) |
| `textures/pbr/`, `textures/hdri/` | Emplacements pour les textures photo et l'HDRI (voir plus bas) |
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
- **Entrée d'hôtel** : façade en noyer sombre (pilastres, chambranle, imposte vitrée), porte double
  blanche moulurée ouverte (béquilles chromées, charnières laiton, bras de retenue), seuil surélevé,
  tapis rouge épais qui épouse la marche, sol du hall en pierre, pièce sombre derrière la borne.
- **Lumière** : soleil rasant à ombres nettes (un auvent invisible ne laisse passer qu'une
  diagonale de soleil sur le bas du tapis et le battant droit), caisson lumineux de la borne,
  néons, faible lumière du hall ; AgX contrasté, profondeur de champ calée sur la carte.
- **Réalisme** : peau d'orange et rugosité variable sur la laque, traces sur le verre et le chrome,
  bois veiné, fibres du tapis, papier cadeau froissé, halo (bloom) sur les néons au compositing.

## Animation (24 i/s, 192 images = 8 s)

| Images | Action |
| --- | --- |
| 1 → 150 | Zoom caméra : plan large sur l'entrée (portes, tapis) → plan serré sur la pince |
| 1 → 48 | Le chariot amène la pince au-dessus du chèque-cadeau, avec balancement |
| 48 → 58 | Ouverture des griffes |
| 58 → 86 | Descente dans les cadeaux |
| 86 → 100 | Fermeture : la carte est pincée par le haut (contrainte *Child Of* activée image 98) |
| 106 → 150 | Remontée avec le chèque-cadeau, balancement pendulaire |
| 150 → 192 | Tenue finale en plan serré |

## Rendu photoréaliste : textures photo + HDRI

Sans rien télécharger, la scène utilise des matériaux 100 % procéduraux. Pour un rendu qui
ressemble vraiment à une photo, ajoute de vraies textures photo et une HDRI depuis
[polyhaven.com](https://polyhaven.com) (gratuit, licence CC0) :

| Dossier | Contenu | Recherche conseillée sur Poly Haven |
| --- | --- | --- |
| `textures/pbr/carpet/` | tapis rouge | « carpet », « fabric », « velvet », « wool » |
| `textures/pbr/facade/` | façade sombre | « wood » (bois foncé, planches, lambris) |
| `textures/pbr/door/` | portes blanches | « painted wood », « plaster » |
| `textures/pbr/lobby_floor/` | sol du hall | « concrete », « stone floor », « marble tiles » |
| `textures/pbr/interior_floor/` | sol de la pièce | « wood floor », « parquet » |
| `textures/hdri/` | environnement | une HDRI d'intérieur (.hdr / .exr) |

1. Pour chaque texture, télécharge la version **2K** (JPG ou PNG) avec au moins les cartes
   *Diffuse*, *Rough*, *nor_gl* et *Displacement*, et dépose les images dans le dossier.
2. Relance `claw_machine.py` : la console affiche « Textures photo utilisées pour … ».
3. Les réglages sont en haut de la section « TEXTURES PHOTO » du script : `PBR_SLOTS`
   (taille d'une répétition en mètres, teinte, relief) et `HDRI_STRENGTH`, `HDRI_ROTATION`.
   Si ta texture de tapis n'est pas rouge, mets par exemple `(0.8, 0.08, 0.08)` comme teinte.

Pour le rendu final, monte `SAMPLES` à 512 et rends sur carte graphique (`USE_GPU`).

## Réglages rapides (en haut du script)

- `MACHINE_GREEN`, `NEON_COLOR`, `NEON_STRENGTH` : couleur de la laque et des néons
- `MARQUEE_TEXT` : texte de l'enseigne
- `OPEN_W`, `OPEN_H`, `DOOR_OPEN`, `STEP_H` (section entrée) : ouverture, angle des battants, hauteur du seuil
- `CAM_WIDE`, `CAM_CLOSE` (section caméra) : départ et arrivée du zoom (position, cible, focale)
- `SEED` : autre disposition et répartition des cadeaux
- `N_GIFTS`, `N_BALLS`, `N_JARS`, `N_CANES` : quantité d'objets
- `FAIRY_LIGHTS`, `FRONT_GLASS` : guirlandes et vitre avant
- `SAMPLES`, `RES_X`, `RES_Y`, `USE_GPU` : qualité et format (3:4 par défaut)
- `CARD_XY`, `CARD_SIZE`, `CARD_CORNER` : position, format et arrondi du chèque-cadeau

Pour changer de visuel, remplace simplement `textures/cheque_recto.png` et `cheque_verso.png`
(même format portrait), puis relance le script.
