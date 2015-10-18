# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: hydratk.extensions.yoda.yoda
   :platform: Unix
   :synopsis: Providing automated testing functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

"""
Events:
-------
yoda_before_init_tests
yoda_before_append_test_file
yoda_before_process_tests
yoda_before_check_results
yoda_before_append_helpers_dir
yoda_before_parse_test_file
yoda_before_exec_ts_prereq
yoda_before_exec_tco_test
yoda_before_exec_validate_test
yoda_before_exec_ts_postreq

"""
import os;
import yaml;
import traceback;
import sys;
from hydratk.core import extension;
from hydratk.core import event;
from hydratk.lib.console.commandlinetool import CommandlineTool;
from hydratk.lib.console.commandlinetool import rprint;
from hydratk.extensions.yoda.testobject import TestRun;
from hydratk.extensions.yoda.testobject import TestSet;
from hydratk.extensions.yoda.testobject import TestScenario;
from hydratk.extensions.yoda.testobject import TestCase;
from hydratk.extensions.yoda.testobject import TestCondition;

class Extension(extension.Extension):
    _test_repo_root         = None;
    _templates_repo         = None;
    _helpers_repo           = None;
    _test_run               = None;
    _current_test_base_path = None; 
    _use_helpers_dir        = [];   
    
    def _init_extension(self):
        self._ext_name    = 'Yoda';
        self._ext_version = '0.1.1';
        self._ext_author  = 'Petr Czaderna <pc@hydratk.org>';
        self._ext_year    = '2014 - 2015';
        
        self._init_repos();  
        
    def _check_dependencies(self):
        return True;
    
    def _init_repos(self):
        self._test_repo_root = self._mh.cfg['Extensions']['Yoda']['test_repo_root'];
        self._templates_repo = self._mh.cfg['Extensions']['Yoda']['test_repo_root'] + '/templates';
        self._helpers_repo   = self._mh.cfg['Extensions']['Yoda']['test_repo_root'] + '/helpers';
        
    def _do_imports(self):
        pass                 
        
    def _register_actions(self):               
        hook = [{'event' : 'htk_on_cmd_options', 'callback' : self.init_check }];        
        self._mh.register_event_hook(hook);

        self._mh.match_command('yoda-run');        
        hook = [{'command' : 'yoda-run', 'callback' : self.init_tests }];        
        self._mh.register_command_hook(hook);
        
        self._mh.match_long_option('yoda-test-path',True);
        self._mh.match_long_option('yoda-test-repo-root-dir',True);                 
    
    def init_check(self, ev):
        """Event listener waiting for htk_on_cmd_options event
           
           If there's --yoda-test-repo-root-dir parameter presence, it will try to override current settings
        
        Args:
           ev (object): hydratk.core.event.Event
        
        """     
        test_repo = CommandlineTool.get_input_option('yoda-test-repo-root-dir');
        if isinstance(test_repo, str) and test_repo != '':
            self._test_repo_root = test_repo;    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_test_repo_root_override',test_repo), self._mh.fromhere());
          
    def get_all_tests_from_path(self, test_path):
        """Method returs all found test in path
           
           Test files are filtered by .yoda file extension
        
        Args:
           test_path (str): test path
        
        Returns:            
           test_files (list)
                  
        """     
        test_files = [];        
        root_dir = test_path;
        for dirname, _, filelist in os.walk(root_dir): # subdir_list not used            
            for fname in filelist:
                if fname.split('.')[1] == 'yoda':
                    test_file = dirname + '/' + fname;
                    ev = event.Event('yoda_before_append_test_file', test_file);        
                    if (self._mh.fire_event(ev) > 0):
                        test_file = ev.argv(0);
                    if ev.will_run_default():
                        test_files.append(test_file)
        return test_files; 
         
    def init_tests(self):
        """Method is initializing tests           
                  
        """
        ev = event.Event('yoda_before_init_tests');        
        self._mh.fire_event(ev);                    
        if ev.will_run_default():     
            test_path = CommandlineTool.get_input_option('--yoda-test-path');
            test_path = test_path if isinstance(test_path, str) else '';                        
            self.init_helpers();
            self._test_run = TestRun();
            if os.path.exists(self._test_repo_root):            
                self._current_test_base_path = self._templates_repo + test_path;
                if os.path.exists(self._current_test_base_path):                
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_start_test_from', self._current_test_base_path), self._mh.fromhere());
                    test_files = self.get_all_tests_from_path(self._current_test_base_path);                
                    ev = event.Event('yoda_before_process_tests', test_files);        
                    if (self._mh.fire_event(ev) > 0):
                        test_files = ev.argv(0);
                    if ev.will_run_default():
                        self.process_tests(test_files);
                    ev = event.Event('yoda_before_check_results', self._test_run);        
                    if (self._mh.fire_event(ev) > 0):                   
                        self._test_run = ev.argv(0);
                    if ev.will_run_default():    
                        self.check_results(self._test_run);  
                else:
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('yoda_invalid_test_base_path', self._current_test_base_path), self._mh.fromhere());                
            else:           
                self._mh.dmsg('htk_on_error', self._mh._trn.msg(' yoda_invalid_test_repo_root', self._test_repo_root), self._mh.fromhere());            
    
    def init_helpers(self):        
        """ Add default helpers repo directory"""
        self._use_helpers_dir.append(self._helpers_repo);  
        ev = event.Event('yoda_before_append_helpers_dir', self._use_helpers_dir);        
        if (self._mh.fire_event(ev) > 0):
            self._use_helpers_dir = ev.argv(0);
        if ev.will_run_default():
            if isinstance(self._use_helpers_dir, list):
                for helpers_dir in self._use_helpers_dir:    
                    if os.path.exists(helpers_dir):
                        sys.path.append(helpers_dir);                         
                        self._mh.dmsg('htk_on_debug_info',self._mh._trn.msg('yoda_added_helpers_dir', helpers_dir), self._mh.fromhere());                        
                    else:
                        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_helpers_dir_not_exists', helpers_dir), self._mh.fromhere());                             
         
    def process_tests(self, test_files):
        total_ts = len(test_files);
        if total_ts > 0:
            self._test_run.total_test_sets = total_ts;
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_process_test_sets_total', total_ts), self._mh.fromhere());            
            for tf in test_files:
                ev = event.Event('yoda_before_parse_test_file', tf);        
                if (self._mh.fire_event(ev) > 0):
                    tf = ev.argv(0);
                if ev.will_run_default():
                    self.parse_test_file(tf);
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_no_tests_found_in_path', self._current_test_base_path), self._mh.fromhere());
            
    def parse_test_file(self, test_file):        
        try:
            with open(test_file, 'r') as f:                    
                testobj = yaml.load(f)    
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_process_test_set', test_file), self._mh.fromhere());                                
                test_set = TestSet();                               
                test_set.current_test_base_path = os.path.dirname(test_file);
                test_set.current_test_set_file = test_file;
                ev = event.Event('yoda_before_exec_test_set', testobj, test_set);        
                if (self._mh.fire_event(ev) > 0):                    
                    testobj  = ev.argv(0);
                    test_set = ev.argv(1);
                if ev.will_run_default():                    
                    self.exec_test_set(testobj, test_set);               
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
                    ev = event.Event('yoda_before_exec_ts_prereq', testobj[ts_k]['Pre-Req']);        
                    if (self._mh.fire_event(ev) > 0):
                        testobj[ts_k]['Pre-Req'] = ev.argv(0);
                    if ev.will_run_default():
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
                    test_scenario.total_tests += 1;                    
                    try:
                        self._test_run.total_tests += 1;                        
                        ev = event.Event('yoda_before_exec_tco_test', testobj[ts_k][tca_k][tco_k]['Test']);        
                        if (self._mh.fire_event(ev) > 0):                            
                            testobj[ts_k][tca_k][tco_k]['Test'] = ev.argv(0);
                        if ev.will_run_default():
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
                        test_scenario.failed_tests +=1;
                        test_case.failed_tco += 1;
                        test_set.failures = True;
                    if test_exception == False:
                        try:
                            ev = event.Event('yoda_before_exec_validate_test', testobj[ts_k][tca_k][tco_k]['Validate']);        
                            if (self._mh.fire_event(ev) > 0):                            
                                testobj[ts_k][tca_k][tco_k]['Validate'] = ev.argv(0);
                            if ev.will_run_default():
                                exec(testobj[ts_k][tca_k][tco_k]['Validate'],globals(),locals());
                            test_scenario.passed_tests += 1;
                            test_case.passed_tco += 1;                            
                            test_condition.test_resolution = 'Passed';
                            self._test_run.passed_tests += 1;
                        except (AssertionError, Exception) as ae:                            
                            test_scenario.failed_tests += 1;
                            test_case.failed_tco += 1;
                            test_set.failures = True;
                            self._test_run.failed_tests += 1
                            test_scenario.failures = True;
                            test_case.failures = True;
                            test_condition.test_log += bytes(ae);
                            test_condition.test_resolution = 'Failed';
                            test_condition.expected_result = ae;                                                     
                    test_case.tco.append(test_condition);                                                          
                    tco_num += 1;
                    tco_k = 'Test-Condition-%d' % tco_num;
                test_scenario.tca.append(test_case);                                   
                tca_num = tca_num + 1;
                tca_k = 'Test-Case-%d' % tca_num;
            if 'Post-Req' in testobj[ts_k]:
                try:
                    ev = event.Event('yoda_before_exec_ts_postreq', testobj[ts_k]['Post-Req']);        
                    if (self._mh.fire_event(ev) > 0):                        
                        testobj[ts_k]['Post-Req'] = ev.argv(0);
                    if ev.will_run_default():                    
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
        print(self._mh._trn.msg('yoda_test_run_summary', test_run.total_test_sets, test_run.total_tests, test_run.failed_tests, test_run.passed_tests));                        
        for test_set in test_run.tset:
            print("  {0}".format(self._mh._trn.msg('yoda_test_set_summary', test_set.current_test_set_file)));                           
            for ts in test_set.ts:
                print("    {0}".format(self._mh._trn.msg('yoda_test_scenario_summary', ts.name,ts.total_tests, ts.failed_tests,ts.passed_tests)));                                                                
                if ts.failures == True:
                    if ts.prereq_passed in (True,None):                        
                        if ts.prereq_passed == True: print("      {0}".format(self._mh._trn.msg('yoda_test_scenario_prereq_passed')));                         
                        for tca in ts.tca:
                            if tca.failed_tco > 0:
                                print("      {0}".format(self._mh._trn.msg('yoda_test_case',tca.name)));                                                           
                                for tco in tca.tco:
                                    if tco.test_resolution == 'Failed':
                                        print("        {0}".format(self._mh._trn.msg('yoda_test_condition',tco.name)));
                                        print("            {}".format(self._mh._trn.msg('yoda_expected_result',str(tco.expected_result).strip())));                                        
                                        print("            {}".format(self._mh._trn.msg('yoda_actual_result',str(tco.test_result))));
                                        print("            {}".format(self._mh._trn.msg('yoda_log',str(tco.test_log))));                                                                                 
                    else:
                        print("      {0}\n   {1}".format(self._mh._trn.msg('yoda_test_scenario_prereq_failed')), ts.test_log);                       
        