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
   'yoda-simul' : 'starts the Yoda tester in test simulation mode'                
}

''' Yoda Options '''
help_opt = {
   'yoda-test-path' : { '{h}--yoda-test-path <path>{e}' : { 'description' : 'test scenario path', 'commands' : ('yoda-run', 'yoda-simul')}},
   'yoda-test-repo-root-dir' : { '{h}--yoda-test-repo-root-dir <path>{e}' : { 'description' : 'test repository root directory', 'commands' : ('yoda-run', 'yoda-simul')}}
}