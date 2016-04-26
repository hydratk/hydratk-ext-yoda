# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testresults.handlers.html
   :platform: Unix
   :synopsis: Default test results html output handler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

class TestResultsOutputHandler(object):
    _db_dsn  = None
    _options = {}
    
    def __init__(self, db_dsn, options = {}):
        self._db_dsn  = db_dsn
        self._options = options
            
    def create(self):
        print("Creating html output")