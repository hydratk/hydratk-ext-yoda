# -*- coding: utf-8 -*-

"""This code is a part of Yoda extension

.. module:: hydratk.extensions.yoda.translation.en.help
   :platform: Unix
   :synopsis: Czech language translation for Yoda extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 

''' Yoda Commands '''
help_cmd = {
   'yoda-run' : 'spustí Yoda tester',
   'yoda-simul' : 'spustí Yoda tester v režimu test simulace',
   'yoda-create-test-results-db' : 'vytvoří databázi pro ukládání výsledků testů podle dsn konfigurace'               
}

''' Yoda Options '''
help_opt = {
   'yoda-test-path' : { '{h}--yoda-test-path <cesta>{e}' : { 'description' : 'cesta k testovacímu scénáři', 'commands' : ('yoda-run','yoda-simul')}},
   'yoda-test-repo-root-dir' : { '{h}--yoda-test-repo-root-dir <cesta>{e}' : { 'description' : 'cesta ke kořenovému adresáři test. repozitáře', 'commands' : ('yoda-run','yoda-simul','yoda-create-test-results-db')}},
   'yoda-db-results-enabled' : { '{h}--yoda-db-results-enabled <stav>{e}' : { 'description' : 'aktivuje/deaktivuje ukládání výsledků testů do databáze', 'commands' : ('yoda-run','yoda-simul')}},
   'yoda-db-results-dsn' : { '{h}--yoda-db-results-dsn <dsn>{e}' : { 'description' : 'definice přístupu k databázi výsledků testů', 'commands' : ('yoda-run','yoda-simul','yoda-create-test-results-db')}}
}