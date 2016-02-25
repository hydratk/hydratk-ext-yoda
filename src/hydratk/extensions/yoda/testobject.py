# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testobject
   :platform: Unix
   :synopsis: Providing automated testing functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
from hydratk.core.event import Event
from hydratk.core.masterhead import MasterHead
import sys
import traceback
from xtermcolor import colorize
import time
import hashlib
import random
import os
import cPickle as pickle
from hydratk.lib.debugging.simpledebug import dmsg

class TestObject(object):    
    
    @property
    def parent(self):
        return self._parent    
    
    def getattr(self, name):
        result = None
        name = name.lower()
        if name in self._attr:
            result = self._attr[name]
        return result
        
    def setattr(self,key,val):
        if key != '':
            key = key.lower();
            key = key.replace('-','_')
            self._attr[key] = val
    
            
    def __getattr__(self,name):        
        result = None
        name = name.lower()
        if name in self._attr:
            result = self._attr[name]
        return result
    
    def get_auto_break(self):
        m = MasterHead.get_head()        
        return m.ext_cfg['Yoda']['auto_break'] if 'auto_break' in m.ext_cfg['Yoda'] else None
        
    def _explain(self, exc_name, exc_value, test_hierarchy, tb):
        tb.pop() #removing unwanted last line        
        result = """
Exception: {exc_name}
    Value: {exc_value}
    Trace:
      from: Test set: {test_set_file}""".format(
                                                 test_set_file=test_hierarchy['test_set_file'], 
                                                 exc_name=exc_name, 
                                                 exc_value=exc_value
                                               )
            
        if tb[4].strip() == 'exec(code, globals(), self._locals)': 
            test_scenario        = "\n      from:  Test scenario: {test_scenario}".format(test_scenario = test_hierarchy['test_scenario']) if test_hierarchy['test_scenario'] is not None else ''
            test_scenario_node   = "\n      from:    Test scenario node: {node}, {line}".format(node = test_hierarchy['test_scenario_node'], line=tb[5].split(',')[1].strip()) if test_hierarchy['test_scenario_node'] is not None else ''
            test_case            = "\n      from:    Test case: {test_case}".format(test_case = test_hierarchy['test_case']) if test_hierarchy['test_case'] is not None else ''
            test_case_node       = "\n      from:      Test case node: {node}, {line}".format(node = test_hierarchy['test_case_node'], line=tb[5].split(',')[1].strip()) if test_hierarchy['test_case_node'] is not None else ''
            test_condition       = "\n      from:      Test condition: {test_condition}".format(test_condition = test_hierarchy['test_condition']) if test_hierarchy['test_condition'] is not None else ''
            test_condition_node  = "\n      from:        Test condition node: {node}, {line}".format(node = test_hierarchy['test_condition_node'], line=tb[5].split(',')[1].strip()) if test_hierarchy['test_condition_node'] is not None else ''          
                      
          
            result += "{test_scenario}{test_scenario_node}{test_case}{test_case_node}{test_condition}{test_condition_node}".format(
                                                                                                     test_scenario=test_scenario,
                                                                                                     test_scenario_node=test_scenario_node,
                                                                                                     test_case=test_case,
                                                                                                     test_case_node=test_case_node,                                                                                                                 
                                                                                                     test_condition=test_condition,                              
                                                                                                     test_condition_node=test_condition_node                              
                                                                                                                                   )
    
            if len(tb) > 6:
                for l in tb[6:]:
                    result += "\n      from:      {}".format(l.strip())                
        else: 
            for l in tb[1:]:
                result += "\n      from:      {}".format(l.strip()) 
        return result
        
    @property
    def attr(self):
        return self._attr;    

    @property
    def log(self):
        return self._log
    
    @log.setter
    def log(self, data):
        self._log += data
    
    @property
    def struct_log(self):
        return self._struct_log
     

class BreakTestRun(Exception):
    pass

class BreakTest(Exception):
    _test_object = None
    
    @property
    def test_object(self):
        return self._test_object
    
    @test_object.setter
    def test_object(self, test_obj):
        self._test_object = test_obj

class BreakTestCase(Exception):
    _test_object = None
    
    @property
    def test_object(self):
        return self._test_object
    
    @test_object.setter
    def test_object(self, test_obj):
        self._test_object = test_obj

class BreakTestScenario(Exception):
    _test_object = None
    
    @property
    def test_object(self):
        return self._test_object
    
    @test_object.setter
    def test_object(self, test_obj):
        self._test_object = test_obj

class BreakTestSet(Exception):
    _test_object = None
    
    @property
    def test_object(self):
        return self._test_object
    
    @test_object.setter
    def test_object(self, test_obj):
        self._test_object = test_obj
            


