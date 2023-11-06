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
parseur.add_argument('--niveau',
                    type=int,
                    choices=[-3, -2, -1, 0, 1, 2],
                    default=-1,
                    required=False,
                    help='Niveau de version selon la convention [GSV](https://semver.org/lang/fr/): Majeure[0|-3].Mineure[1|-2].Correctif[2|-1]')
arguments = parseur.parse_args()

actuel = Path.cwd()
for dossier in arguments.dossiers:
    if dossier.exists():
        try:
            config = FichierConfig(dossier / 'setup.cfg')
            
            vieille_valeur = config.get('metadata', 'version')
            chiffres = list(map(int, vieille_valeur.split('.')))

            if arguments.niveau < 0:
                arguments.niveau = len(chiffres) + arguments.niveau

            chiffres[arguments.niveau] += 1
            for i in range(arguments.niveau+1, len(chiffres)):
                chiffres[i] = 0
            
            config.set('metadata', 'version', '.'.join(map(str, chiffres)))

            os.chdir(dossier)
            run(['zsh', Path(__file__).parent / 'script.zsh'])
        finally:
            os.chdir(actuel)
