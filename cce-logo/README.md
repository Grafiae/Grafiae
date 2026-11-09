# CCE – Châlons Champagnes Évents : exploration de logo

Cinq pistes graphiques, une présentation PDF et deux maquettes (Facebook, brochure).

## Contenu

| Dossier / fichier | Rôle |
|---|---|
| `CCE_presentation_pistes_logo.pdf` | Série 1 : présentation A4 paysage, 17 pages (brief, références, pistes 01 à 05, comparatif, recommandation, palette, déclinaisons, maquettes) |
| `CCE_presentation_serie2.pdf` | Série 2 : 9 pages (références détaillées, pistes 06 à 10, comparatif, associations possibles) |
| `CCE_5_propositions_logo.png`, `CCE_serie2_5_propositions_logo.png` | Planches d’ensemble de chaque série |
| `svg/` | Logos vectoriels, **texte converti en courbes**. 3 variantes par piste : `couleur`, `negatif` (avec fond vert), `negatif-transparent`, `mono` (noir) |
| `png/` | Mêmes fichiers, fond transparent, 2400 px |
| `mockups/` | `facebook_page.png`, `brochure.png` |
| `tests/` | **40 tests de logos** : les 10 pistes × 4 palettes (9 palettes en tout), SVG avec fond, nommés `pisteNN_nom_palette.svg` |
| `CCE_tests_40_logos.pdf`, `CCE_tests_40_logos_planche.png` | PDF des tests (palettes, une page par piste, vue d’ensemble) et planche des 40 variantes. Aucune maquette |
| `tests3/` | **Série 3, d’après le tableau Pinterest** : 6 pistes (11 à 16) × 5 palettes = 30 variantes SVG |
| `CCE_presentation_serie3_pinterest.pdf`, `CCE_serie3_30_variantes_planche.png` | PDF (lecture du tableau, « inspiré sans copier », une page par piste) et planche des 30 variantes |
| `src/` | Scripts Python/Node qui génèrent tout (pour régénérer après modification) |

## Les 5 pistes

1. **La Plaque** : sceau inspiré des plaques de muselet (+ version simplifiée sans texte pour avatars)
2. **Le Perlage** : monogramme aéré, colonne de bulles dessinées à la main
3. **Le Reflet** : coupe et reflet sur le canal (« Venise pétillante »)
4. **La Signature** : lettrage manuscrit, trait de pinceau doré (+ monogramme manuscrit)
5. **L’Arcade** : trois arches, une lettre par arche (C, C, E). Recommandée comme logo principal

## Série 2 : le nom complet en premier (pistes 06 à 10)

6. **L’Étiquette** : ovale de cuvée à l’ancienne, nom en capitales et italique, ruban CCE
7. **L’Affiche** : nom composé sur trois lignes comme une affiche de la Belle Époque, CCE en signature
8. **Les Flèches** : façade stylisée de Notre-Dame-en-Vaux et son reflet dans le Mau
9. **Le Fizz** : logotype contemporain en minuscules, le « o » de « châlons » devient une bulle
10. **L’Éclat** : coupe d’où jaillissent des rayons terminés en bulles, CCE dans la coupe

Même arborescence : `svg/pisteNN_nom_{couleur,negatif,negatif-transparent,mono}.svg` et `png/`.

## Série 3 : d’après votre tableau Pinterest (pistes 11 à 16)

11. **Le Trait** : coupe d’un seul trait dont le pied devient le filet sous le nom
12. **L’Arche pleine** : arche pleine de Châlons avec coupe, bulles et sigle en réserve
13. **Santé** : deux coupes qui trinquent, éclat de bulles, CCE entre les pieds
14. **Le Cartouche** : cartouche dont la bordure est faite de bulles
15. **La Rosace** : symbole entièrement en bulles + nom en capitales géométriques
16. **Les Gigognes** : C dans C dans E, bulles qui s’échappent

Les images du tableau ne sont pas copiées dans ce dossier. Une recherche d’antériorités (INPI, image inversée) reste à faire avant de choisir.

## Ce qui n’est pas fait, à lire avant d’ouvrir

- **Pas de fichiers `.ai` ni `.indd`.** Le connecteur Adobe était indisponible dans cette session (erreur proxy) : rien n’a été créé dans Illustrator ni InDesign.
  Les SVG s’ouvrent dans Illustrator (Fichier > Ouvrir) avec un groupe `logo`, des tracés vectoriels et un dégradé d’or. Enregistrez-les en `.ai` ensuite.
- **Le PDF n’est pas une mise en page InDesign** : il est fabriqué en HTML puis exporté. Pour le reprendre dans InDesign, placez les SVG comme images liées ; le texte est à ressaisir.
- **C’est une exploration, pas des logos finis.** Les lettres viennent de polices libres (Cormorant Garamond, Jost, Pinyon Script, licence OFL) ; les bulles et le trait de pinceau sont générés par calcul. Le dessin à la main (croquis, scan, tracé dans Illustrator) reste à faire pour les pistes retenues.
- **Les maquettes utilisent des visuels illustrés et des contenus fictifs** (dates, événements). À remplacer par de vraies photographies.
- **Aucune vérification de disponibilité** de la marque (INPI) n’a été faite. L’accent remplacé par une bulle (« Évents ») est un parti pris à tester.
- **Références** : seuls les textes des pages ont pu être consultés, pas leurs images.

## Sources consultées (série 2)

- Mucha et le champagne : https://www.champagneclub.com/?p=53281
- Design d’étiquettes de champagne : https://www.champagneclub.com/?p=52341
- Cappiello, Champagne Delbeck (1902) : https://www.1stdibs.com/fr/meubles/d%C3%A9corations-murales/affiches/affiche-r%C3%A9tro-originale-de-leonetto-cappiello-champagne-delbeck-reims-1902/id-f_34386552
- Madagascar Champagne : https://packagingoftheworld.com/2023/03/champagne-label-design.html
- Notre-Dame-en-Vaux (base Mérimée) : https://monumentum.fr/monument-historique/pa00078618/chalons-en-champagne-eglise-notre-dame-en-vaux-et-son-cloitre
- Les Bulles, French Bubbles, M.G.Heucq : https://worldbranddesign.com/studio-leichtfried-helps-the-renaissance-of-a-champagne-visual-brand-identity
- Marques de champagne modernisées : https://futurebrand.com/our-work/moet-chandon

## Sources consultées (série 1)

- Communiqué de l’office de tourisme sur son nouveau logo (18 mai 2021) : https://www.chalons-tourisme.com/app/uploads/chalons-en-champagne/2021/08/21-05-18-cp-nouveau-logo.pdf
- Muselets personnalisés : https://www.paris-friendly.fr/muselet-champagne-personnalise.html
- Cairn Champagne (Dribbble) : https://dribbble.com/cairnchampagne
- « Les bulles » : https://mindsparklemag.com/design/les-bulles
- Exemples de branding champagne : https://www.designrush.com/agency/branding/trends/champagne-branding-examples
