# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testresults
   :platform: Unix
   :synopsis: Providing manipulation with test results
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.lib.database.dbo import dbo
from hydratk.lib.debugging.simpledebug import dmsg
from hydratk.lib.system.io import cprint

db_struct = {
             'sqlite' : """
  CREATE TABLE test_run(
                        id VARCHAR NOT NULL, -- unique string + timestamp + process id
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id)
                       );
                       
  CREATE TABLE test_set(
                        id VARCHAR NOT NULL, -- test_run.id + test_set.tset_id
                        tset_id VARCHAR NOT NULL, -- test set path 
                        test_run_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_run_id) REFERENCES test_run(id)
                       );

  CREATE TABLE test_scenario(
                        id VARCHAR NOT NULL, -- test_run.id + test_set.id + test_scenario.ts_id
                        ts_id VARCHAR NOT NULL,
                        test_set_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_set_id) REFERENCES test_set(id)
                       );                       

  CREATE TABLE test_case(
                        id VARCHAR NOT NULL, -- test_run.id + test_set.id + test_scenario.id + test_case.tca_id
                        tca_id VARCHAR NOT NULL,
                        test_scenario_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_scenario_id) REFERENCES test_scenario(id)
                       );
                          
    CREATE TABLE test_condition(
                        id VARCHAR NOT NULL,  -- test_run.id + test_set.id + test_scenario.id + test_case.id + test_condition.tco_id
                        tco_id VARCHAR NOT NULL,
                        test_case_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_case_id) REFERENCES test_case(id)
                       );
                       
    CREATE TABLE custom_data(
                        test_run_id VARCHAR NOT NULL,
                        test_obj_id VARCHAR NOT NULL, -- test_run.id, test_set.id ..
                        test_obj_name VARCHAR NOT NULL, -- test_run, test_set, ...
                        key VARCHAR NOT NULL,
                        value VARCHAR NOT NULL,
                        FOREIGN KEY(test_run_id) REFERENCES test_run(id)
    )                                                    
"""
}

class TestResultsDB(object):
    _trdb = None
    _dsn  = None
    
    def __init__(self, dsn):
        self._trdb = dbo.DBO(dsn)
        self._dsn = dsn
    
    def create_database(self, force = False):
        if self._trdb.database_exists() == True:
            if force == True:
                self._trdb.remove_database()
            else:
                raise Exception("Database already exists dsn:{0}".format(self._dsn)) 
        else:
            self._trdb.cursor.executescript(db_struct[self._trdb.driver_name])
            cprint("Database created successfully")      