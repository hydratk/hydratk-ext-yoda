# -*- coding: utf-8 -*-

"""This code is a part of Yoda extension

.. module:: hydratk.extensions.yoda.translation.en.help
   :platform: Unix
   :synopsis: English language translation for Yoda extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
} 

''' Yoda Commands '''
help_cmd = {
   'yoda-run' : 'starts the Yoda tester',   
   'yoda-simul' : 'starts the Yoda tester in test simulation mode',
   'yoda-create-test-results-db' : 'creates database for storing test results base on specified dsn configuration'                 
}

''' Yoda Options '''
help_opt = {
   'yoda-test-path' : { '{h}--yoda-test-path <path>{e}' : { 'description' : 'test scenario path', 'commands' : ('yoda-run','yoda-run-pp','yoda-simul')}},
   'yoda-test-repo-root-dir' : { '{h}--yoda-test-repo-root-dir <path>{e}' : { 'description' : 'test repository root directory', 'commands' : ('yoda-run','yoda-run-pp','yoda-simul','yoda-create-test-results-db')}},
   'yoda-db-results-enabled' : { '{h}--yoda-db-results-enabled <state>{e}' : { 'description' : 'activates/deactivates test results storage to the database', 'commands' : ('yoda-run','yoda-run-pp','yoda-simul')}},
   'yoda-db-results-dsn' : { '{h}--yoda-db-results-dsn <dsn>{e}' : { 'description' : 'test results database access definition', 'commands' : ('yoda-run','yoda-run-pp','yoda-simul','yoda-create-test-results-db')}},   
}