class TestRun(TestObject):
    _id                     = None
    _name                   = 'Undefined'
    _attr                   = {}
    _total_test_sets        = 0
    _total_tests            = 0
    _failed_tests           = 0
    _passed_tests           = 0
    _skipped_tests          = 0
    _run_tests              = 0
    _norun_tests            = 0
    _failures               = False
    _start_time             = None
    _end_time               = None
    _status                 = None
    _statuses               = ['started','finished','repeat','break']    
    _log                    = ''
    _struct_log             = {}
    
    '''Test Sets'''
    _tset                   = [] 
    _inline_tests           = []
    '''Test Engine'''
    _te                     = None  
    
    def __init__(self, test_engine = None):
        self._id                     = hashlib.md5('{0}{1}{2}'.format(random.randint(100000000,999999999), time.time(), os.getpid())).hexdigest()        
        self._total_test_sets        = 0
        self._total_tests            = 0
        self._failed_tests           = 0
        self._passed_tests           = 0
        self._skipped_tests          = 0
        self._norun_tests            = 0
        self._failures               = False
        self._start_time             = time.time()
        self._end_time               = -1
        self._tset                   = []
        self._inline_tests           = []
        self._te                     = test_engine
        self._log                    = ''
        self._struct_log             = {}

    
    def create_db_record(self):
        self._te.test_results_db.db_action(
                                                   'create_test_run_record',
                                                 [
                                                  self._id,
                                                  self._name,
                                                  self._start_time,
                                                  self._end_time,
                                                  self._total_tests,
                                                  self._failed_tests,
                                                  self._passed_tests,
                                                  self._log,
                                                  pickle.dumps(self._struct_log)  
                                                ])
    def update_db_record(self):
        self._te.test_results_db.db_action(
                                                   'update_test_run_record',
                                                 {
                                                  'id'           : self._id,
                                                  'name'         : self._name,
                                                  'start_time'   : self._start_time,
                                                  'end_time'     : self._end_time,
                                                  'total_tests'  : self._total_tests,
                                                  'failed_tests' : self._failed_tests,
                                                  'passed_tests' : self._passed_tests,
                                                  'log'          : self._log,
                                                  'struct_log'   : pickle.dumps(self._struct_log)  
                                                })
    
    def write_custom_data(self):
        have_filter = 'TestRun' in self._te.test_results_db.custom_data_filter
        for key, value in self._attr.items():
            pickled = 0
            if have_filter:
                if key in self._te.test_results_db.custom_data_filter['TestRun']:
                    continue
            if type(value).__name__ not in ['int','float','str']:
                value = pickle.dumps(value)
                pickled = 1
            self._te.test_results_db.db_action(
                                                   'create_custom_data',
                                                 [
                                                  self._te.test_run.id,
                                                  self._id,
                                                  'Test-Run',
                                                  key,
                                                  value,
                                                  pickled                                                                                                    
                                                 ]) 
               
    @property
    def te(self):
        return self._te
    
    @te.setter
    def te(self,test_engine):
        self._te = test_engine
                    
    @property
    def inline_tests(self):
        return self._inline_tests
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
           
    @property
    def total_test_sets(self):
        return self._total_test_sets
    
    @total_test_sets.setter
    def total_test_sets(self, total):
        self._total_test_sets = total
        
    @property
    def total_tests(self):
        return self._total_tests
    
    @total_tests.setter
    def total_tests(self, total):
        self._total_tests = total        

    @property
    def failed_tests(self):
        return self._failed_tests
    
    @failed_tests.setter
    def failed_tests(self, total):
        self._failed_tests = total  

    @property
    def passed_tests(self):
        return self._passed_tests
    
    @passed_tests.setter
    def passed_tests(self, total):
        self._passed_tests = total  

    @property
    def skipped_tests(self):
        return self._skipped_tests
    
    @skipped_tests.setter
    def skipped_tests(self, total):
        self._skipped_tests = total

    @property
    def norun_tests(self):
        return self._norun_tests
    
    @norun_tests.setter
    def norun_tests(self, total):
        self._norun_tests = total          

    @property
    def run_tests(self):
        return self._run_tests
    
    @run_tests.setter
    def run_tests(self, total):
        self._run_tests = total  
                
    @property
    def failures(self):
        return self._passed_tests
    
    @failures.setter
    def failures(self, total):
        self._failures = total  

    @property
    def status(self):
        return self._status;
    
    @status.setter
    def status(self,status):
        self._status = status
        
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, time):
        self._start_time = time 

    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, time):
        self._end_time = time 

    @property
    def tset(self):
        return self._tset
    
    @tset.setter
    def tset(self, tset):
        self._tset = tset 
                    
    def __repr__(self):
        return ( """
                 total_test_sets = {0}\n
                 total_tests     = {1}
                 failed_tests    = {2}
                 passed_tests    = {3}
                 failures        = {4}
                 start_time      = {5}
                 end_time        = {6}
                 tset            = {7}
                 """.format(self.total_test_sets,
                            self.total_tests,
                            self.failed_tests,
                            self.passed_tests,
                            self.failures,
                            self.start_time,
                            self.end_time,
                            self.tset)
                 )
        
    def break_test_run(self, reason):        
        self.status                      = 'break' # testc condition break
        raise BreakTestRun(reason)
         
