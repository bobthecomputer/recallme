# RecallMe Demo

Ceci est une démonstration simplifiée de l'application **RecallMe**. L'idée est de montrer comment croiser une liste de rappels produits avec vos achats.

Le script `main.py` récupère la liste des rappels depuis l'API officielle
RappelConso et signale une erreur si la connexion échoue. Vous pouvez
**réactiver** le repli sur un fichier local en appelant
`load_recalls(require_api=False, retries=3)`. Utiliser `retries=None` lance
une boucle infinie d'essais, ce qui peut bloquer l'application si l'accès au
réseau est restreint.

Dans certains environnements, un proxy HTTP peut empêcher l'accès à
l'API. Vous pouvez passer `use_proxy=False` ou définir la variable
`RECALLME_NO_PROXY=1` pour ignorer les variables `HTTP(S)_PROXY`.
La plupart des commandes acceptent également `--no-proxy`.

Les rappels proviennent de l'URL suivante, triée par date de publication la plus
récente. Seuls les vingt derniers résultats sont conservés pour la comparaison :

https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records?limit=20&order_by=date_publication%20desc


## Utilisation

1.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
2.  Lancer le script (optionnellement avec `--no-proxy`) :
    ```bash
    python main.py [--no-proxy]
    ```
    Le programme affiche maintenant les 20 derniers rappels connus avant de
    comparer vos achats avec ces rappels. Il tente automatiquement de récupérer
    les rappels depuis l'API officielle RappelConso et revient aux données
    locales en cas d'échec. En cas d'erreur réseau, un message indique que les
    données locales sont utilisées. Pour exiger absolument les données de
    l'API, passez `require_api=True`. Vous pouvez augmenter le nombre de
    tentatives avec `retries=5` ou plus, mais notez qu'une valeur `None`
    relance la requête indéfiniment et peut bloquer la démo si l'accès à
    l'API est impossible.

3.  Ouvrir l'interface graphique (facultatif) :
    ```bash
    python -m recallme.gui
    ```
    Lancez cette commande depuis le dossier parent qui contient le
    répertoire `recallme`. Si vous êtes déjà dans ce répertoire, exécutez
    simplement :
    ```bash
    python gui.py
    ```

Cette interface utilise Tkinter pour afficher une fenêtre et énumérer les
produits rappelés détectés dans vos achats.

4.  Démarrer l'application web (facultatif) :
    ```bash
    python -m recallme.app [--no-proxy]
    ```
    Comme pour la commande précédente, lancez-la depuis le dossier parent.
    Depuis `recallme`, vous pouvez exécuter directement :
    ```bash
    python app.py [--no-proxy]
    ```
    Vous pouvez également lancer le script depuis n'importe quel dossier en
    indiquant son chemin complet ; il s'adaptera automatiquement.
    Une fois le serveur lancé, ouvrez `http://localhost:5000` dans votre navigateur.
    Par défaut aucune liste d'achats n'est affichée : cliquez sur le bouton
    **Essayer la démo** pour générer un exemple de courses. Les lignes en rouge
    indiquent les produits rappelés. Le site affiche également les 20 derniers
    rappels connus.

    Un bouton "Essayer la démo" permet de générer aléatoirement une liste
    d'achats (20 articles par défaut) à partir du fichier
    `french_top500_products.csv`. Un à trois produits rappelés peuvent y être
    insérés aléatoirement, mais il est également possible qu'aucun rappel ne
    soit présent. Ces rappels proviennent toujours de la liste des 20 plus
    récents retournés par l'API, garantissant ainsi la cohérence avec les
    données affichées. Vous pouvez ajuster le nombre d'articles en passant `n=40`
    ou tout autre chiffre dans l'URL `/demo`.

    Les fichiers `french_top500_products.csv` et `sample_recalls.json` sont
    fournis dans le dépôt. S'ils sont manquants, l'application tentera de les
    télécharger automatiquement depuis GitHub puis utilisera de petits exemples
    intégrés en dernier recours. Ainsi la démo fonctionne immédiatement après
    avoir installé les dépendances.

    Si vous relancez le serveur plusieurs fois, le port 5000 peut rester
    occupé. L'application démarre maintenant sans le reloader afin d'éviter ce
    problème. Au besoin, terminez le processus Python précédent ou modifiez le
    port dans `app.py`.

    Pour personnaliser l'en-tête avec votre logo, placez simplement une image
    nommée `logo.png` dans le dossier `recallme/static/`. L'application la
    chargera automatiquement si elle est présente.

    Cette interface web utilise un petit gabarit HTML et la librairie Bootstrap
    pour offrir un aperçu plus attrayant de vos données.

Vous devriez voir la liste des produits achetés faisant l'objet d'un rappel sanitaire.

## Dépannage

Si l'application reste bloquée en attendant la réponse de l'API, commencez par vérifier la connectivité :

```bash
curl "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records?limit=1&order_by=date_publication%20desc" -H "Accept: application/json"
```

Cette commande doit renvoyer un petit document JSON. Vous pouvez également tester l'appel directement depuis Python :

```bash
python -m recallme.check_api
```

Si vous obtenez une erreur 403 alors que la commande fonctionne en dehors de
votre environnement, il est probable qu'un proxy réseau bloque l'accès.
Vous pouvez réessayer en ignorant les variables `HTTP(S)_PROXY` (avec
`--no-proxy` ou `RECALLME_NO_PROXY=1`) :

```bash
python -m recallme.check_api --no-proxy
```

Si à l'inverse l'appel n'aboutit que lorsque vous passez par votre
proxy d'entreprise, assurez‑vous que les variables d'environnement
`HTTP_PROXY` ou `HTTPS_PROXY` sont correctement renseignées. Vous
pouvez également forcer explicitement leur utilisation :

```bash
python -m recallme.check_api --use-proxy
```
