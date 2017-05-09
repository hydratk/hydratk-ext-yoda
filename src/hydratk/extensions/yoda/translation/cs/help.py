# -*- coding: utf-8 -*-

"""This code is a part of Yoda extension

.. module:: hydratk.extensions.yoda.translation.cs.help
   :platform: Unix
   :synopsis: Czech language translation for Yoda extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
    'name': 'Čeština',
    'ISO-639-1': 'cs'
}

''' Yoda Commands '''
help_cmd = {
    'yoda-run': 'spustí Yoda tester',
    'yoda-simul': 'spustí Yoda tester v režimu test simulace',
    'yoda-create-test-results-db': 'vytvoří databázi pro ukládání výsledků testů podle dsn konfigurace',
    'yoda-create-testdata-db': 'vytvoří databázi pro testovací data',
    # standalone with option profile yoda
    'run': 'spustí Yoda tester',
    'simul': 'spustí Yoda tester v režimu test simulace',
    'create-test-results-db': 'vytvoří databázi pro ukládání výsledků testů podle dsn konfigurace',
    'create-testdata-db': 'vytvoří databázi pro testovací data'
}

''' Yoda Options '''
help_opt = {
    'yoda-test-path': {'{h}--yoda-test-path <cesta>{e}': {'description': 'cesta k testovacímu scénáři', 'commands': ('yoda-run', 'yoda-simul')}},
    'yoda-test-run-name': {'{h}--yoda-test-run-name <název>{e}': {'description': 'identifikátor spouštěného běhu', 'commands': ('yoda-run', 'yoda-simul')}},
    'yoda-test-repo-root-dir': {'{h}--yoda-test-repo-root-dir <cesta>{e}': {'description': 'cesta ke kořenovému adresáři test. repozitáře', 'commands': ('yoda-run', 'yoda-simul')}},
    'yoda-test-results-output-create': {'{h}--yoda-test-results-output-create <stav>{e}': {'description': 'aktivuje/deaktivuje nativní zpracování výsledků testů', 'commands': ('yoda-run', 'yoda-simul')}},
    'yoda-test-results-output-handler': {'{h}--yoda-test-results-output-handler <typ>{e}': {'description': 'nastaví typ handleru pro zpracování výsledků testů', 'commands': ('yoda-run', 'yoda-simul')}},
    'yoda-db-results-dsn': {'{h}--yoda-db-results-dsn <dsn>{e}': {'description': 'definice přístupu k databázi výsledků testů', 'commands': ('yoda-run', 'yoda-simul', 'yoda-create-test-results-db')}},
    'yoda-db-testdata-dsn': {'{h}--yoda-db-testdata-dsn <dsn>{e}': {'description': 'definice přístupu k databázi testovacích dat', 'commands': ('yoda-create-testdata-db')}},
    'yoda-multiply-tests': {'{h}--yoda-multiply-tests <číslo>{e}': {'description': 'počet nalezených testů bude vynásoben zvoleným číslem', 'commands': ('yoda-run')}},
    # standalone with option profile yoda
    'test-path': {'{h}-tp, --test-path <cesta>{e}': {'description': 'cesta k testovacímu scénáři', 'commands': ('run', 'simul')}},
    'test-run-name': {'{h}-rn, --test-run-name <název>{e}': {'description': 'identifikátor spouštěného běhu', 'commands': ('run', 'simul')}},
    'test-repo-root-dir': {'{h}-rd, --test-repo-root-dir <cesta>{e}': {'description': 'cesta ke kořenovému adresáři test. repozitáře', 'commands': ('run', 'simul')}},
    'test-results-output-create': {'{h}-oc, --test-results-output-create <stav>{e}': {'description': 'aktivuje/deaktivuje nativní zpracování výsledků testů', 'commands': ('run', 'simul')}},
    'test-results-output-handler': {'{h}-oh, --test-results-output-handler <typ>{e}': {'description': 'nastaví typ handleru pro zpracování výsledků testů', 'commands': ('run', 'simul')}},
    'db-results-dsn': {'{h}--db-results-dsn <dsn>{e}': {'description': 'definice přístupu k databázi výsledků testů', 'commands': ('run', 'simul', 'create-test-results-db')}},
    'db-testdata-dsn': {'{h}--db-testdata-dsn <dsn>{e}': {'description': 'definice přístupu k databázi testovacích dat', 'commands': ('create-testdata-db')}},
    'multiply-tests': {'{h}--multiply-tests <číslo>{e}': {'description': 'počet nalezených testů bude vynásoben zvoleným číslem', 'commands': ('run')}},
}
