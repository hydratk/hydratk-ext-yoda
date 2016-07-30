# -*- coding: utf-8 -*-
"""Providing manipulation with test results

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
                         'expected' : 7
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
                        id VARCHAR NOT NULL, -- test_run_id + test_obj_id + key
                        test_run_id VARCHAR NOT NULL,
                        test_obj_id VARCHAR NOT NULL, -- test_run.id, test_set.id ..
                        test_obj_name VARCHAR NOT NULL, -- test_run, test_set, ...
                        key VARCHAR NOT NULL,
                        value VARCHAR,
                        pickled INTEGER,
                        PRIMARY KEY(id),
                        FOREIGN KEY(test_run_id) REFERENCES test_run(id)
                       );
                       
    CREATE TABLE  custom_data_opt(
                        id VARCHAR NOT NULL, -- custom_data_id + opt_name
                        custom_data_id VARCHAR NOT NULL,
                        opt_name VARCHAR NOT NULL,
                        opt_value VARCHAR,
                        PRIMARY KEY(id),
                        FOREIGN KEY(custom_data_id) REFERENCES custom_data(id)
                       );                                                    
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
                   'write_custom_data'           : "INSERT OR REPLACE INTO custom_data VALUES(?,?,?,?,?,?,?)", 
                   'create_custom_data'          : "INSERT INTO custom_data VALUES(?,?,?,?,?,?,?)",
                   'write_custom_data_opt'       : "INSERT OR REPLACE INTO custom_data_opt VALUES(?,?,?,?)",                   
                   'create_custom_data_opt'      : "INSERT INTO custom_data_opt VALUES(?,?,?)",
                   'get_test_stats'              : "select sum(total_tests) total_tests, sum(failed_tests) failed_tests, sum(passed_tests) passed_tests from test_set where test_run_id = :test_run_id",
                   'get_total_test_sets'         : "select count(tset_id) total_test_sets from test_set where test_run_id = :test_run_id",
                   'get_total_tests'             : "select count(tco_id) total_tests from test_condition where test_run_id = :test_run_id",
                   'get_failed_tests'            : "select count(tco_id) failed_tests from test_condition where test_run_id = :test_run_id and test_resolution = 'failed'",
                   'get_passed_tests'            : "select count(tco_id) passed_tests from test_condition where test_run_id = :test_run_id and test_resolution = 'passed'",                                                                                                                                                                                                       
                   'get_test_sets'               : "select * from test_set where test_run_id = :test_run_id",
                   'get_test_scenarios'          : """select distinct test_scenario.*, custom_data.key 'key', custom_data.value 'value', custom_data.pickled 'pickled' from test_scenario left join custom_data on test_scenario.id = custom_data.test_obj_id
                                                        where test_scenario.test_run_id = :test_run_id and test_scenario.test_set_id = :test_set_id and custom_data.key = 'name'                                                       
                                                   """,
                   'get_test_cases'              : """select distinct test_case.*, custom_data.key 'key', custom_data.value 'value', custom_data.pickled 'pickled' from test_case left join custom_data on test_case.id = custom_data.test_obj_id
                                                        where test_case.test_run_id = :test_run_id and test_case.test_set_id = :test_set_id and test_case.test_scenario_id = :test_scenario_id and custom_data.key = 'name'                                                       
                                                   """,
                   'get_test_conditions'         : """select distinct test_condition.*, custom_data.key 'key', custom_data.value 'value', custom_data.pickled 'pickled' from test_condition left join custom_data on test_condition.id = custom_data.test_obj_id
                                                        where test_condition.test_run_id = :test_run_id and test_condition.test_set_id = :test_set_id and test_condition.test_scenario_id = :test_scenario_id and test_condition.test_case_id = :test_case_id and custom_data.key = 'name'                                                       
                                                   """                                                                                                        
                }                           
}
 
class TestResultsDB(object):
    """Class TestResultsDB
    """
    
    _trdb = None
    _dsn  = None
    _custom_data_filter = {
               'TestScenario'  : ['id', 'events', 'pre_req', 'post_req', 'help'],            
               'TestCase'      : ['id', 'events'],            
               'TestCondition' : ['id', 'events', 'test', 'validate', 'expected_result']
               }
    
    @property
    def trdb(self):
        """ trdb property getter """
        
        return self._trdb
    
    @property
    def custom_data_filter(self):
        """ custom_data_filter property getter """
        
        return self._custom_data_filter
    
    def __init__(self, dsn):
        """Class constructor
        
        Called when object is initialized
        
        Args:
           dsn (str): dsn
            
        """    
               
        self._trdb = dbo.DBO(dsn)
        self._trdb.dbcon.text_factory = bytes        
        self._trdb.result_as_dict(True)
        self._dsn = dsn
    
    def db_check_ok(self):
        """Method checks if database is successfully created 
        
        Args:
           none
        
        Returns:
           bool: result
            
        """   
                
        result = False        
        if self._trdb.database_exists() == True:            
            self._trdb.cursor.execute(check_db_struct[self._trdb.driver_name]['query'])
            row = self._trdb.cursor.fetchone()
            if row is not None:                
                if row['expected'] == check_db_struct[self._trdb.driver_name]['expected']:
                    result = True                      
        return result
    
    def create_database(self, force=False):
        """Method creates database
        
        Args:
           force (bool): recreate database if exists
        
        Returns:
           void
           
        Raises:
           exception: Exception
            
        """   
                
        if self._trdb.database_exists() == True:
            if force == True:
                self._trdb.remove_database()
                self._trdb.connect()
            else:
                raise Exception("Database already exists dsn:{0}".format(self._dsn)) 
            
        self._trdb.cursor.executescript(db_struct[self._trdb.driver_name])
        cprint("Database created successfully")
           
    def db_action(self, action, columns):
        """Method executes write query
        
        Args:
           action (str): query
           columns (dict): binded columns
        
        Returns:
           void
            
        """   
                
        dmsg("Running action: {0} {1}".format(action, str(columns)), 3)
        self._trdb.cursor.execute(db_actions[self._trdb.driver_name][action], columns)
        self._trdb.commit()
    
    def db_data(self, action, columns):
        """Method executes read query
        
        Args:
           action (str): query
           columns (list): returned columns
        
        Returns:
           dict: query result
            
        """   
                
        dmsg("Get data action: {0} {1}".format(action, str(columns)), 3)
        self._trdb.cursor.execute(db_actions[self._trdb.driver_name][action], columns)
        return self._trdb.cursor.fetchall()


tro_handlers = {
                  'console' : 'hydratk.extensions.yoda.testresults.handlers.console' ,
                  'text'    : 'hydratk.extensions.yoda.testresults.handlers.text',
                  'html'    : 'hydratk.extensions.yoda.testresults.handlers.html'                
               }

class TestResultsOutputFactory(object):
    """Class TestResultsOutputFactory
    """
    
    _handler_name = None
    _handler      = None
    _handler_opt  = {}
        
    def __init__(self, db_dsn, handler_def='console'):
        """Class constructor
        
        Called when object is initiazed
        
        Args:
           db_dsn (str): dsn
           handler_def (str): output handler, console|html|text
            
        """   
                
        self._dispatch_handler_def(handler_def)
        if self._handler_name not in tro_handlers:
            raise ValueError('Unknown handler: {0}'.format(self._handler_name))
        
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
            raise TypeError("handler_name have to be a nonempty string, got {0}, value: {1}".format(type(handler_def).__name__, handler_def))
    
    def __getattr__(self, name):
        """Method gets attribute
        
        Args:
           name (str): attribute name
        
        Returns:
           obj: attribute value
            
        """   
                
        return getattr(self._handler, name)
    
    def __getitem__(self, name):
        """Method gets item
        
        Args:
           name (str): item name
        
        Returns:
           obj: item value
            
        """ 
                
        return getattr(self._handler, name) 
              
    def _import_tro_handler(self, handler_name):
        """Method imports output handler
        
        Args:
           handler_name (str): handler
        
        Returns:
           obj: module
            
        """ 
                
        return importlib.import_module(tro_handlers[handler_name])