# RecallMe Demo

Ceci est une démonstration simplifiée de l'application **RecallMe**. L'idée est de montrer comment croiser une liste de rappels produits avec vos achats.

Le script `main.py` charge une liste factice de rappels et une liste d'achats depuis `purchases.csv`, puis affiche les produits concernés.

Dans un projet réel, on utiliserait l'API officielle RappelConso, mais cette démo utilise des données locales pour faciliter les tests.

## Utilisation

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancer le script :
   ```bash
   python main.py
   ```

3. Ouvrir l'interface graphique (facultatif) :
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

4. Démarrer l'application web (facultatif) :
   ```bash
   python -m recallme.app
   ```
   Comme pour la commande précédente, lancez-la depuis le dossier parent.
   Depuis `recallme`, vous pouvez exécuter directement :
   ```bash
   python app.py
   ```
   Une fois le serveur lancé, ouvrez `http://localhost:5000` dans votre navigateur
   pour voir vos achats. Les lignes en rouge indiquent les produits rappelés.

   Cette interface web utilise un petit gabarit HTML et la librairie Bootstrap
   pour offrir un aperçu plus attrayant de vos données.

Vous devriez voir la liste des produits achetés faisant l'objet d'un rappel sanitaire.