class TestSet(TestObject):
    _id                      = None
    _attr                    = {}
    _current_test_base_path  = ''
    _current_test_set_file   = ''
    _parsed_tests            = {
                                 'total_ts' : 0,
                                 'total_tca' : 0,
                                 'total_tco' : 0
                                }
    _total_tests             = 0
    _failed_tests            = 0
    _passed_tests            = 0
    _failed_ts               = 0
    _passed_ts               = 0
    _failures                = False
    _start_time              = None
    _end_time                = None
    _log                     = ''
    _struct_log              = {}
    
    '''Test Scenarios'''
    _ts                      = []         

    '''Test Run'''
    _test_run                = None
    _current                 = None

    @property
    def id(self):
        return self._id
    
    @property
    def test_run(self):        
        return self._test_run
    
    @test_run.setter
    def test_run(self,tr):
        self._test_run = tr
    
    @property
    def current_test_base_path(self):
        return self._current_test_base_path
    
    @current_test_base_path.setter
    def current_test_base_path(self, path):
        self._current_test_base_path = path        
   
    @property
    def current_test_set_file(self):
        return self._current_test_set_file
    
    @current_test_set_file.setter
    def current_test_set_file(self, path):
        self._current_test_set_file = path 
         
    @property
    def parsed_tests(self):
        return self._parsed_tests
    
    @parsed_tests.setter
    def parsed_tests(self, total):
        self._parsed_tests = total   
   
    @property
    def total_tests(self):
        return self._total_tests
    
    @total_tests.setter
    def total_tests(self, total):
        self._total_tests = total        

    @property
    def failed_tests(self):
        return self._failed_tests
    
    @failed_tests.setter
    def failed_tests(self, total):
        self._failed_tests = total  

    @property
    def passed_tests(self):
        return self._passed_tests
    
    @passed_tests.setter
    def passed_tests(self, total):
        self._passed_tests = total   

    @property
    def failed_ts(self):
        return self._failed_ts
    
    @failed_ts.setter
    def failed_ts(self, total):
        self._failed_ts = total  

    @property
    def passed_ts(self):
        return self._passed_ts
    
    @passed_ts.setter
    def passed_ts(self, total):
        self._passed_ts = total   

    @property
    def failures(self):
        return self._failures;
    
    @failures.setter
    def failures(self, status):
        if status in (True, False):
            self._failures = status
                
    @property
    def ts(self):
        return self._ts
    
    @ts.setter
    def ts(self, ts):
        self._ts = ts 

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, time):
        self._start_time = time 

    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, time):
        self._end_time = time            
    
    def __init__(self, current, test_set_file):
        if test_set_file != '<str>':        
            self._current_test_base_path  = os.path.dirname(test_set_file)
       
        id_salt = '{}{}{}'.format(test_set_file,random.randint(100000000, 999999999),current.te.exec_level)
        self._current_test_set_file   = test_set_file
        self._id                      = hashlib.md5('{0}{1}{2}'.format(current.te.test_run.id, self._current_test_set_file, id_salt)).hexdigest()    
        self._total_tests             = 0
        self._failed_tests            = 0
        self._passed_tests            = 0
        self._failed_ts               = 0
        self._passed_ts               = 0
        self._failures                = False
        self._start_time              = time.time()
        self._end_time                = -1
        self._log                     = ''
        self._struct_log              = {}
        
        '''Test Scenarios'''
        self._ts                      = []
        self._current                 = current 
        
    
    def create_db_record(self):        
        self._current.te.test_results_db.db_action(
                                                   'create_test_set_record',
                                                 [
                                                  self._id,                                                  
                                                  self._current_test_set_file,
                                                  self._current.te.test_run.id,
                                                  self._start_time,
                                                  self._end_time,
                                                  self._total_tests,
                                                  self._failed_tests,
                                                  self._passed_tests,
                                                  self._log,                                                  
                                                  pickle.dumps(self._struct_log)  
                                                ])
    
    def update_db_record(self):
        self._current.te.test_results_db.db_action(
                                                   'update_test_set_record',
                                                 {
                                                  'id'           : self._id,                                                  
                                                  'tset_id'      : self._current_test_set_file,
                                                  'test_run_id'  : self._current.te.test_run.id,
                                                  'start_time'   : self._start_time,
                                                  'end_time'     : self._end_time,
                                                  'total_tests'  : self._total_tests,
                                                  'failed_tests' : self._failed_tests,
                                                  'passed_tests' : self._passed_tests,
                                                  'log'          : self._log,                                                  
                                                  'struct_log'   : pickle.dumps(self._struct_log)   
                                                })
    
    def write_custom_data(self):
        have_filter = 'TestSet' in self._current.te.test_results_db.custom_data_filter
        for key, value in self._attr.items():
            pickled = 0
            if have_filter:
                if key in self._current.te.test_results_db.custom_data_filter['TestSet']:
                    continue
            if type(value).__name__ not in ['int','float','str']:
                value = pickle.dumps(value)
                pickled = 1
            self._current.te.test_results_db.db_action(
                                                   'create_custom_data',
                                                 [
                                                  self._current.te.test_run.id,
                                                  self._id,
                                                  'Test-Set',
                                                  key,
                                                  value,
                                                  pickled                                                                                                    
                                                 ])    
    
    def __repr__(self):
        result = '';
        for var,val in self.__dict__.items():
            if var == '_ts':
                result += "_ts= [\n"
                for obj in self._ts:
                    result += "{0},\n".format(str(obj))
                result += "]\n"
            else:
                result += "{var} = {val}\n".format(var=var,val=val)
           
        return result;
           
        
    def append_ts(self, ts):
        if isinstance(ts, TestScenario):
            self._ts.append(ts)
           
        
    def reset_data(self):
        self.current_test_base_path  = None
        self.current_test_set_file   = None
        self.total_tests             = 0
        self.failed_tests            = 0
        self.passed_tests            = 0
        self.failed_ts               = 0
        self.passed_ts               = 0
        self.failures                = False
        self.start_time              = None
        self.end_time                = None
        '''Test Scenarios'''
        self.ts                      = [] 
        
    def run(self): 
        import pprint
        current      = self._current
        current.tset = self
        this         = self
        
        current.te.test_run.tset.append(self) 
                             
        for ts in self.ts:
            run_ts = True
            if current.te.ts_filter is not None and type(current.te.ts_filter).__name__ == 'list' and len(current.te.ts_filter) > 0:                    
                if ts.id is not None and ts.id != '' and ts.id not in current.te.ts_filter:
                    print(ts.id)
                    pprint.pprint(current.te.ts_filter)
                    run_ts = False
                
            if run_ts:
                if self._current.te.have_test_results_db:
                    try:
                        ts.start_time = time.time()                    
                        ts.create_db_record()
                        ts.write_custom_data()
                    except:
                        print(sys.exc_info())
                        ex_type, ex, tb = sys.exc_info()
                        traceback.print_tb(tb)
                        raise Exception('Failed to create test_scenario database record')
                    
                print("Running test scenario {0}".format(ts.id)) 
                ts.status          = 'started'
                self._this         = ts
                           
                while ts.status != 'finished':
                    if ts.status in ('started','repeat'):
                        try:
                            ts.run()
                        except (BreakTestRun, BreakTestSet) as exc:
                            self.status = 'break'
                            raise exc
                        except BreakTestScenario as exc:
                            ts.resolution = 'break'
                            continue                            
                    elif ts.status == 'break':
                        break;
                ts.resolution = 'completed'
                if self._current.te.have_test_results_db:
                    try:
                        ts.end_time = time.time()                    
                        ts.update_db_record()
                    except:
                        print(sys.exc_info())
                        raise Exception('Failed to update test_scenario database record')
            else:
                ts.resolution = 'skipped'
                print("Filter: Skippind test scenario {0}".format(ts.id))
        
    
    def break_test_set(self, reason, test_object = None):
        self.status                      = 'break' # testc condition break
        b = BreakTestSet(reason)
        b.test_object = test_object
        raise BreakTestSet(reason)
    
        
