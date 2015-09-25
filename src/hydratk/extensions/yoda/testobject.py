# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit (HydraTK)

.. module:: hydratk.extensions.yoda.testobject
   :platform: Unix
   :synopsis: Providing automated testing functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

class TestRun():
    total_test_sets        = 0;
    total_tests            = 0;
    failed_tests           = 0;
    passed_tests           = 0;
    failures               = False;
    start_time             = None;
    end_time               = None;
    tset                   = []; '''Test Sets'''
    
    def __init__(self):
        pass
    
    def reset_data(self):
        self.current_test_base_path = None;
        self.total_test_sets        = 0;
        self.total_tests            = 0;
        self.failed_tests           = 0;
        self.passed_tests           = 0;
        self.start_time             = None;
        self.end_time               = None;
        self.ts                          = [];
        
class TestSet():
    current_test_base_path  = None;
    current_test_set_file   = None;
    total_tests             = 0;
    failed_tests            = 0;
    passed_tests            = 0;
    failed_ts               = 0;
    passed_ts               = 0;
    failures                = False;
    start_time              = None;
    end_time                = None;
    ts                      = []; '''Test Scenarios'''
    
    
    def __init__(self):
        pass
        
class TestScenario(object):
    _id             = None;
    path            = None;
    name            = None;
    desc            = None;
    author          = None;
    version         = None;
    total_tests     = 0;
    failed_tests    = 0;
    passed_tests    = 0;
    failures        = False;
    tca             = []; '''Test Cases'''
    prereq_passed   = None;
    test_log        = '';
    start_time      = None;
    end_time        = None;

    def __init__(self, ts_id):
        self._id = ts_id;
          
        
class TestCase():
    _id             = None;
    name            = None; 
    desc            = None;
    failures        = False;
    failed_tco      = 0;
    passed_tco      = 0;
    tco             = []; '''Test Conditions'''
    start_time      = None;
    end_time        = None;
    
    def __init__(self, tca_id):
        self._id = tca_id;

class TestCondition():
    _id             = None;
    name            = None;
    desc            = None;
    expected_result = None;    
    test_resolution = False;
    test_result     = None;
    test_output     = '';
    test_assert     = None;
    test_validate   = None;
    test_log        = '';
    start_time      = None;
    end_time        = None;  
    
    def __init__(self, tco_id):
        self._id = tco_id;

