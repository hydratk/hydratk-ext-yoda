# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testresults.handlers.console
   :platform: Unix
   :synopsis: Default test results console output handler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
from hydratk.lib.debugging.simpledebug import dmsg
from xtermcolor import colorize
from hydratk.lib.string.operation import strip_accents
from hydratk.extensions.yoda.testresults import testresults
from hydratk.core.masterhead import MasterHead

class TestResultsOutputHandler(object):
    _options = {}
    _db_dsn  = None
    _db_con  = None
    
    def __init__(self, db_dsn, options = {}):
        self._db_dsn  = db_dsn
        self._options = options
        
    def create(self, test_run):
        mh = MasterHead.get_head()
        self._db_con     = testresults.TestResultsDB(self._db_dsn)
        total_test_sets  = self._db_con.db_data("get_total_test_sets", {'test_run_id' : test_run.id })[0]["total_test_sets"]
        total_tests      = self._db_con.db_data("get_total_tests", {'test_run_id' : test_run.id })[0]["total_tests"]
        failed_tests     = self._db_con.db_data("get_failed_tests", {'test_run_id' : test_run.id })[0]["failed_tests"]
        passed_tests     = self._db_con.db_data("get_passed_tests", {'test_run_id' : test_run.id })[0]["passed_tests"]
        test_run_summary = mh._trn.msg('yoda_test_run_summary', total_test_sets, total_tests, failed_tests, passed_tests)
        bar_len = len(strip_accents(test_run_summary))
        dmsg("Creating console output")
        trs_tpl = """
+{bar}+
|{test_run_summary}|
+{bar}+""".format(bar = bar_len * '-', test_run_summary=test_run_summary)                
        print(trs_tpl)
        
        test_sets = self._db_con.db_data("get_test_sets", {'test_run_id' : test_run.id })   
        for test_set in test_sets:
            print("\n{0}".format(mh._trn.msg('yoda_test_set_summary', test_set['tset_id'])))
            test_scenarios = self._db_con.db_data("get_test_scenarios", {'test_run_id' : test_run.id, 'test_set_id' : test_set['id'] })                                                 
            for ts in test_scenarios:                
                print("  {0}".format(mh._trn.msg('yoda_test_scenario_summary', ts['value'],ts['total_tests'], ts['failed_tests'],ts['passed_tests'])))                                                                                                         
                if ts['failures'] == True:                    
                    if ts['prereq_passed'] in (True,None):                        
                        if ts['prereq_passed'] == True: print("    + {0}".format(mh._trn.msg('yoda_test_scenario_prereq_passed')))                       
                        test_cases = self._db_con.db_data("get_test_cases", {'test_run_id' : test_run.id, 'test_set_id' : test_set['id'], 'test_scenario_id' : ts['id'] })                                                                   
                        for tca in test_cases:
                            #print(tca)                                                                                                                                        
                            if tca['failures'] > 0: #tca.failed_tco
                                print("    {0}".format(mh._trn.msg('yoda_test_case',tca['value'])))
                                test_conditions = self._db_con.db_data("get_test_conditions", {'test_run_id' : test_run.id, 'test_set_id' : test_set['id'], 'test_scenario_id' : ts['id'], 'test_case_id' : tca['id'] })                                                                                      
                                for tco in test_conditions:                                                                    
                                    if tco['test_resolution'] == 'failed':
                                        print("      {0}".format(mh._trn.msg('yoda_test_condition',tco['value'])))
                                        print("            {}".format(mh._trn.msg('yoda_expected_result',str(tco['expected_result']).strip())))                                        
                                        print("            {}".format(mh._trn.msg('yoda_actual_result',str(tco['test_result']))))
                                        print("            {}".format(mh._trn.msg('yoda_log',colorize(str(tco['log']),rgb=0x00bfff))))
                                    if tco['events_passed'] == False:
                                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_condition_events_failed', tco['log'])),rgb=0xd70000))
                                    if tco['test_exec_passed'] == False:
                                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_condition_test_exec_failed', tco['log'])),rgb=0xd70000))
                                    if tco['validate_exec_passed'] == False:
                                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_condition_validate_exec_failed', tco['log'])),rgb=0xd70000))
                                
                            if tca['events_passed'] == False:
                                print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_case_events_failed', tca['log'])),rgb=0xd70000))                                                                                                                              
                    else:
                        print(colorize("     ! {0}".format(mh._trn.msg('yoda_test_scenario_prereq_failed', colorize(ts['log'], rgb=0xd70000))),rgb=0xd70000))
                    if ts['events_passed'] == False:
                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_scenario_events_failed', ts['log'])),rgb=0xd70000))
                    if ts['postreq_passed'] == True:
                        print("    + {0}".format(mh._trn.msg('yoda_test_scenario_postreq_passed')))
                    elif ts['postreq_passed'] == False:
                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_scenario_postreq_failed', colorize(ts['log'], rgb=0xd70000))),rgb=0xd70000))             