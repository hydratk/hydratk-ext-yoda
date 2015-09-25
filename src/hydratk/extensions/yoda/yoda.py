# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: hydratk.extensions.yoda.yoda
   :platform: Unix
   :synopsis: Providing automated testing functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

events = {  
  'yoda_before_start'          : 'hydra.extensions.yoda.yoda',  '''yoda_onbefore_start'''
  'yoda_on_start'                : 'hydra.extensions.yoda.yoda',  '''yoda_on_start'''
  'yoda_on_stop'                 : 'hydra.extensions.yoda.yoda'  '''yoda_on_stop''' 
};

import os;
import yaml;
import traceback;
import sys;
import pprint;
import traceback;
from hydratk.core import extension;
from hydratk.core import const;
from hydra.translation import messages;
from hydratk.lib.console.commandlinetool import CommandlineTool;
from hydratk.lib.console.commandlinetool import rprint;
from hydratk.extensions.yoda.testobject import TestRun;
from hydratk.extensions.yoda.testobject import TestSet;
from hydratk.extensions.yoda.testobject import TestScenario;
from hydratk.extensions.yoda.testobject import TestCase;
from hydratk.extensions.yoda.testobject import TestCondition;

class Extension(extension.Extension):
    _test_repo              = None;
    _test_run               = None;    
    
    def _init_extension(self):
        self._ext_name = 'Yoda';
        self._ext_version = '0.1.0';
        self._ext_author = 'Petr Czaderna <pc@hydratk.org>';
        self._ext_year = '2014 - 2015';  
        
    def _check_dependencies(self):
        return True;
    
    def _do_imports(self):
        pass
        
    def _export_messages(self): 
        messages.help_cmd['cs']['run-yoda'] = 'spustí yoda tester';
        messages.help_cmd['en']['run-yoda'] = 'starts the yoda tester';                
        messages.help_opt['cs']['test-path']  = { '{h}--test-path <cesta>{e}' : { 'description' : 'cesta k testovacímu scénáři', 'commands' : ('run-yoda')}};
        messages.help_opt['en']['test-path']  = { '{h}--test-path <path>{e}' :  { 'description' : 'test scenario path', 'commands' : ('run-yoda')}};
        pass        
        
    def _register_actions(self):               
        hook = [{'event' : 'h_on_cmd_options', 'callback' : self.init_check }];        
        self._mh.register_event_hook(hook);

        self._mh.match_command('run-yoda');        
        hook = [{'command' : 'run-yoda', 'callback' : self.init_tests }];        
        self._mh.register_command_hook(hook);
        self._mh.match_long_option('test-path',True);             

    def init_check(self, oevent):        
        pass
    
    """Method returs all found test in path
           
           Test files are filtered by .yoda file extension
        
        Args:
           test_path (str): test path
        
        Returns:            
           test_files (list)
                  
        """           
    def get_all_tests_from_path(self, test_path):
        test_files = [];        
        root_dir = test_path;
        for dirname, _, filelist in os.walk(root_dir): # subdir_list not used            
            for fname in filelist:
                if fname.split('.')[1] == 'yoda':
                    test_files.append(dirname + '/' + fname)
        return test_files; 
         
    def init_tests(self):
        test_path = CommandlineTool.get_input_option('--test-path');
        self._mh.dmsg('h_on_debug_info', "Running test %s" % test_path, self._mh.fromhere());        
        self.init_helpers();
        self._test_run = TestRun();
        if os.path.exists(self._mh.cfg['Extensions']['Yoda']['test_repo_root']):
            self._test_repo = self._mh.cfg['Extensions']['Yoda']['test_repo_root'];
            self._current_test_base_path = self._test_repo + '/templates/' + test_path;
            if os.path.exists(self._current_test_base_path):
                test_files = self.get_all_tests_from_path(self._current_test_base_path);
                self.process_tests(test_files);
                self.check_results(self._test_run);  
            else:
                print("invalid test base path %s" % self._current_test_base_path )
        else:
            print("invalid test repo root %s" % self._mh.cfg['Extensions']['Yoda']['test_repo_root'])
    
    def init_helpers(self):
        helpers_root_dir = self._mh.cfg['Extensions']['Yoda']['test_repo_root'] + '/helpers';
        if os.path.exists(helpers_root_dir):
            sys.path.append(helpers_root_dir);
            print('Using helpers in %s' % (helpers_root_dir))
        else:
            self.dmsg('h_on_debug_info', 'Helpers not properly configured, skipping', self.fromhere());                             
         
    def process_tests(self, test_files):
        total_ts = len(test_files);
        if total_ts > 0:
            self._test_run.total_test_sets = total_ts;
            print('Found %d test sets' % total_ts);
            for tf in test_files:
                self.parse_test(tf);
        else:
            print('No tests found in specified path')
            
    def parse_test(self, test_file):
        try:
            with open(test_file, 'r') as f:                    
                testobj = yaml.load(f)                                                            
                self._mh.dmsg('h_on_debug_info', 'Processing test set ' + test_file, self._mh.fromhere()); 
                #pprint.pprint(testobj)
                test_set = TestSet();
                test_set.current_test_base_path = os.path.dirname(test_file);
                test_set.current_test_set_file = test_file;
                self.exec_test_set(testobj, test_set);
                #pprint.pprint(test_set.ts);
                self._test_run.tset.append(test_set);                
                             
        except Exception as detail:
            print('except here')
            print(detail);
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
            sys.exit(1);
    
    def exec_test_set(self,testobj, test_set):                
        ts_num = 1;
        ts_k = 'Test-Scenario-%d' % ts_num;
        while ts_k in testobj:            
            test_scenario = TestScenario(ts_num);
            test_scenario.path    = testobj[ts_k]['Path'] if 'Path' in testobj[ts_k] else None;
            test_scenario.name    = testobj[ts_k]['Name'] if 'Name' in testobj[ts_k] else None;
            test_scenario.desc    = testobj[ts_k]['Desc'] if 'Desc' in testobj[ts_k] else None;
            test_scenario.author  = testobj[ts_k]['Author'] if 'Author' in testobj[ts_k] else None;
            test_scenario.version = testobj[ts_k]['Version'] if 'Version' in testobj[ts_k] else None;            
            if 'Pre-Req' in testobj[ts_k]:
                try:
                    exec(testobj[ts_k]['Pre-Req'],globals(),locals());
                    test_scenario.prereq_passed = True;
                except Exception as exc:
                    test_scenario.prereq_passed = False;                    
                    exc_info = sys.exc_info();
                    test_scenario.test_log += "Exception: %s\n" % exc_info[0];
                    test_scenario.test_log += "Value: %s\n" % str(exc_info[1]);
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = '';
                    for line in formatted_lines:
                        trace += "%s\n" % str(line);
                    test_scenario.test_log += trace;
                    test_set.failures = True;
                    test_scenario.failures = True;                  
                    test_set.ts.append(test_scenario);
                    break; 
            tca_num = 1;
            tca_k = 'Test-Case-%d' % tca_num;
            while tca_k in testobj[ts_k]:
                test_case      = TestCase(tca_num);
                test_case.name = testobj[ts_k][tca_k]['Name'] if 'Name' in testobj[ts_k][tca_k] else None;
                test_case.desc = testobj[ts_k][tca_k]['Desc'] if 'Desc' in testobj[ts_k][tca_k] else None;                
                tco_num = 1;
                tco_k = 'Test-Condition-%d' % tco_num;
                while tco_k in testobj[ts_k][tca_k]:
                    test_exception = False;
                    test_condition = TestCondition(tco_num);
                    test_condition.name = testobj[ts_k][tca_k][tco_k]['Name'] if 'Name' in testobj[ts_k][tca_k][tco_k] else None;
                    test_condition.desc = testobj[ts_k][tca_k][tco_k]['Desc'] if 'Desc' in testobj[ts_k][tca_k][tco_k] else None;
                    test_condition.expected_result = testobj[ts_k][tca_k][tco_k]['Validate'];                    
                    try:
                        exec(testobj[ts_k][tca_k][tco_k]['Test'],globals(),locals());
                    except Exception as exc:
                        exc_info = sys.exc_info();
                        test_condition.test_log += "Exception: %s\n" % exc_info[0];
                        test_condition.test_log += "Value: %s\n" % str(exc_info[1]);
                        formatted_lines = traceback.format_exc().splitlines()
                        trace = '';
                        for line in formatted_lines:
                            trace += "%s\n" % str(line);
                        test_condition.test_log += trace;
                        test_exception = True;
                        test_condition.test_resolution = 'Failed';
                        test_scenario.total_tests += 1;
                        test_scenario.failed_tests +=1;
                        test_case.failed_tco += 1;
                        test_set.failures = True;
                    if test_exception == False:
                        try:
                            exec(testobj[ts_k][tca_k][tco_k]['Validate'],globals(),locals());
                            test_scenario.passed_tests += 1;
                            test_case.passed_tco += 1;
                            test_condition.test_resolution = 'Passed';
                        except (AssertionError, Exception) as ae:                            
                            test_scenario.failed_tests +=1;
                            test_case.failed_tco += 1;
                            test_set.failures = True;
                            test_scenario.failures = True;
                            test_case.failures = True;
                            test_condition.test_log += bytes(ae);
                            test_condition.test_resolution = 'Failed';
                                                     
                    test_case.tco.append(test_condition);                                       
                    tco_num += 1;
                    tco_k = 'Test-Condition-%d' % tco_num;
                test_scenario.tca.append(test_case);                    
                tca_num += 1;
                tca_k = 'Test-Case-%d' % tca_num;
            if 'Post-Req' in testobj[ts_k]:
                try:                    
                    exec(testobj[ts_k]['Post-Req'],globals(),locals());
                except Exception as exc:
                    exc_info = sys.exc_info();
                    test_condition.test_log += "Exception: %s\n" % exc_info[0];
                    test_condition.test_log += "Value: %s\n" % str(exc_info[1]);
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = '';
                    for line in formatted_lines:
                        trace += "%s\n" % str(line);
                    test_condition.test_log += trace;
                    test_exception = True;
                                        
            test_set.ts.append(test_scenario);     
            ts_num += 1;
            ts_k = 'Test-Scenario-%d' % ts_num;        
    
    def check_results(self, test_run):        
        for test_set in test_run.tset:        
            for ts in test_set.ts:                
                print("Test Scenario: %s, tests - total: %d, failed: %d, passed: %d" % (ts.name,ts.total_tests, ts.failed_tests,ts.passed_tests));
                if ts.failures == True:
                    if ts.prereq_passed in (True,None):
                        if ts.prereq_passed == True: print("Pre-requirements passed successfully"); 
                        for tca in ts.tca:
                            if tca.failed_tco > 0:
                                print(" Test Case: %s" % (tca.name));
                                for tco in tca.tco:
                                    if tco.test_resolution == 'Failed':
                                        print("  Test Condition: %s" % (tco.name));
                                        print("    Expected Result: %s" % str(tco.expected_result).strip());
                                        print("    Actual Result: %s" % str(tco.test_result));
                                        print("    Log: %s" % str(tco.test_log));
                    else:
                        print(" Pre-requirements failed in:");
                        print("   %s" % ts.test_log);