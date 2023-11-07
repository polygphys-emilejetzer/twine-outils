# -*- coding: utf-8 -*-


'''
# [Gestion sémantique de version]
Étant donné un numéro de version MAJEUR.MINEUR.CORRECTIF, il faut incrémenter :

    le numéro de version MAJEUR quand il y a des changements non rétrocompatibles,
    le numéro de version MINEUR quand il y a des ajouts de fonctionnalités rétrocompatibles,
    le numéro de version de CORRECTIF quand il y a des corrections d’anomalies rétrocompatibles.

Des libellés supplémentaires peuvent être ajoutés pour les versions de pré-livraison et pour des méta-données de construction sous forme d’extension du format MAJEURE.MINEURE.CORRECTIF.

[Gestion sémantique de version]: https://semver.org/lang/fr/
'''

import argparse
import os

from pathlib import Path
from subprocess import run

from polygphys.outils.config import FichierConfig

parseur = argparse.ArgumentParser(description='Augmenter le numéro de version d\'un programme, et le charger sur PIPy.')
parseur.add_argument('dossiers',
                    type=Path,
                    nargs='+',
                    help='Liste de répertoires contenant un fichier `setup.cfg`: dossier [dossiers [...]]')
parseur.add_argument('-n', '--niveau',
                    type=int,
                    choices=[-3, -2, -1, 0, 1, 2],
                    default=-1,
                    required=False,
                    help='Niveau de version selon la convention [GSV](https://semver.org/lang/fr/): Majeure[0|-3].Mineure[1|-2].Correctif[2|-1]')
parseur.add_argument('-s', '--sorte',
                     type=str,
                     choices=['a', 'b', 'r'],
                     required=False,
                     default='',
                     help='Type de version: [a (alpha) | b (bêta) | r («release»)]')
parseur.add_argument('-m', '--message',
                    type=str,
                    required=False,
                    default='',
                    help='Un message transmis à git dans la création de l\'étiquette.')
parseur.add_argument('-a',
                    type=bool,
                    required=False,
                    default=False,
                    help='Ajouter les fichiers modifiés au commit')
arguments = parseur.parse_args()

actuel = Path.cwd()
for dossier in arguments.dossiers:
    if dossier.exists():
        try:
            config = FichierConfig(dossier / 'setup.cfg')
            
            vieille_valeur = config.get('metadata', 'version')
            
            if vieille_valeur[-1] in 'abr':
                vieille_valeur, sorte = vieille_valeur[:-1], vieille_valeur[-1]
            else:
                vieille_valeur, sorte = vieille_valeur, ''

            if arguments.sorte:
                sorte = arguments.sorte

            chiffres = list(map(int, vieille_valeur.split('.')))

            if arguments.niveau < 0:
                arguments.niveau = len(chiffres) + arguments.niveau

            chiffres[arguments.niveau] += 1
            for i in range(arguments.niveau+1, len(chiffres)):
                chiffres[i] = 0
            
            version = '.'.join(map(str, chiffres)) + sorte
            config.set('metadata', 'version', version)

            os.chdir(dossier)
            commande = ['zsh', Path(__file__).parent / 'script.zsh', version]
            if arguments.message:
                commande += ['-m', arguments.message]
                        i
            run(, arguments.message])
        finally:
            os.chdir(actuel)
