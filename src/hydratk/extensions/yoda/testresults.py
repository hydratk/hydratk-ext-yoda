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
from hydratk.lib.debugging.simpledebug import dmsg


check_db_struct = {
            'sqlite' : { 'query'    : "SELECT count(*) expected from sqlite_master where type='table'",
                         'expected' : 6
                        }                     
}

db_struct = {
             'sqlite' : """
  CREATE TABLE test_run(
                        id VARCHAR NOT NULL, -- unique string + timestamp + process id
                        name VARCHAR,
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
                        id VARCHAR NOT NULL, -- test_run.id + test_set.id + TestScenario._num
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
                        id VARCHAR NOT NULL, -- test_run.id + test_set.id + test_scenario.id + TestCase._num
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
                        id VARCHAR NOT NULL,  -- test_run.id + test_set.id + test_scenario.id + test_case.id + TestCondition._num
                        tco_id VARCHAR NOT NULL,
                        test_case_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        expected_result VARCHAR,                        
                        test_result VARCHAR,
                        test_resolution VARCHAR,
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
                        pickled INTEGER,
                        FOREIGN KEY(test_run_id) REFERENCES test_run(id)
    )                                                    
"""
}

db_actions = {
       'sqlite': {
                  'create_test_run_record' : "INSERT INTO test_run VALUES (?,?,?,?,?,?,?,?,?)",
                  'update_test_run_record' : """
                              UPDATE test_run SET name=:name,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  total_tests=:total_tests, 
                                                  failed_tests=:failed_tests, 
                                                  passed_tests=:passed_tests, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                  'create_test_set_record' : "INSERT INTO test_set VALUES (?,?,?,?,?,?,?,?,?,?)",
                  'update_test_set_record' : """
                              UPDATE test_set SET tset_id=:tset_id,
                                                  test_run_id=:test_run_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  total_tests=:total_tests, 
                                                  failed_tests=:failed_tests, 
                                                  passed_tests=:passed_tests, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,        
                  'create_test_scenario_record' : "INSERT INTO test_scenario VALUES (?,?,?,?,?,?,?,?,?,?)",
                  'update_test_scenario_record' : """
                              UPDATE test_scenario SET ts_id=:ts_id,
                                                  test_set_id=:test_set_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  total_tests=:total_tests, 
                                                  failed_tests=:failed_tests, 
                                                  passed_tests=:passed_tests, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                  'create_test_case_record' : "INSERT INTO test_case VALUES (?,?,?,?,?,?,?,?,?,?)",
                  'update_test_case_record' : """
                              UPDATE test_case SET tca_id=:tca_id,
                                                  test_scenario_id=:test_scenario_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  total_tests=:total_tests, 
                                                  failed_tests=:failed_tests, 
                                                  passed_tests=:passed_tests, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                  'create_test_condition_record' : "INSERT INTO test_condition VALUES (?,?,?,?,?,?,?,?,?,?)",
                  'update_test_condition_record' : """
                              UPDATE test_condition SET tco_id=:tco_id,
                                                  test_case_id=:test_case_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  expected_result=:expected_result, 
                                                  test_result=:test_result, 
                                                  test_resolution=:test_resolution, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                   'create_custom_data'          : "INSERT INTO custom_data VALUES(?,?,?,?,?,?)"                                                                                                                                                                 
                }                           
}
 
class TestResultsDB(object):
    _trdb = None
    _dsn  = None
    _custom_data_filter = {
               'TestScenario'  : ['id', 'events', 'pre-req', 'post-req'],            
               'TestCase'      : ['id', 'events'],            
               'TestCondition' : ['id', 'events', 'test', 'validate', 'expected_result']
               }
    
    @property
    def custom_data_filter(self):
        return self._custom_data_filter
    
    def __init__(self, dsn):
        self._trdb = dbo.DBO(dsn)
        self._dsn = dsn
    
    def db_check_ok(self):
        result = False        
        if self._trdb.database_exists() == True:            
            self._trdb.cursor.execute(check_db_struct[self._trdb.driver_name]['query'])
            row = self._trdb.cursor.fetchone()
            if row is not None:
                if row[0] == check_db_struct[self._trdb.driver_name]['expected']:
                    result = True                      
        return result
    
    def create_database(self, force = False):
        if self._trdb.database_exists() == True:
            if force == True:
                self._trdb.remove_database()
            else:
                raise Exception("Database already exists dsn:{0}".format(self._dsn)) 
        else:
            self._trdb.cursor.executescript(db_struct[self._trdb.driver_name])
            cprint("Database created successfully")
       
    def db_action(self, action, columns):
        dmsg("Running action: {} {}".format(action, str(columns)), 3)
        self._trdb.cursor.execute(db_actions[self._trdb.driver_name][action], columns)
        self._trdb.commit()    
  