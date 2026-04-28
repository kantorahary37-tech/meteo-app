### Sauvegarde des modules python installés dans le fichier requirements.txt

```bash
pip freeze > requirements.txt
```

### Commandes Git utiles

#### Initialiser un dépôt Git
```bash
git init
```

#### Cloner un dépôt existant
```bash
git clone <url-du-repo>
```

#### Vérifier l'état du dépôt
```bash
git status
```

#### Ajouter des fichiers à l'index (staging)
```bash
git add .                    # Ajouter tous les fichiers
git add <fichier>           # Ajouter un fichier spécifique
```

#### Créer un commit
```bash
git commit -m "Message du commit"
```

#### Voir l'historique des commits
```bash
git log                      # Historique complet
git log --oneline            # Historique simplifié
```

#### Créer et changer de branche
```bash
git branch <nom-branche>     # Créer une branche
git checkout <nom-branche>   # Changer de branche
git checkout -b <nom-branche> # Créer et changer de branche
```

#### Fusionner une branche
```bash
git merge <nom-branche>
```

#### Ajouter un dépôt distant
```bash
git remote add origin <url-du-repo>
```

#### Envoyer vers le dépôt distant (Github)
```bash
git push origin <nom-branche>
```

#### Récupérer les modifications du dépôt distant
```bash
git pull origin <nom-branche>
```

#### Annuler des modifications
```bash
git restore <fichier>                    # Annuler les modifs d'un fichier
git restore --staged <fichier>           # Retirer un fichier de l'index
git reset --hard HEAD                    # Annuler toutes les modifs locales
```

#### Voir les différences
```bash
git diff                                 # Modifications non indexées
git diff --staged                        # Modifications indexées
```

#### Stash (mettre de côté temporairement)
```bash
git stash                                # Mettre de côté les modifs
git stash pop                            # Réappliquer les modifs mises de côté
````