class TestScenario(TestObject):
    _id             = None
    _num            = None
    _attr           = {}
    _tca            = []
    _resolution     = None
    _status         = None    
    _statuses       = ['started','finished','repeat','break']
    _action         = None
    _prereq_passed  = None
    _postreq_passed = None
    _events_passed  = None    
    _failures       = False       
    _total_tests    = 0
    _failed_tests   = 0
    _passed_tests   = 0        
    _start_time     = None
    _end_time       = None
    _parent         = None #parent Test Set
    _current        = None
    _log            = ''
    _struct_log     = {}

    
    def exec_test(self, test_path):
        self._current.te.exec_test(test_path)
    
    def __init__(self, ts_num, parent_tset, current):
        self._num            = ts_num   
        id_salt              = '{}{}'.format(random.randint(100000000, 999999999),current.te.exec_level)     
        self._id             = hashlib.md5('{0}{1}{2}{3}'.format(current.te.test_run.id, parent_tset.id, ts_num, id_salt)).hexdigest()
        self._attr           = {}
        self._tca            = []
        self._resolution     = None 
        self._status         = None
        self._statuses       = ['started','finished','repeat','break']    
        self._action         = None              
        self._prereq_passed  = None
        _events_passed       = None         
        self._failures       = False       
        self._total_tests    = 0
        self._failed_tests   = 0
        self._passed_tests   = 0        
        self._start_time     = 0
        self._end_time       = -1
        self._parent         = parent_tset 
        self._current        = current   

    
    @property
    def id(self):
        return self._attr['id']
    
    @property
    def num(self):
        return self._num
    
    def create_db_record(self):
        self._current.te.test_results_db.db_action(
                                                   'create_test_scenario_record',
                                                 [
                                                  self._id,                                                  
                                                  self._attr['id'],
                                                  self._current.te.test_run.id,
                                                  self._parent.id, # test set
                                                  self._start_time,
                                                  self._end_time,
                                                  self._total_tests,
                                                  self._failed_tests,
                                                  self._passed_tests,
                                                  self._log,                                                  
                                                  pickle.dumps(self._struct_log)  
                                                ])
               
    def update_db_record(self):
        self._current.te.test_results_db.db_action(
                                                   'update_test_scenario_record',
                                                 {
                                                  'id'           : self._id,                                                  
                                                  'ts_id'        : self._attr['id'],
                                                  'test_run_id'  : self._current.te.test_run.id,
                                                  'test_set_id'  : self._parent.id,
                                                  'start_time'   : self._start_time,
                                                  'end_time'     : self._end_time,
                                                  'total_tests'  : self._total_tests,
                                                  'failed_tests' : self._failed_tests,
                                                  'passed_tests' : self._passed_tests,
                                                  'log'          : self._log,                                                  
                                                  'struct_log'   : pickle.dumps(self._struct_log)   
                                                }) 
        
    def write_custom_data(self):
        have_filter = 'TestCase' in self._current.te.test_results_db.custom_data_filter
        for key, value in self._attr.items():
            pickled = 0
            if have_filter:
                if key in self._current.te.test_results_db.custom_data_filter['TestScenario']:
                    continue
            if type(value).__name__ not in ['int','float','str']:
                value = pickle.dumps(value)
                pickled = 1
            self._current.te.test_results_db.db_action(
                                                   'create_custom_data',
                                                 [
                                                  self._current.te.test_run.id,
                                                  self._id,
                                                  'Test-Scenario',
                                                  key,
                                                  value,
                                                  pickled                                                                                                    
                                                 ])   

    def run(self):                   
        '''Define missing locals'''        
        this              = self
        self._current.ts  = self
        current           = self._current       
        parent            = self._parent
        mh                = MasterHead.get_head()
        test_hierarchy    = {
                               'test_set_file'       : this.parent.current_test_set_file,
                               'test_scenario'       : "Test-Scenario-{}".format(self._num),
                               'test_scenario_node'  : None, 
                               'test_case'           : None,
                               'test_case_node'      : None,
                               'test_condition'      : None,
                               'test_condition_node' : None     
                            }
        
        if self.pre_req != None:
            try:
                ev = Event('yoda_before_exec_ts_prereq', self.pre_req)        
                if (mh.fire_event(ev) > 0):
                    self.pre_req = ev.argv(0)
                if ev.will_run_default():                    
                    test_hierarchy['test_scenario_node'] = 'pre-req'
                    if current.te.test_simul_mode == False:
                        current.te.code_stack.execute(self.pre_req, locals())                                                                                   
                    else:
                        print("Simulation: Running Test scenario %s pre-req" % self.name)
                        compile(self.pre_req,'<string>','exec')
                self.prereq_passed = True
                
            except (BreakTestRun, BreakTestSet, BreakTestScenario) as exc:
                self.status = 'break'
                raise exc
            
            except BreakTest as exc:
                raise Exception("You can't use 'break_test' outside the Test-Condition section")
            
            except BreakTestCase as exc:
                raise Exception("You can't use 'break_test_case' outside the Test-Case section") 
                 
            except Exception as exc:                
                self.prereq_passed = False
                self.log = self._explain(
                              exc_name       = sys.exc_info()[0],
                              exc_value      = sys.exc_info()[1],
                              test_hierarchy = test_hierarchy,                             
                              tb             = traceback.format_exc().splitlines()                              
                           )                                   
 
                current.tset.failures = True
                self.failures = True                 
                auto_break = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True                
                                                                            
        if self.events != None and 'before_start' in self.events:                
            try:
                self._events_passed = False
                ev = Event('yoda_events_before_start_ts', self.events['before_start'])        
                if (mh.fire_event(ev) > 0):
                    self.events['before_start'] = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_scenario_node'] = 'events.before_start'
                    if current.te.test_simul_mode == False:                                                        
                        current.te.code_stack.execute(self.events['before_start'], locals())                              
                    else:
                        print("Simulation: Running Test scenario %s yoda_events_before_start_ts " % self.name)
                        compile(self.events['before_start'],'<string>','exec')
                self._events_passed = True 
            except (BreakTestRun, BreakTestSet, BreakTestScenario) as exc:
                self.status = 'break'
                raise exc
            
            except BreakTest as exc:
                raise Exception("You can't use 'break_test' outside the Test-Condition section")
            
            except BreakTestCase as exc:
                raise Exception("You can't use 'break_test_case' outside the Test-Case section") 
                
            except Exception as exc:                                              
                self.log = self._explain(
                                            exc_name       = sys.exc_info()[0],
                                            exc_value      = sys.exc_info()[1],
                                            test_hierarchy = test_hierarchy,                             
                                            tb             = traceback.format_exc().splitlines()                              
                                       )              
                current.tset.failures = True
                self.failures = True
                auto_break = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True                
                                 
        for tca in self.tca:
            run_tca = True
            if current.te.tca_filter is not None and type(current.te.tca_filter).__name__ == 'list' and len(current.te.tca_filter) > 0:
                if tca.id is not None and tca.id != '' and tca.id not in current.te.tca_filter:
                    run_tca = False
            
            if run_tca:
                if self._current.te.have_test_results_db:
                    try:
                        tca.start_time = time.time()                    
                        tca.create_db_record()
                        tca.write_custom_data()
                    except:
                        print(sys.exc_info())
                        ex_type, ex, tb = sys.exc_info()
                        traceback.print_tb(tb)
                        raise Exception('Failed to create test_case database record')
                    
                tca.status     = 'started'                           
                while tca.status != 'finished':
                    if tca.status in ('started','repeat'):
                        try:
                            tca.run()
                        except (BreakTestRun, BreakTestSet, BreakTestScenario) as exc:
                            self.status = 'break'
                            raise exc
                        except BreakTestCase as exc:
                            tca.resolution = 'break'
                            continue
                    elif tca.status == 'break':
                        break;
                #tca finished event here
                tca.resolution = 'completed'
                if self._current.te.have_test_results_db:
                    try:
                        tca.end_time = time.time()                    
                        tca.update_db_record()
                        tca.write_custom_data()
                    except:
                        print(sys.exc_info())
                        raise Exception('Failed to update test_case database record')
            else:
                tca.resolution = 'skipped'
                print("Filter: Skippind test case {0}".format(tca.id))
                                
        if self.action == None:
            self.status = "finished"

        if self.events != None and 'after_finish' in self.events:                
            try:
                self._events_passed = False
                ev = Event('yoda_events_after_finish_ts', self.events['after_finish'])        
                if (mh.fire_event(ev) > 0):
                    self.events['after_finish'] = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_scenario_node'] = 'events.after_finish'
                    if current.te.test_simul_mode == False:                                                        
                        current.te.code_stack.execute(self.events['after_finish'], locals())                              
                    else:
                        print("Simulation: Running Test scenario %s yoda_events_after_finish_ts " % self.name)
                        compile(self.events['after_finish'],'<string>','exec')
                self._events_passed = True 
            except (BreakTestRun, BreakTestSet, BreakTestScenario) as exc:
                self.status = 'break'
                raise exc
            
            except BreakTest as exc:
                raise Exception("You can't use 'break_test' outside the Test-Condition section")
            
            except BreakTestCase as exc:
                raise Exception("You can't use 'break_test_case' outside the Test-Case section") 
                
            except Exception as exc:                                              
                self.log = self._explain(
                                            exc_name       = sys.exc_info()[0],
                                            exc_value      = sys.exc_info()[1],
                                            test_hierarchy = test_hierarchy,                             
                                            tb             = traceback.format_exc().splitlines()                              
                                       )              
                current.tset.failures = True
                self.failures = True
                auto_break = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True
        
        if self.post_req != None:
            try:
                ev = Event('yoda_before_exec_ts_postreq', self.post_req)        
                if (mh.fire_event(ev) > 0):
                    self.post_req = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_scenario_node'] = 'post-req'
                    if current.te.test_simul_mode == False:
                        current.te.code_stack.execute(self.post_req, locals())                                                                                   
                    else:
                        print("Simulation: Running Test scenario %s post-req" % self.name)
                        compile(self.post_req,'<string>','exec')
                self.prereq_passed = True
                
            except (BreakTestRun, BreakTestSet, BreakTestScenario) as exc:
                self.status = 'break'
                raise exc
            
            except BreakTest as exc:
                raise Exception("You can't use 'break_test' outside the Test-Condition section")
            
            except BreakTestCase as exc:
                raise Exception("You can't use 'break_test_case' outside the Test-Case section") 
                 
            except Exception as exc:
                self.postreq_passed = False                    
                self.log = self._explain(
                                            exc_name       = sys.exc_info()[0],
                                            exc_value      = sys.exc_info()[1],
                                            test_hierarchy = test_hierarchy,                             
                                            tb             = traceback.format_exc().splitlines()                              
                                       )              
                current.tset.failures = True
                self.failures = True
                auto_break = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True                 
        
    @property
    def tca(self):
        return self._tca;
    
    @property
    def resolution(self):
        return self._resolution;
    
    @resolution.setter
    def resolution(self,res):
        self._resolution = res
        
    @property
    def status(self):
        return self._status;
    
    @status.setter
    def status(self,status):
        self._status = status

    @property
    def prereq_passed(self):
        return self._prereq_passed;
    
    @prereq_passed.setter
    def prereq_passed(self, status):
        self._prereq_passed = status
        
    @property
    def postreq_passed(self):
        return self._postreq_passed;
    
    @postreq_passed.setter
    def postreq_passed(self, status):
        self._postreq_passed = status                 

    @property
    def events_passed(self):
        return self._events_passed;
    
    @events_passed.setter
    def events_passed(self, status):
        self._events_passed = status    
        
    @property
    def failures(self):
        return self._failures;
    
    @failures.setter
    def failures(self, status):
        if status in (True, False):
            self._failures = status

    @property
    def action(self):
        return self._action;
    
    @action.setter
    def action(self, action):
        self._action = action

    @property
    def total_tests(self):
        return self._total_tests;
    
    @total_tests.setter
    def total_tests(self, total):
        self._total_tests = total

    @property
    def passed_tests(self):
        return self._passed_tests;
    
    @passed_tests.setter
    def passed_tests(self, passed):
        self._passed_tests = passed

    @property
    def failed_tests(self):
        return self._failed_tests;
    
    @failed_tests.setter
    def failed_tests(self, passed):
        self._failed_tests = passed
                
    @property
    def start_time(self):
        return self._start_time;
    
    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time;
    
    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    def break_test_scenario(self, reason):
        self.status                      = 'break' # testc condition break
        raise BreakTestScenario(reason)

    def break_test_set(self, reason):
        self.status                      = 'break' # testc condition break
        self.parent.break_test_set(reason, test_object = self)
                
    def break_test_run(self, reason):
        self.status                      = 'break' # testc condition break        
        self._current.te.test_run.break_test_run(reason)        
    
                                    
