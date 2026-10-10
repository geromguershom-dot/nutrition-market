# Nutrition & Market

Site vitrine multi-pages pour **Nutrition & Market** (santé, nutrition cellulaire, agriculture — Yaoundé, Cameroun).

HTML / CSS / JavaScript natif, sans framework. Les pages sont générées par un petit script Python (`build.py`) qui partage l'en-tête, le pied de page et les composants entre toutes les pages.

## Pages

Accueil · Boutique (filtre + tri) · Conseils · Formations · Annonces · Blog (3 articles) · Vidéos · À propos · Contact

## Fonctionnalités

- Panier sauvegardé dans le navigateur, **commande envoyée par WhatsApp** (paiement à la livraison)
- Formulaire de contact qui prépare le message dans WhatsApp
- Annonces automatiquement marquées « terminées » après leur date de fin
- Responsive, images WebP, menu mobile, navigation au clavier (Échap ferme le panier)

## Modifier le contenu

Tout le contenu (produits, prix, annonces, formations, articles, vidéos, coordonnées) est en haut de `build.py`.

```bash
python3 build.py     # régénère les pages .html à la racine
npm run dev          # aperçu local (npx serve .)
```

Pour activer une vidéo, renseigner l'identifiant YouTube dans la liste `VIDEOS` de `build.py`.

## Déploiement

Les pages générées sont versionnées : le dépôt se déploie tel quel sur Vercel ou GitHub Pages (aucune étape de build requise).
