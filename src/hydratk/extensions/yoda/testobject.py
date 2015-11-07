# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: hydratk.extensions.yoda.testobject
   :platform: Unix
   :synopsis: Providing automated testing functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

class TestRun():
    _total_test_sets        = 0
    _total_tests            = 0
    _failed_tests           = 0
    _passed_tests           = 0
    _failures               = False
    _start_time             = None
    _end_time               = None
    '''Test Sets'''
    _tset                    = [] 
    
    def __init__(self):
        self._total_test_sets        = 0
        self._total_tests            = 0
        self._failed_tests           = 0
        self._passed_tests           = 0
        self._failures               = False
        self._start_time             = None
        self._end_time               = None
        self._tset                   = []
    
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
    def failures(self):
        return self._passed_tests
    
    @failures.setter
    def failures(self, total):
        self._failures = total  

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

         
class TestSet():
    _current_test_base_path  = 'xxxx'
    _current_test_set_file   = 'ffff'
    _total_tests             = 0
    _failed_tests            = 0
    _passed_tests            = 0
    _failed_ts               = 0
    _passed_ts               = 0
    _failures                = False
    _start_time              = None
    _end_time                = None
    '''Test Scenarios'''
    _ts                     = []         


    @property
    def current_test_base_path(self):
        return self._current_test_base_path
    
    @current_test_base_path.setter
    def current_test_base_path(self, path):
        self._current_test_base_path = path        

   
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
    
    def __init__(self):
        self._current_test_base_path  = None
        self._current_test_set_file   = None
        self._total_tests             = 0
        self._failed_tests            = 0
        self._passed_tests            = 0
        self._failed_ts               = 0
        self._passed_ts               = 0
        self._failures                = False
        self._start_time              = None
        self._end_time                = None
        '''Test Scenarios'''
        self._ts                      = [] 
    
    
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
        
class TestScenario():
    _num            = None
    _attr           = {}
    _tca            = []
    _status         = None
    _statuses       = ['started','finished','repeat','break']
    _action         = None
    _prereq_passed  = None
    _test_log       = ''
    _failures       = False       
    _total_tests    = 0
    _failed_tests   = 0
    _passed_tests   = 0        
    _start_time     = None
    _end_time       = None

    
    def __init__(self, ts_num):
        self._num            = ts_num
        self._id             = None
        self._attr           = {}
        self._tca            = [] 
        self._status         = None
        self._statuses       = ['started','finished','repeat','break']    
        self._action         = None              
        self._prereq_passed  = None
        self._test_log       = ''
        self._failures       = False       
        self._total_tests    = 0
        self._failed_tests   = 0
        self._passed_tests   = 0        
        self._start_time     = None
        self._end_time       = None
    
        
    def append_tca(self, tca):
        if isinstance(tca, TestCase):
            self._tca.append(tca)
                
    def setattr(self,key,val):
        if key != '':
            key = key.replace('-','_')
            self._attr[key]  = val
    
    def __getattr__(self,name):        
        result = None
        if name in self._attr:
            result = self._attr[name]
        return result
        
    @property
    def tca(self):
        return self._tca;
    
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
    def test_log(self):
        return self._test_log;
    
    @test_log.setter
    def test_log(self, msg):
        self._test_log = msg

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
        self._passed_tests = passed
                
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

                                    
class TestCase():
    _num            = None
    _attr           = {}
    _status         = None
    _statuses       = ['started','finished','repeat','break']    
    _tco            = []
    _action         = None
    _test_log       = ''
    _failures       = False
    _failed_tco     = 0 
    _passed_tco     = 0   
    
    def __init__(self, tca_num):
        self._num        = tca_num
        self._id         = None
        self._attr       = {} 
        self._status     = None
        self._statuses   = ['started','finished','repeat','break']
        self._tco        = []    
        self._action     = None  
        self._test_log   = ''
        self._failures   = False
        self._failed_tco = 0 
        self._passed_tco = 0         
       
    
    def append_tco(self, tco):
        if isinstance(tco, TestCondition):
            self._tco.append(tco)
            
    def setattr(self,key,val):
        if key != '':
            key = key.replace('-','_')
            self._attr[key] = val
            
    def __getattr__(self,name):        
        result = None
        if name in self._attr:
            result = self._attr[name]
        return result

    @property
    def tco(self):
        return self._tco;
    
    @property
    def status(self):
        return self._status;
    
    @status.setter
    def status(self,status):
        self._status = status
 
    @property
    def test_log(self):
        return self._test_log;
    
    @test_log.setter
    def test_log(self, msg):
        self._test_log = msg

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
    
class TestCondition():
    _num             = None
    _id              = None
    _attr            = {} 
    _status          = None
    _statuses        = ['started','finished','repeat','break']    
    _action          = None
    _test_log        = ''
    _failures        = False
    _expected_result = None    
    _test_resolution = False
    _test_result     = None
    _test_output     = ''
    _test_assert     = None
    _test_validate   = None       
    
    def __init__(self, tco_num):
        self._num             = tco_num
        self._id              = None
        self._attr            = {} 
        self._status          = None
        self._statuses        = ['started','finished','repeat','break']    
        self._action          = None
        self._test_log        = ''
        self._failures        = False
        self._expected_result = None    
        self._test_resolution = False
        self._test_result     = None
        self._test_output     = ''
        self._test_assert     = None
        self._test_validate   = None   
    
    def setattr(self,key,val):
        if key != '':
            key = key.replace('-','_')
            self._attr[key] = val
    
            
    def __getattr__(self,name):        
        result = None
        if name in self._attr:
            result = self._attr[name]
        return result
        
    @property
    def status(self):
        return self._status;
    
    @status.setter
    def status(self,status):
        self._status = status   
    
    @property
    def test_log(self):
        return self._test_log;
    
    @test_log.setter
    def test_log(self, msg):
        self._test_log = msg

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