class TestCase(TestObject):
    _id             = None
    _num            = None
    _attr           = {}
    _resolution     = None
    _status         = None
    _statuses       = ['started','finished','repeat','break']    
    _tco            = []
    _action         = None
    _failures       = False
    _failed_tco     = 0
    _tco_failures   = None 
    _passed_tco     = 0 
    _parent         = None
    _current        = None
    _start_time     = None
    _end_time       = None
    _events_passed  = None
    _log            = ''
    _struct_log     = {}  
    
    def exec_test(self, test_path):
        self._current.te.exec_test(test_path)
        
    def __init__(self, tca_num, parent_ts, current):
        self._num        = tca_num 
        id_salt          = '{}{}'.format(random.randint(100000000, 999999999),current.te.exec_level)      
        self._id         = hashlib.md5('{0}{1}{2}{3}{4}'.format(current.te.test_run.id, parent_ts.parent.id, parent_ts.id, tca_num, id_salt)).hexdigest()
        self._attr       = {} 
        self._resolution = None
        self._status     = None
        self._statuses   = ['started','finished','repeat','break']
        self._tco        = []    
        self._action     = None          
        self._failures   = False
        self._failed_tco = 0 
        self._passed_tco = 0   
        self._parent     = parent_ts
        self._current    = current 
        self._start_time = 0
        self._end_time   = -1     

    @property
    def id(self):
        return self._attr['id']
    
    @property
    def num(self):
        return self._num

    def create_db_record(self):
        self._current.te.test_results_db.db_action(
                                                   'create_test_case_record',
                                                 [
                                                  self._id,                                                  
                                                  self._attr['id'],
                                                  self._current.te.test_run.id,                                                 
                                                  self._parent.parent.id, #test set
                                                  self._parent.id,        #test scenario                                                 
                                                  self._start_time,
                                                  self._end_time,
                                                  self._total_tests,
                                                  self._failed_tests,
                                                  self._passed_tests,
                                                  self._log,                                                  
                                                  pickle.dumps(self._struct_log)  
                                                ])
           
    
    def update_db_record(self):
        self._current.te.test_results_db.db_action(
                                                   'update_test_case_record',
                                                 {
                                                  'id'               : self._id,                                                  
                                                  'tca_id'           : self._attr['id'],
                                                  'test_run_id'      : self._current.te.test_run.id,
                                                  'test_set_id'      : self._parent.parent.id, 
                                                  'test_scenario_id' : self._parent.id,
                                                  'start_time'       : self._start_time,
                                                  'end_time'         : self._end_time,
                                                  'total_tests'      : self._total_tests,
                                                  'failed_tests'     : self._failed_tests,
                                                  'passed_tests'     : self._passed_tests,
                                                  'log'              : self._log,                                                  
                                                  'struct_log'       : pickle.dumps(self._struct_log)   
                                                })   


    def write_custom_data(self):
        have_filter = 'TestCase' in self._current.te.test_results_db.custom_data_filter
        for key, value in self._attr.items():
            pickled = 0
            if have_filter:
                if key in self._current.te.test_results_db.custom_data_filter['TestCase']:
                    continue
            if type(value).__name__ not in ['int','float','str']:
                value = pickle.dumps(value)
                pickled = 1
            self._current.te.test_results_db.db_action(
                                                   'create_custom_data',
                                                 [
                                                  self._current.te.test_run.id,
                                                  self._id,
                                                  'Test-Case',
                                                  key,
                                                  value,
                                                  pickled                                                                                                    
                                                 ]) 
                
    def run(self):        
       
        '''Define missing locals'''
        this              = self           
        self._current.tca = self
        current           = self._current
        parent            = self._parent
        mh                = MasterHead.get_head()                    
        test_hierarchy    = {
                       'test_set_file'       : this.parent.parent.current_test_set_file,
                       'test_scenario'       : "Test-Scenario-{}".format(parent.num),
                       'test_scenario_node'  : None, 
                       'test_case'           : "Test-Case-{}".format(self._num),
                       'test_case_node'      : None,
                       'test_condition'      : None,
                       'test_condition_node' : None     
                    }                                                   
        if self.events != None and 'before_start' in self.events:                
            try:                
                ev = Event('yoda_events_before_start_tca', self.events['before_start'])        
                if (mh.fire_event(ev) > 0):
                    self.events['before_start'] = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_case_node'] = 'events.before_start'
                    if current.te.test_simul_mode == False:                                                                                                                                       
                        current.te.code_stack.execute(self.events['before_start'], locals())                                                                      
                    else:
                        print("Simulation: Running Test Case %s yoda_events_before_start_tca " % self.name)
                        compile(self.events['before_start'],'<string>','exec')
                        
            except (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase) as exc:
                self.status = 'break'
                raise exc
            
            except BreakTest as exc:
                raise Exception("You can't use 'break_test' outside the Test-Condition section") 
               
            except Exception as exc:                                              
                self.log = self._explain(
                            exc_name       = sys.exc_info()[0],
                            exc_value      = sys.exc_info()[1],
                            test_hierarchy = test_hierarchy,                             
                            tb             = traceback.format_exc().splitlines()                              
                       )
                self._events_passed   = False              
                current.tset.failures = True
                parent.failures       = True
                self.failures         = True
                auto_break            = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True                          
        
                      
        for tco in self.tco:
            run_tco = True
            if current.te.tco_filter is not None and type(current.te.tco_filter).__name__ == 'list' and len(current.te.tco_filter) > 0:
                if tco.id is not None and tco.id != '' and tco.id not in current.te.tco_filter:
                    run_tco = False
            
            if run_tco:
                if current.te.have_test_results_db:
                    try:
                        tco.start_time = time.time()                    
                        tco.create_db_record()
                    except:                        
                        ext, msg, trb = sys.exc_info()
                        print(msg)
                        print repr(traceback.format_tb(trb))
                        raise Exception('Failed to create test_condition database record')
                                                                 
                tco.status     = 'started'                        
                while tco.status != 'finished':
                    if tco.status in ('started','repeat'):
                        try:                        
                            tco.run()
                        except (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase) as exc:
                            self.status = 'break'
                            raise exc
                        except BreakTest as exc:
                            tco.resolution = 'break'
                            continue
                    elif tco.status == 'break':
                        break;
                tco.resolution = 'completed'
                if self._current.te.have_test_results_db:
                    try:
                        tco.end_time = time.time()                    
                        tco.update_db_record()
                        tco.write_custom_data()
                    except:
                        print(sys.exc_info())
                        ex_type, ex, tb = sys.exc_info()
                        traceback.print_tb(tb)
                        raise Exception('Failed to update test_condition database record')
            else:
                tco.resolution = 'skipped'
                print("Filter: Skippind test condition {0}".format(tco.id))    
        if self.action == None:
            self.status = "finished" 

        if self.events != None and 'after_finish' in self.events:                
            try:
                ev = Event('yoda_events_after_finish_tca', self.events['after_finish'])        
                if (mh.fire_event(ev) > 0):
                    self.events['after_finish'] = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_case_node'] = 'events.after_finish'
                    if current.te.test_simul_mode == False:                                                                                                                                       
                        current.te.code_stack.execute(self.events['after_finish'], locals())                                                                      
                    else:
                        print("Simulation: Running Test Case %s yoda_events_after_finish_tca " % self.name)
                        compile(self.events['after_finish'],'<string>','exec')
                        
            except (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase) as exc:
                self.status = 'break'
                raise exc
            
            except BreakTest as exc:
                raise Exception("You can't use 'break_test' outside the Test-Condition section") 
               
            except Exception as exc:                                              
                self.log = self._explain(
                            exc_name       = sys.exc_info()[0],
                            exc_value      = sys.exc_info()[1],
                            test_hierarchy = test_hierarchy,                             
                            tb             = traceback.format_exc().splitlines()                              
                       )
                self._events_passed   = False              
                current.tset.failures = True
                parent.failures       = True
                self.failures         = True
                auto_break            = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True                  

    @property
    def tco(self):
        return self._tco;
    
    @property
    def resolution(self):
        return self._resolution;
    
    @resolution.setter
    def resolution(self,res):
        self._resolution = res
        
    @property
    def status(self):
        return self._status;
    
    @status.setter
    def status(self,status):
        self._status = status

    @property
    def failures(self):
        return self._failures;
    
    @failures.setter
    def failures(self, status):
        if status in (True, False):
            self._failures = status

    @property
    def tco_failures(self):
        return self._tco_failures;
    
    @tco_failures.setter
    def tco_failures(self, status):
        if status in (True, False):
            self._tco_failures = status
                
    @property
    def action(self):
        return self._action;
    
    @action.setter
    def action(self, action):
        self._action = action    

    @property
    def failed_tco(self):
        return self._failed_tco;
    
    @failed_tco.setter
    def failed_tco(self, failed_tco):
        self._failed_tco = failed_tco

    @property
    def passed_tco(self):
        return self._passed_tco;
    
    @passed_tco.setter
    def passed_tco(self, passed_tco):
        self._passed_tco = passed_tco           

    @property
    def start_time(self):
        return self._start_time;
    
    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time;
    
    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time
    
    @property
    def events_passed(self):
        return self._events_passed;
    
    @events_passed.setter
    def events_passed(self, status):
        self._events_passed = status 
                
    def break_test_case(self, reason):
        self.status                      = 'break' # testc condition break
        raise BreakTestCase(reason)
    
    def break_test_set(self, reason):
        self.status                      = 'break' # testc condition break
        self.parent.parent.break_test_set(reason, test_object = self)
                
    def break_test_run(self, reason):
        self.status                      = 'break' # testc condition break        
        self._current.te.test_run.break_test_run(reason)        
        
            
