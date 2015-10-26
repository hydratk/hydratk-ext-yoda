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
   'yoda-simul' : 'spustí Yoda tester v režimu test simulace'               
}

''' Yoda Options '''
help_opt = {
   'yoda-test-path' : { '{h}--yoda-test-path <cesta>{e}' : { 'description' : 'cesta k testovacímu scénáři', 'commands' : ('yoda-run','yoda-simul')}},
   'yoda-test-repo-root-dir' : { '{h}--yoda-test-repo-root-dir <cesta>{e}' : { 'description' : 'cesta ke kořenovému adresáři test. repozitáře', 'commands' : ('yoda-run','yoda-simul')}}
}