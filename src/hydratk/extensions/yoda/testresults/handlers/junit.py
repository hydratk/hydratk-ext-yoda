# -*- coding: utf-8 -*-
"""Default test results JUnit output handler

.. module:: yoda.testresults.handlers.junit
   :platform: Unix
   :synopsis: Default test results JUnit output handler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
from hydratk.lib.debugging.simpledebug import dmsg
from xtermcolor import colorize
from hydratk.lib.string.operation import strip_accents
from hydratk.extensions.yoda.testresults import testresults
from hydratk.extensions.yoda.testresults.handlers.xjunit.testcase import TestCase
from hydratk.extensions.yoda.testresults.handlers.xjunit.testreport import TestReport
from hydratk.extensions.yoda.testresults.handlers.xjunit.testsuite import TestSuite
from hydratk.core.masterhead import MasterHead
from hydratk.lib.system.fs import file_put_contents
import datetime
import os


class TestResultsOutputHandler(object):
    """Class TestResultsOutputHandler
    """

    _options = {}
    _db_dsn = None
    _db_con = None

    def __init__(self, db_dsn, options={}):
        """Class constructor

        Called when object is initialized

        Args:
           db_dsn (str): dsn
           options (dict): output options

        """

        self._db_dsn = db_dsn
        self._options = options

    def create(self, test_run):
        """Methods creates test run output as JUnit file

        Args:
           test_run (obj): test run object

        Returns:
           void

        """
        if not os.path.exists(self._options['path']):
            print("Path {0} doesn't exists html report will be not created").format(self._options['path'])
            return False
        if not os.access(self._options['path'], os.W_OK):
            print("Path {0} is not writeable, permission denied").format(self._options['path'])
            return False 
        
        test_suites_list = []
        test_cases_list  = []
        mh = MasterHead.get_head()
        self._db_con = testresults.TestResultsDB(self._db_dsn)
        total_test_sets = self._db_con.db_data(
            "get_total_test_sets", {'test_run_id': test_run.id})[0]["total_test_sets"]
        total_tests = self._db_con.db_data(
            "get_total_tests", {'test_run_id': test_run.id})[0]["total_tests"]
        failed_tests = self._db_con.db_data(
            "get_failed_tests", {'test_run_id': test_run.id})[0]["failed_tests"]
        passed_tests = self._db_con.db_data(
            "get_passed_tests", {'test_run_id': test_run.id})[0]["passed_tests"]
        test_run_summary = mh._trn.msg(
            'yoda_test_run_summary', total_test_sets, total_tests, failed_tests, passed_tests)        
        dmsg(mh._trn.msg('yoda_create_output_console'))
        test_run_data    = self._db_con.db_data("get_test_run", {'test_run_id' : test_run.id })
        test_run_id = test_run_data[0]['name'] if test_run_data[0]['name'].decode() != 'Undefined' else test_run.id
        test_report_file = "{0}/{1}{2}.xml".format(self._options['path'],datetime.datetime.fromtimestamp(int(test_run_data[0]['start_time'])).strftime('%Y-%m-%d_%H-%M-%S_'),test_run_id)
        
        test_sets = self._db_con.db_data(
            "get_test_sets", {'test_run_id': test_run.id})
        for test_set in test_sets:            
            test_scenarios = self._db_con.db_data("get_test_scenarios", {'test_run_id': test_run.id, 'test_set_id': test_set['id'].decode()})
            
            test_cases_list = []
            for ts in test_scenarios:
                
                if ts['failures'] == True:
                    if ts['prereq_passed'] in (True, None):                        
                        test_cases = self._db_con.db_data("get_test_cases", {'test_run_id': test_run.id, 'test_set_id': test_set[
                                                          'id'].decode(), 'test_scenario_id': ts['id'].decode()})
                        for tca in test_cases:
                            if tca['failures'] > 0:  # tca.failed_tco
                                
                                test_conditions = self._db_con.db_data("get_test_conditions", {'test_run_id': test_run.id, 'test_set_id': test_set[
                                                                       'id'].decode(), 'test_scenario_id': ts['id'].decode(), 'test_case_id': tca['id'].decode()})
                                for tco in test_conditions:
                                    if tco['test_resolution'] != None and tco['test_resolution'].decode() == 'failed':
                                        
                                        test_cases_list.append(TestCase(name=tco['value'].decode(), failure=tco['test_result'], failure_message=tco['log'].decode()))
                                    else:
                                        #tco ok
                                        pass                                           
                                    if tco['events_passed'] == False:
                                        pass
                                    if tco['test_exec_passed'] == False:
                                        pass
                                    if tco['validate_exec_passed'] == False:
                                        pass
                                #tca failures
                                #test_cases_list.append(TestCase(name=tca['value'].decode(), time=tca['start_time'] - tca['end_time']))
                            else:
                                #tca ok 
                                test_cases_list.append(TestCase(name=tca['value'].decode(), time=tca['start_time'] - tca['end_time']))
                            if tca['events_passed'] == False:
                                print(colorize("    ! {0}".format(
                                    mh._trn.msg('yoda_test_case_events_failed', tca['log'].decode())), rgb=0xd70000))
                    else:
                        print(colorize("     ! {0}".format(mh._trn.msg('yoda_test_scenario_prereq_failed', colorize(
                            ts['log'].decode(), rgb=0xd70000))), rgb=0xd70000))
                    if ts['events_passed'] == False:
                        print(colorize("    ! {0}".format(mh._trn.msg(
                            'yoda_test_scenario_events_failed', ts['log'].decode())), rgb=0xd70000))
                    if ts['postreq_passed'] == True:
                        print(
                            "    + {0}".format(mh._trn.msg('yoda_test_scenario_postreq_passed')))
                    elif ts['postreq_passed'] == False:
                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_scenario_postreq_failed', colorize(
                            ts['log'].decode(), rgb=0xd70000))), rgb=0xd70000))
                else:
                    #ok test scenarios
                    pass
                            
            test_suites_list.append(TestSuite(test_cases_list, name=test_set['id'].decode()['id'].decode(), errors=test_set['failed_tests'], failures=test_set['failed_tests'], skipped=None, tests=test_set['total_tests']))
            
        test_report = TestReport(test_suites_list, name='MyReport')
        file_content = test_report.toXml(prettyPrint=True)
        file_put_contents(test_report_file, file_content)