class TestCondition(TestObject):
    _num                  = None
    _id                   = None
    _attr                 = {} 
    _resolution           = None
    _status               = None
    _statuses             = ['started','finished','repeat','break']    
    _action               = None
    _failures             = False
    _expected_result      = None    
    _test_resolution      = None
    _test_result          = None
    _test_output          = ''
    _test_assert          = None
    _test_validate        = None
    _parent               = None
    _current              = None 
    _start_time           = None
    _end_time             = None
    _events_passed        = None
    _test_exec_passed     = None
    _validate_exec_passed = None
    _log                  = ''
    _struct_log           = {}       
    
    def exec_test(self, test_path):
        self._current.te.exec_test(test_path)
        
    def __init__(self, tco_num, parent_tca, current):
        self._num             = tco_num
        id_salt               = '{}{}'.format(random.randint(100000000, 999999999),current.te.exec_level)                    
        self._id              = hashlib.md5('{0}{1}{2}{3}{4}{5}'.format(current.te.test_run.id, parent_tca.parent.parent.id, parent_tca.parent.id, parent_tca.id, tco_num, id_salt)).hexdigest()      
        self._attr            = {} 
        self._resolution      = None
        self._status          = None
        self._statuses        = ['started','finished','repeat','break']    
        self._action          = None       
        self._expected_result = None    
        self._test_resolution = None
        self._test_result     = None
        self._test_output     = ''
        self._test_assert     = None
        self._test_validate   = None
        self._parent          = parent_tca        
        self._current         = current        
        self._start_time      = 0
        self._end_time        = -1   

    @property
    def id(self):
        return self._attr['id']

    def create_db_record(self):        
        self._current.te.test_results_db.db_action(
                                                   'create_test_condition_record',
                                                 [
                                                  self._id,                                                  
                                                  self._attr['id'],
                                                  self._current.te.test_run.id,
                                                  self._parent.parent.parent.id, #test set
                                                  self._parent.parent.id, #test scenario
                                                  self._parent.id,        #test_case
                                                  self._start_time,
                                                  self._end_time,
                                                  self._expected_result,
                                                  self._test_result,
                                                  self._test_resolution,
                                                  self._log,                                                  
                                                  pickle.dumps(self._struct_log)  
                                                ])
                                                    
    def update_db_record(self):        
        self._current.te.test_results_db.db_action(
                                                   'update_test_condition_record',
                                                 {
                                                  'id'               : self._id,                                                  
                                                  'tco_id'           : self._attr['id'],
                                                  'test_run_id'      : self._current.te.test_run.id,
                                                  'test_set_id'      : self._parent.parent.parent.id,
                                                  'test_scenario_id' : self._parent.parent.id,
                                                  'test_case_id'     : self._parent.id,
                                                  'start_time'       : self._start_time,
                                                  'end_time'         : self._end_time,
                                                  'expected_result'  : str(self._expected_result) if self._expected_result is not None else None,
                                                  'test_result'      : self._test_result,
                                                  'test_resolution'  : self._test_resolution.lower(),
                                                  'log'              : self._log,                                                  
                                                  'struct_log'       : pickle.dumps(self._struct_log)   
                                                })   
     
    def write_custom_data(self):
        have_filter = 'TestCondition' in self._current.te.test_results_db.custom_data_filter
        for key, value in self._attr.items():
            pickled = 0
            if have_filter:
                if key in self._current.te.test_results_db.custom_data_filter['TestCondition']:
                    continue
            if type(value).__name__ not in ['int','float','str']:
                value = pickle.dumps(value)
                pickled = 1
            self._current.te.test_results_db.db_action(
                                                   'create_custom_data',
                                                 [
                                                  self._current.te.test_run.id,
                                                  self._id,
                                                  'Test-Condition',
                                                  key,
                                                  value,
                                                  pickled                                                                                                    
                                                 ]) 
                            
    def run(self):                
        '''Define missing locals'''                   
        this              = self
        self._current.tco = self
        current           = self._current
        parent            = self._parent
        mh                = MasterHead.get_head()           
        test_hierarchy    = {
               'test_set_file'       : current.tset.current_test_set_file,
               'test_scenario'       : "Test-Scenario-{}".format(parent.parent.num),
               'test_scenario_node'  : None, 
               'test_case'           : "Test-Case-{}".format(parent.num),
               'test_case_node'      : None,
               'test_condition'      : "Test-Condition-{}".format(self._num),
               'test_condition_node' : None     
        }                      
                        
        test_exception = False
        if self.events != None and 'before_start' in self.events:                                
            try:
                ev = Event('yoda_events_before_start_tco', self.events['before_start'])        
                if (mh.fire_event(ev) > 0):
                    self.events['before_start'] = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_condition_node'] = 'events.before_start'                        
                    if current.te.test_simul_mode == False:                                                                                                  
                        current.te.code_stack.execute(self.events['before_start'], locals())     
                    else:
                        print("Simulation: Running Test Condition %s yoda_events_before_start_tco " % self.name)
                        compile(self.events['before_start'],'<string>','exec')
            
            except (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase, BreakTest) as exc:
                raise exc
                    
            except Exception as exc:                                   
                self.prereq_passed = False
                self.log = self._explain(
                              exc_name       = sys.exc_info()[0],
                              exc_value      = sys.exc_info()[1],
                              test_hierarchy = test_hierarchy,                             
                              tb             = traceback.format_exc().splitlines()                              
                           )                                   
 
                current.tset.failures = True
                current.ts.failures   = True
                parent.tco_failures   = True
                self.failures         = True
                self.events_passed    = False                 
                auto_break = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True       
        
        try:                
            current.te.test_run.total_tests += 1                        
            ev = Event('yoda_before_exec_tco_test', self.test)        
            if (mh.fire_event(ev) > 0):                            
                self.test = ev.argv(0)
            if ev.will_run_default():
                test_hierarchy['test_condition_node'] = 'test' 
                if current.te.test_simul_mode == False:
                    current.ts.total_tests += 1                                                                                                                                                                                       
                    current.te.code_stack.execute(self.test, locals())
                    current.te.test_run.norun_tests -= 1
                    current.te.test_run.run_tests                         
                else:                        
                    print("Simulation: Running Test case: %s, Test condition: %s" % (current.tca.name, self.name))
                    compile(self.test,'<string>','exec')
                    
        except (BreakTestRun,BreakTestSet, BreakTestCase, BreakTest) as exc:
            raise exc
                        
        except Exception as exc:
            test_exception = True                                  
            current.ts.failed_tests +=1
            current.tca.failed_tco += 1
            current.tset.failures   = True
            current.ts.failures  = True
            current.tca.failures = True
            parent.tco_failures = True
            self.log = self._explain(
                         exc_name       = sys.exc_info()[0],
                         exc_value      = sys.exc_info()[1],
                         test_hierarchy = test_hierarchy,                             
                         tb             = traceback.format_exc().splitlines()                              
                      )                                   

            current.tset.failures = True
            self.failures = True
            self.test_exec_passed = False                 
            auto_break = self.get_auto_break()
            break_meth = {
                         'break_test_set' : self.break_test_set,
                         'break_test_run' : self.break_test_run
                         }
            if auto_break in break_meth:
                break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
            self.status = 'break'
            self.action = 'break'         
                                       
        if test_exception == False:                
            try:
                ev = Event('yoda_before_exec_validate_test', self.validate)        
                if (mh.fire_event(ev) > 0):                            
                    self.validate = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_condition_node'] = 'validate' 
                    if current.te.test_simul_mode == False:                                                                                 
                        current.te.code_stack.execute(self.validate, locals())     
                    else:
                        print("Simulation: Validating result, Test case: %s, Test condition: %s" % (current.tca.name, self.name))
                        compile(self.validate,'<string>','exec')                                
                current.ts.passed_tests += 1
                current.tca.passed_tco += 1                            
                self.test_resolution = 'Passed'
                current.te.test_run.passed_tests += 1                    
                tco_note = "*** {ts}/{tca}/{tco}: ".format(ts=current.ts.name,tca=current.tca.name,tco=self.name)
                tco_note = colorize(tco_note, rgb=0x00bfff) + colorize('PASSED',rgb=0x00ff00)
                print(tco_note)                                                    
            
            except (BreakTestRun,BreakTestSet, BreakTestCase, BreakTest) as exc:
                raise exc
                    
            except (AssertionError) as ae:                                               
                current.ts.failed_tests += 1
                current.tca.failed_tco += 1
                current.tset.failures = True
                current.te.test_run.failed_tests += 1                    
                current.ts.failures = True
                current.tca.failures = True
                parent.tco_failures = True
                self.log += bytes(ae)
                self.test_resolution = 'Failed'
                self.expected_result = ae                         
                    
            except Exception as exc:
                test_exception = True
                self.validate_exec_passed = False                        
                current.ts.failed_tests +=1
                current.tca.failed_tco += 1
                current.tset.failures = True
                   
                self.log = self._explain(
                             exc_name       = sys.exc_info()[0],
                             exc_value      = sys.exc_info()[1],
                             test_hierarchy = test_hierarchy,                             
                             tb             = traceback.format_exc().splitlines()                              
                          )                                   
    
                current.tset.failures     = True
                current.ts.failures       = True
                self.failures             = True
                current.tca.tco_failures  = True 
                self.validate_exec_passed = False                       
                auto_break = self.get_auto_break()
                break_meth = {
                             'break_test_set' : self.break_test_set,
                             'break_test_run' : self.break_test_run
                             }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))                      
         
        if self.test_resolution == 'Failed':
            tco_note = "*** {ts}/{tca}/{tco}: ".format(ts=current.ts.name,tca=current.tca.name,tco=self.name)
            tco_note = colorize(tco_note, rgb=0x00bfff) + colorize('FAILED',rgb=0xff0000)
            print(tco_note)              
                                    
        if self.action == None:
            self.status = "finished"
            
        elif self.action == "repeat":
            self.status = "repeat"
            self.action = None
        
        elif self.action == 'break':
            self.status = 'break'
            self.action = None 

        if self.events != None and 'after_finish' in self.events:                                
            try:
                ev = Event('yoda_events_after_finish_tco', self.events['after_finish'])        
                if (mh.fire_event(ev) > 0):
                    self.events['after_finish'] = ev.argv(0)
                if ev.will_run_default():
                    test_hierarchy['test_condition_node'] = 'events.after_finish'                        
                    if current.te.test_simul_mode == False:                                                                                                  
                        current.te.code_stack.execute(self.events['after_finish'], locals())     
                    else:
                        print("Simulation: Running Test Condition %s yoda_events_after_finish_tco " % self.name)
                        compile(self.events['after_finish'],'<string>','exec')
            
            except (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase, BreakTest) as exc:
                raise exc
                    
            except Exception as exc:                                   
                self.prereq_passed = False
                self.log = self._explain(
                              exc_name       = sys.exc_info()[0],
                              exc_value      = sys.exc_info()[1],
                              test_hierarchy = test_hierarchy,                             
                              tb             = traceback.format_exc().splitlines()                              
                           )                                   
 
                current.tset.failures = True
                current.ts.failures   = True
                parent.tco_failures   = True
                self.failures         = True
                self.events_passed    = False                 
                auto_break = self.get_auto_break()
                break_meth = {
                              'break_test_set' : self.break_test_set,
                              'break_test_run' : self.break_test_run
                              }
                if auto_break in break_meth:
                    break_meth[auto_break]("{}: {}".format(sys.exc_info()[0],sys.exc_info()[1]))
                self.status = 'break'
                return True                   
        
    @property
    def resolution(self):
        return self._resolution;
    
    @resolution.setter
    def resolution(self,res):
        self._resolution = res
    
        
    @property
    def status(self):
        return self._status;
    
    @status.setter
    def status(self,status):
        self._status = status   
    
    @property
    def failures(self):
        return self._failures;
    
    @failures.setter
    def failures(self, status):
        if status in (True, False):
            self._failures = status

    @property
    def action(self):
        return self._action;
    
    @action.setter
    def action(self, action):
        self._action = action    
      

    @property
    def expected_result(self):
        return self._expected_result;
    
    @expected_result.setter
    def expected_result(self, result):
        self._expected_result = result
        
    @property
    def test_resolution(self):
        return self._test_resolution;
    
    @test_resolution.setter
    def test_resolution(self, resolution):
        self._test_resolution = resolution     
        
    @property
    def test_result(self):
        return self._test_result;
    
    @test_result.setter
    def test_result(self, result):
        self._test_result = result            
        
    @property
    def test_output(self):
        return self._test_output;
    
    @test_output.setter
    def test_output(self, output):
        self._test_output = output            

    @property
    def test_assert(self):
        return self._test_assert;
    
    @test_assert.setter
    def test_assert(self, result):
        self._test_assert = result
        
    @property
    def test_validate(self):
        return self._test_validate;
    
    @test_validate.setter
    def test_validate(self, result):
        self._test_validate = result                    

    @property
    def start_time(self):
        return self._start_time;
    
    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time;
    
    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time
    
    @property
    def events_passed(self):
        return self._events_passed;
    
    @events_passed.setter
    def events_passed(self, status):
        self._events_passed = status

    @property
    def test_exec_passed(self):
        return self._test_exec_passed;
    
    @test_exec_passed.setter
    def test_exec_passed(self, status):
        self._test_exec_passed = status

    @property
    def validate_exec_passed(self):
        return self._validate_exec_passed;
    
    @validate_exec_passed.setter
    def validate_exec_passed(self, status):
        self._validate_exec_passed = status
                            
    def break_test(self, reason):
        self.status = 'break'
        raise BreakTest(reason)
    
    def break_test_case(self, reason):
        self.status                      = 'break' # testc condition break
        self.parent.break_test_case(reason)
    
    def break_test_scenario(self, reason):
        self.status                      = 'break' # testc condition break        
        self.parent.parent.break_test_scenario(reason)
    
    def break_test_set(self, reason):
        self.status                      = 'break' # testc condition break
        self.parent.parent.parent.break_test_set(reason)
                
    def break_test_run(self, reason):
        self.status                      = 'break' # testc condition break        
        self._current.te.test_run.break_test_run(reason)        

        