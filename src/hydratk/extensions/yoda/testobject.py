# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

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
        self.total_test_sets        = 0;
        self.total_tests            = 0;
        self.failed_tests           = 0;
        self.passed_tests           = 0;
        self.failures               = False;
        self.start_time             = None;
        self.end_time               = None;
        self.tset                   = [];
    
    def reset_data(self):
        self.total_test_sets        = 0;
        self.total_tests            = 0;
        self.failed_tests           = 0;
        self.passed_tests           = 0;
        self.failures               = False;
        self.start_time             = None;
        self.end_time               = None;
        self.tset                   = [];
        
    def __repr__(self):
        return ( """
                 total_test_sets = {0}\n
                 total_tests     = {1};
                 failed_tests    = {2};
                 passed_tests    = {3};
                 failures        = {4};
                 start_time      = {5};
                 end_time        = {6};
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
        self.current_test_base_path  = None;
        self.current_test_set_file   = None;
        self.total_tests             = 0;
        self.failed_tests            = 0;
        self.passed_tests            = 0;
        self.failed_ts               = 0;
        self.passed_ts               = 0;
        self.failures                = False;
        self.start_time              = None;
        self.end_time                = None;
        self.ts                      = []; '''Test Scenarios'''
    
    def reset_data(self):
        self.current_test_base_path  = None;
        self.current_test_set_file   = None;
        self.total_tests             = 0;
        self.failed_tests            = 0;
        self.passed_tests            = 0;
        self.failed_ts               = 0;
        self.passed_ts               = 0;
        self.failures                = False;
        self.start_time              = None;
        self.end_time                = None;
        self.ts                      = []; '''Test Scenarios'''
        
class TestScenario():
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
        self._id             = ts_id;
        self.path            = None;
        self.name            = None;
        self.desc            = None;
        self.author          = None;
        self.version         = None;
        self.total_tests     = 0;
        self.failed_tests    = 0;
        self.passed_tests    = 0;
        self.failures        = False;
        self.tca             = []; '''Test Cases'''
        self.prereq_passed   = None;
        self.test_log        = '';
        self.start_time      = None;
        self.end_time        = None;
    
    def reset(self):
        self._id             = None;
        self.path            = None;
        self.name            = None;
        self.desc            = None;
        self.author          = None;
        self.version         = None;
        self.total_tests     = 0;
        self.failed_tests    = 0;
        self.passed_tests    = 0;
        self.failures        = False;
        self.tca             = []; '''Test Cases'''
        self.prereq_passed   = None;
        self.test_log        = '';
        self.start_time      = None;
        self.end_time        = None;
        
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
        self._id         = tca_id;
        self.name        = None; 
        self.desc        = None;
        self.failures    = False;
        self.failed_tco  = 0;
        self.passed_tco  = 0;
        self.tco         = []; '''Test Conditions'''
        self.start_time  = None;
        self.end_time    = None;
    
    def reset(self):
        self._id         = None;
        self.name        = None; 
        self.desc        = None;
        self.failures    = False;
        self.failed_tco  = 0;
        self.passed_tco  = 0;
        self.tco         = []; '''Test Conditions'''
        self.start_time  = None;
        self.end_time    = None;

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
        self.name            = None;
        self.desc            = None;
        self.expected_result = None;    
        self.test_resolution = False;
        self.test_result     = None;
        self.test_output     = '';
        self.test_assert     = None;
        self.test_validate   = None;
        self.test_log        = '';
        self.start_time      = None;
        self.end_time        = None; 

    def reset(self):
        self._id             = None;
        self.name            = None;
        self.desc            = None;
        self.expected_result = None;    
        self.test_resolution = False;
        self.test_result     = None;
        self.test_output     = '';
        self.test_assert     = None;
        self.test_validate   = None;
        self.test_log        = '';
        self.start_time      = None;
        self.end_time        = None; 
