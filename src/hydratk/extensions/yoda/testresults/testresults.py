# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testresults.testresults
   :platform: Unix
   :synopsis: Providing manipulation with test results
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import importlib
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
                        test_run_id VARCHAR NOT NULL,
                        test_set_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        prereq_passed INTEGER,
                        postreq_passed INTEGER,
                        events_passed INTEGER,
                        failures INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_set_id) REFERENCES test_set(id)
                       );                       

  CREATE TABLE test_case(
                        id VARCHAR NOT NULL, -- test_run.id + test_set.id + test_scenario.id + TestCase._num
                        tca_id VARCHAR NOT NULL,
                        test_run_id VARCHAR NOT NULL,
                        test_set_id VARCHAR NOT NULL,
                        test_scenario_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        total_tests INTEGER,
                        failed_tests INTEGER,
                        passed_tests INTEGER,
                        events_passed INTEGER,
                        failures INTEGER,
                        log BLOB,
                        struct_log BLOB,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_scenario_id) REFERENCES test_scenario(id)
                       );
                          
    CREATE TABLE test_condition(
                        id VARCHAR NOT NULL,  -- test_run.id + test_set.id + test_scenario.id + test_case.id + TestCondition._num
                        tco_id VARCHAR NOT NULL,
                        test_run_id VARCHAR NOT NULL,
                        test_set_id VARCHAR NOT NULL,
                        test_scenario_id VARCHAR NOT NULL,
                        test_case_id VARCHAR NOT NULL,
                        start_time INTEGER NOT NULL,
                        end_time INTEGER NOT NULL, 
                        expected_result VARCHAR,                        
                        test_result VARCHAR,
                        test_resolution VARCHAR,
                        events_passed INTEGER,
                        test_exec_passed INTEGER,
                        validate_exec_passed INTEGER,   
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
                  'create_test_scenario_record' : "INSERT INTO test_scenario VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  'update_test_scenario_record' : """
                              UPDATE test_scenario SET ts_id=:ts_id,
                                                  test_run_id=:test_run_id,
                                                  test_set_id=:test_set_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  total_tests=:total_tests, 
                                                  failed_tests=:failed_tests, 
                                                  passed_tests=:passed_tests,
                                                  prereq_passed=:prereq_passed,
                                                  postreq_passed=:postreq_passed,
                                                  events_passed=:events_passed,
                                                  failures=:failures, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                  'create_test_case_record' : "INSERT INTO test_case VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  'update_test_case_record' : """
                              UPDATE test_case SET tca_id=:tca_id,
                                                  test_run_id=:test_run_id,
                                                  test_set_id=:test_set_id,
                                                  test_scenario_id=:test_scenario_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  total_tests=:total_tests, 
                                                  failed_tests=:failed_tests, 
                                                  passed_tests=:passed_tests,
                                                  events_passed=:events_passed,
                                                  failures=:failures, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                  'create_test_condition_record' : "INSERT INTO test_condition VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  'update_test_condition_record' : """
                              UPDATE test_condition SET tco_id=:tco_id,
                                                  test_run_id=:test_run_id,
                                                  test_set_id=:test_set_id,
                                                  test_scenario_id=:test_scenario_id,
                                                  test_case_id=:test_case_id,
                                                  start_time=:start_time, 
                                                  end_time=:end_time, 
                                                  expected_result=:expected_result, 
                                                  test_result=:test_result, 
                                                  test_resolution=:test_resolution,
                                                  events_passed=:events_passed,
                                                  test_exec_passed=:test_exec_passed,
                                                  validate_exec_passed=:validate_exec_passed, 
                                                  log=:log, 
                                                  struct_log=:struct_log
                              WHERE id=:id
                            """,
                   'create_custom_data'          : "INSERT INTO custom_data VALUES(?,?,?,?,?,?)",
                   'get_test_stats'              : "select sum(total_tests) total_tests, sum(failed_tests) failed_tests, sum(passed_tests) passed_tests from test_set where test_run_id = :test_run_id",
                   'get_total_test_sets'         : "select count(tset_id) total_test_sets from test_set where test_run_id = :test_run_id",
                   'get_total_tests'             : "select count(tco_id) total_tests from test_condition where test_run_id = :test_run_id",
                   'get_failed_tests'            : "select count(tco_id) failed_tests from test_condition where test_run_id = :test_run_id and test_resolution = 'failed'",
                   'get_passed_tests'            : "select count(tco_id) passed_tests from test_condition where test_run_id = :test_run_id and test_resolution = 'passed'",                                                                                                                                                                                                       
                   'get_test_sets'               : "select * from test_set where test_run_id = :test_run_id",
                   'get_test_scenarios'          : """select distinct * from test_scenario left join custom_data on test_scenario.id = custom_data.test_obj_id
                                                        where test_scenario.test_run_id = :test_run_id and test_scenario.test_set_id = :test_set_id and custom_data.key = 'name'                                                       
                                                   """,
                   'get_test_cases'              : """select distinct * from test_case left join custom_data on test_case.id = custom_data.test_obj_id
                                                        where test_case.test_run_id = :test_run_id and test_case.test_set_id = :test_set_id and test_case.test_scenario_id = :test_scenario_id and custom_data.key = 'name'                                                       
                                                   """,
                   'get_test_conditions'         : """select distinct * from test_condition left join custom_data on test_condition.id = custom_data.test_obj_id
                                                        where test_condition.test_run_id = :test_run_id and test_condition.test_set_id = :test_set_id and test_condition.test_scenario_id = :test_scenario_id and test_condition.test_case_id = :test_case_id and custom_data.key = 'name'                                                       
                                                   """                                                                                                        
                }                           
}
 
class TestResultsDB(object):
    _trdb = None
    _dsn  = None
    _custom_data_filter = {
               'TestScenario'  : ['id', 'events', 'pre_req', 'post_req', 'help'],            
               'TestCase'      : ['id', 'events'],            
               'TestCondition' : ['id', 'events', 'test', 'validate', 'expected_result']
               }
    
    @property
    def custom_data_filter(self):
        return self._custom_data_filter
    
    def __init__(self, dsn):
        self._trdb = dbo.DBO(dsn)
        self._trdb.dbcon.text_factory = bytes        
        self._trdb.result_as_dict(True)
        self._dsn = dsn
    
    def db_check_ok(self):
        result = False        
        if self._trdb.database_exists() == True:            
            self._trdb.cursor.execute(check_db_struct[self._trdb.driver_name]['query'])
            row = self._trdb.cursor.fetchone()
            if row is not None:                
                if row['expected'] == check_db_struct[self._trdb.driver_name]['expected']:
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
    
    def db_data(self, action, columns):
        dmsg("Get data action: {} {}".format(action, str(columns)), 3)
        self._trdb.cursor.execute(db_actions[self._trdb.driver_name][action], columns)
        return self._trdb.cursor.fetchall()


tro_handlers = {
                  'console' : 'hydratk.extensions.yoda.testresults.handlers.console' ,
                  'text'    : 'hydratk.extensions.yoda.testresults.handlers.text',
                  'html'    : 'hydratk.extensions.yoda.testresults.handlers.html'                
               }

class TestResultsOutputFactory(object):
    _handler_name = None
    _handler      = None
    _handler_opt  = {}
        
    def __init__(self, db_dsn, handler_def='console'):
        self._dispatch_handler_def(handler_def)
        if self._handler_name not in tro_handlers:
            raise ValueError('Unknown handler: {}'.format(self._handler_name))
        
        handler_mod   = self._import_tro_handler(self._handler_name)
        self._handler = handler_mod.TestResultsOutputHandler(db_dsn, self._handler_opt)
        
    
    def _dispatch_handler_def(self, handler_def):
        if type(handler_def).__name__ == 'str' and handler_def != '':            
            handltok = handler_def.split(':')
            self._handler_name = handltok[0]
            if len(handltok) > 1: #dispatch options
                handltok_opt = handltok[1].split(';')                
                for opt in handltok_opt:
                    opt_data = opt.split('=')                    
                    self._handler_opt[opt_data[0]] = opt_data[1]
                
        else:
            raise TypeError("handler_name have to be a nonempty string, got {}, value: {}".format(type(handler_def).__name__, handler_def))
    
    def __getattr__(self,name):
        return getattr(self._handler, name)
    
    def __getitem__(self, name):
        return getattr(self._handler, name) 
              
    def _import_tro_handler(self, handler_name):
        return importlib.import_module(tro_handlers[handler_name])