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
   'yoda-create-test-results-db' : 'creates database for storing test results base on specified dsn configuration',
   #standalone with option profile yoda                  
   'run' : 'starts the Yoda tester',   
   'simul' : 'starts the Yoda tester in test simulation mode',
   'create-test-results-db' : 'creates database for storing test results base on specified dsn configuration'
}

''' Yoda Options '''
help_opt = {
   'yoda-test-path' : { '{h}--yoda-test-path <path>{e}' : { 'description' : 'test scenario path', 'commands' : ('yoda-run','yoda-simul')}},
   'yoda-test-run-name' : { '{h}--yoda-test-run-name <name>{e}' : { 'description' : 'test run identification', 'commands' : ('yoda-run','yoda-simul')}},
   'yoda-test-repo-root-dir' : { '{h}--yoda-test-repo-root-dir <path>{e}' : { 'description' : 'test repository root directory', 'commands' : ('yoda-run','yoda-simul','yoda-create-test-results-db')}},
   'yoda-test-results-output-create' : { '{h}--yoda-test-results-output-create <state>{e}' : { 'description' : 'activates/deactivates native test results output handler', 'commands' : ('yoda-run','yoda-simul')}},
   'yoda-test-results-output-handler' : { '{h}-a, --yoda-test-results-output-handler <type>{e}' : { 'description' : 'set the test results output handler type', 'commands' : ('yoda-run','yoda-simul')}},   
   'yoda-db-results-dsn' : { '{h}--yoda-db-results-dsn <dsn>{e}' : { 'description' : 'test results database access definition', 'commands' : ('yoda-run','yoda-simul','yoda-create-test-results-db')}},
   #standalone with option profile yoda
   'test-path' : { '{h}-tp, --test-path <path>{e}' : { 'description' : 'test scenario path', 'commands' : ('run','simul')}},
   'test-run-name' : { '{h}-tn, --test-run-name <name>{e}' : { 'description' : 'test run identification', 'commands' : ('run','simul')}},
   'test-repo-root-dir' : { '{h}-tr, --test-repo-root-dir <path>{e}' : { 'description' : 'test repository root directory', 'commands' : ('run','simul','create-test-results-db')}},
   'test-results-output-create' : { '{h}-oc, --test-results-output-create <state>{e}' : { 'description' : 'activates/deactivates native test results output handler', 'commands' : ('run','simul')}},
   'test-results-output-handler' : { '{h}-oh, --test-results-output-handler <type>{e}' : { 'description' : 'set the test results output handler type', 'commands' : ('run','simul')}},
   'db-results-dsn' : { '{h}--db-results-dsn <dsn>{e}' : { 'description' : 'test results database access definition', 'commands' : ('run','simul','create-test-results-db')}},       
}