# -*- coding: utf-8 -*-

import argparse
import os

from pathlib import Path
from subprocess import run

from polygphys.outils.config import FichierConfig

parseur = argparse.ArgumentParser(description='Augmenter le numéro de version d\'un programme, et le charger sur PIPy.')
parseur.add_argument('dossiers', type=Path, nargs='+')
parseur.add_argument('--niveau', type=int, default=-1, required=False)
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
