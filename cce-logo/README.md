# CCE – Châlons Champagnes Évents : exploration de logo

Cinq pistes graphiques, une présentation PDF et deux maquettes (Facebook, brochure).

## Contenu

| Dossier / fichier | Rôle |
|---|---|
| `CCE_presentation_pistes_logo.pdf` | Présentation A4 paysage, 17 pages : brief, références, 5 pistes, comparatif, recommandation, palette, déclinaisons, maquettes |
| `svg/` | Logos vectoriels, **texte converti en courbes**. 3 variantes par piste : `couleur`, `negatif` (avec fond vert), `negatif-transparent`, `mono` (noir) |
| `png/` | Mêmes fichiers, fond transparent, 2400 px |
| `mockups/` | `facebook_page.png`, `brochure.png` |
| `src/` | Scripts Python/Node qui génèrent tout (pour régénérer après modification) |

## Les 5 pistes

1. **La Plaque** : sceau inspiré des plaques de muselet (+ version simplifiée sans texte pour avatars)
2. **Le Perlage** : monogramme aéré, colonne de bulles dessinées à la main
3. **Le Reflet** : coupe et reflet sur le canal (« Venise pétillante »)
4. **La Signature** : lettrage manuscrit, trait de pinceau doré (+ monogramme manuscrit)
5. **L’Arcade** : trois arches, une lettre par arche (C, C, E). Recommandée comme logo principal

## Ce qui n’est pas fait, à lire avant d’ouvrir

- **Pas de fichiers `.ai` ni `.indd`.** Le connecteur Adobe était indisponible dans cette session (erreur proxy) : rien n’a été créé dans Illustrator ni InDesign.
  Les SVG s’ouvrent dans Illustrator (Fichier > Ouvrir) avec un groupe `logo`, des tracés vectoriels et un dégradé d’or. Enregistrez-les en `.ai` ensuite.
- **Le PDF n’est pas une mise en page InDesign** : il est fabriqué en HTML puis exporté. Pour le reprendre dans InDesign, placez les SVG comme images liées ; le texte est à ressaisir.
- **C’est une exploration, pas des logos finis.** Les lettres viennent de polices libres (Cormorant Garamond, Jost, Pinyon Script, licence OFL) ; les bulles et le trait de pinceau sont générés par calcul. Le dessin à la main (croquis, scan, tracé dans Illustrator) reste à faire pour les pistes retenues.
- **Les maquettes utilisent des visuels illustrés et des contenus fictifs** (dates, événements). À remplacer par de vraies photographies.
- **Aucune vérification de disponibilité** de la marque (INPI) n’a été faite. L’accent remplacé par une bulle (« Évents ») est un parti pris à tester.
- **Références** : seuls les textes des pages ont pu être consultés, pas leurs images.

## Sources consultées

- Communiqué de l’office de tourisme sur son nouveau logo (18 mai 2021) : https://www.chalons-tourisme.com/app/uploads/chalons-en-champagne/2021/08/21-05-18-cp-nouveau-logo.pdf
- Muselets personnalisés : https://www.paris-friendly.fr/muselet-champagne-personnalise.html
- Cairn Champagne (Dribbble) : https://dribbble.com/cairnchampagne
- « Les bulles » : https://mindsparklemag.com/design/les-bulles
- Exemples de branding champagne : https://www.designrush.com/agency/branding/trends/champagne-branding-examples
