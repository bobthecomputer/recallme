# RecallMe Demo

Ceci est une démonstration simplifiée de l'application **RecallMe**. L'idée est de montrer comment croiser une liste de rappels produits avec vos achats.

Le script `main.py` récupère la liste des rappels depuis l'API officielle
RappelConso (avec repli sur un fichier local en cas d'échec de connexion) puis
charge vos achats depuis `purchases.csv` afin d'afficher les produits
concernés. Les rappels proviennent de l'URL suivante :

https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records?limit=20


## Utilisation

1.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
2.  Lancer le script :
    ```bash
    python main.py
    ```
    Le programme affiche maintenant les 20 derniers rappels connus avant de
    comparer vos achats avec ces rappels. Il tente automatiquement de récupérer
    les rappels depuis l'API officielle RappelConso et revient aux données
    locales en cas d'échec. En cas d'erreur réseau, un message indique que les
    données locales sont utilisées.

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

4.  Démarrer l'application web (facultatif) :
    ```bash
    python -m recallme.app
    ```
    Comme pour la commande précédente, lancez-la depuis le dossier parent.
    Depuis `recallme`, vous pouvez exécuter directement :
    ```bash
    python app.py
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
    `french_top500_products.csv`. Cette liste inclut entre 0 et 3 produits
    rappelés pour visualiser le fonctionnement. Vous pouvez ajuster le nombre
    d'articles en passant `n=40` ou tout autre chiffre dans l'URL `/demo`.

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