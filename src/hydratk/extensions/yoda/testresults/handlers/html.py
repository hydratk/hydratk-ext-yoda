# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testresults.handlers.html
   :platform: Unix
   :synopsis: Default test results html output handler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
from hydratk.lib.debugging.simpledebug import dmsg
from hydratk.lib.string.operation import strip_accents
from hydratk.lib.system.fs import file_get_contents, file_put_contents
from hydratk.extensions.yoda.testresults import testresults
from hydratk.core.masterhead import MasterHead
import datetime
import os
import pickle

class TestResultsOutputHandler(object):
    _db_dsn               = None
    _db_con               = None
    _options              = {} 
    _have_template_header = False
    _have_template_footer = False
    
    def __init__(self, db_dsn, options = {}):
        self._db_dsn  = db_dsn
        self._options = options

    def bind_data(self, content, *args, **kwargs):
        """Method binds input data to request template

        Args:
           content (str): template
           args (arg): arguments
           kwargs (kwargs): key value arguments

        Returns:
           str content
    
        """
                
        if content is not None:
            content = str(content)
            for bdata in args:
                for var,value in bdata.items():
                    bind_var = '[{var}]'.format(var=var)                
                    content = content.replace(str(bind_var), str(value))
            for var, value in kwargs.items():
                bind_var = '[{var}]'.format(var=var)                
                content = content.replace(str(bind_var), str(value))                
        return content
                         
    def create(self, test_run):
        """Methods creates test run output for html report
        
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
        
        mh = MasterHead.get_head()
        self._db_con     = testresults.TestResultsDB(self._db_dsn)
        test_run_data    = self._db_con.db_data("get_test_run", {'test_run_id' : test_run.id })
        test_run_id = test_run_data[0]['name'] if test_run_data[0]['name'] != 'Undefined' else test_run.id
        test_report_file = "{0}/{1}{2}.html".format(self._options['path'],datetime.datetime.fromtimestamp(int(test_run_data[0]['start_time'])).strftime('%Y-%m-%d_%H-%M-%S_'),test_run_id)
        template_header_file = "{0}/header.html".format(self._options['style'])
        template_body_file   = "{0}/body.html".format(self._options['style'])
        template_footer_file = "{0}/footer.html".format(self._options['style'])
        
        template_body   = None
        template_header = None
        template_footer = None
        
        if not os.path.exists(template_body_file):
            print("Missing template body.html {0}, report will be not created".format(template_body_file))
            return False 
        if os.path.exists(template_header_file):
            template_header = file_get_contents(template_header_file)
            self._have_template_header = True
            
        if os.path.exists(template_footer_file):
            template_header = file_get_contents(template_footer_file)
            self._have_template_footer = True
                
        template_body = file_get_contents(template_body_file)
           
        total_test_sets  = self._db_con.db_data("get_total_test_sets", {'test_run_id' : test_run.id })[0]["total_test_sets"]
        total_tests      = self._db_con.db_data("get_total_tests", {'test_run_id' : test_run.id })[0]["total_tests"]
        failed_tests     = self._db_con.db_data("get_failed_tests", {'test_run_id' : test_run.id })[0]["failed_tests"]
        passed_tests     = self._db_con.db_data("get_passed_tests", {'test_run_id' : test_run.id })[0]["passed_tests"]
        dmsg(mh._trn.msg('yoda_create_output_html', test_report_file))
        
        test_results = self.get_test_results(test_run.id)
        
        header = '' if template_header == None else template_header
        footer = '' if template_footer == None else template_footer       
        trf = self.bind_data(
                        template_body,
                        {
                          'header' : header,
                          'footer' : footer,
                          'total_test_sets' : total_test_sets,
                          'total_tests' : total_tests,
                          'passed_tests' : passed_tests,
                          'failed_tests' : failed_tests,
                          'test_run_id'  : test_run_id,
                          'test_run_start_time' : datetime.datetime.fromtimestamp(int(test_run_data[0]['start_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                          'test_run_end_time' : datetime.datetime.fromtimestamp(int(test_run_data[0]['end_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                          'test_run_total_time' : round(test_run_data[0]['end_time'] - test_run_data[0]['start_time'],3),
                          'test_results' : test_results
                         }
                        )         
        file_put_contents(test_report_file, trf)

    def _format_custom_tco_opt(self, tco, tco_opt):
        
        res = ""
        res += """
        <tr>
          <th>Id:</th>
          <td>{tco_id}</td>
        </tr>
        <tr>
          <th>Name:</th>
          <td>{tc_name}</td>
        </tr>       
        """.format(
                   tco_id = tco['tco_id'],
                   tc_name = tco['value'],
                  )
        tco_opt_rest = []        
        for opt_dict in tco_opt:          
            if opt_dict['key'] == 'name':               
                continue
            if opt_dict['key'] == 'desc':                 
                tco_desc = opt_dict['value']              
                continue          
            tco_opt_rest.append(opt_dict)
            
        res += """
         <tr>
           <th>Description:</th>
           <td>{tco_desc}</td>
        </tr>
        <tr>   
           <th>Start time:</th>
          <td>{start_time}</td>
        </tr>
        <tr>
          <th>End time:</th>
          <td>{end_time}</td>
        </tr>
        <tr>
          <th>Total time:</th>
          <td>{total_time} s</td>
        </tr>        
        <tr>
          <th>Test resolution:</th>
          <td>{test_resolution}</td>
        </tr>
        <tr>
          <th>Expected result:</th>
          <td>{expected_result}</td>
        </tr>
        <tr>
          <th>Actual result:</th>
          <td>{test_result}</td>
        </tr>
        </tr>
          <th>Log:</th>
          <td>{log}</td>          
        </tr>                       
        """.format(
                   tco_desc = tco_desc,
                   start_time = datetime.datetime.fromtimestamp(int(tco['start_time'])).strftime('%Y-%m-%d %H:%M:%S'), 
                   end_time = datetime.datetime.fromtimestamp(int(tco['end_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                   total_time = round(tco['end_time'] - tco['start_time'],3),
                   test_resolution = tco['test_resolution'],
                   expected_result = tco['expected_result'],
                   test_result = tco['test_result'],                  
                   log = tco['log'].replace("\n","<br>")
                  )
        tco_opt_rest_all = {} 
                             
        for opt_dict in tco_opt_rest:
            if opt_dict['key'] not in tco_opt_rest_all:
                tco_opt_rest_all[opt_dict['key']] = {
                                                    'key'   : opt_dict['key'],
                                                    'value' : opt_dict['value'],
                                                    'pickled' : opt_dict['pickled'],
                                                    'options' : { } 
                                                   }
            if opt_dict['opt_name'] is not None:    
                tco_opt_rest_all[opt_dict['key']]['options'][opt_dict['opt_name']] = opt_dict['opt_value']
        
        if len(tco_opt_rest_all) > 0:            
            res += self._process_custom_data_opt(tco_opt_rest_all)
            
        return res  
        
    def _format_custom_tc_opt(self, tc, tc_opt):
            
        res = ""
        res += """
        <tr>
          <th>Id:</th>
          <td>{tca_id}</td>
        </tr>
        <tr>
          <th>Name:</th>
          <td>{tc_name}</td>
        </tr>
        """.format(
                   tca_id = tc['tca_id'],
                   tc_name = tc['value']
                   )
        
        tc_opt_rest = []        
        for opt_dict in tc_opt:          
            if opt_dict['key'] == 'name':               
                continue
            if opt_dict['key'] == 'desc':                 
                tc_desc = opt_dict['value']              
                continue          
            tc_opt_rest.append(opt_dict)
            
        res += """
         <tr>
           <th>Description:</th>
           <td>{tc_desc}</td>
        </tr>
         <tr>
          <th>Start time:</th>
          <td>{start_time}</td>
        </tr>
        <tr>
          <th>End time:</th>
          <td>{end_time}</td>
        </tr>
        <tr>
          <th>Total time:</th>
          <td>{total_time} s</td>
        </tr>
        <tr>
          <th>Total tests:</th>
          <td>{total_tests}</td>
        </tr>
        <tr>
          <th>Passed tests:</th>
          <td>{passed_tests}</td>          
        </tr>
        <tr>
          <th>Failed tests:</th>
          <td>{failed_tests}</td>          
        </tr>
        <tr>
          <th>Log:</th>
          <td>{log}</td>          
        </tr>                       
        """.format(                   
                   tc_desc = tc_desc,
                   start_time = datetime.datetime.fromtimestamp(int(tc['start_time'])).strftime('%Y-%m-%d %H:%M:%S'), 
                   end_time = datetime.datetime.fromtimestamp(int(tc['end_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                   total_time = round(tc['end_time'] - tc['start_time'],3),
                   total_tests = tc['total_tests'],
                   passed_tests = tc['passed_tests'],
                   failed_tests = tc['failed_tests'],
                   log = tc['log'].replace("\n","<br>")
                  )
        tc_opt_rest_all = {} 
                             
        for opt_dict in tc_opt_rest:
            if opt_dict['key'] not in tc_opt_rest_all:
                tc_opt_rest_all[opt_dict['key']] = {
                                                    'key'   : opt_dict['key'],
                                                    'value' : opt_dict['value'],
                                                    'pickled' : opt_dict['pickled'],
                                                    'options' : { } 
                                                   }
            if opt_dict['opt_name'] is not None:    
                tc_opt_rest_all[opt_dict['key']]['options'][opt_dict['opt_name']] = opt_dict['opt_value']
        
        if len(tc_opt_rest_all) > 0:            
            res += self._process_custom_data_opt(tc_opt_rest_all)
            
        return res  
    
    def _format_custom_ts_opt(self, ts, ts_opt):        
        res = ""
        res += """
        <tr>
          <th>Id:</th>
          <td>{ts_id}</td>
        </tr>
        <tr>
          <th>Name:</th>
          <td>{ts_name}</td>
        </tr>
        """.format(ts_id = ts['ts_id'], ts_name = ts['value'])        
      
        ts_desc    = ''
        ts_author  = ''
        ts_version = ''
        ts_opt_rest = []        
        for opt_dict in ts_opt:          
            if opt_dict['key'] == 'name':               
                continue
            if opt_dict['key'] == 'desc':                 
                ts_desc = opt_dict['value']              
                continue
            if opt_dict['key'] == 'path':                 
                ts_path = opt_dict['value']              
                continue
            if opt_dict['key'] == 'author':    
                ts_author = opt_dict['value']              
                continue
            if opt_dict['key'] == 'version':    
                ts_version = opt_dict['value']                
                continue
            ts_opt_rest.append(opt_dict)
        
        prereq = "Not defined"
        if ts['prereq_passed'] in (True, False):
            prereq = "Failed" if ts['prereq_passed'] == False else "Passed"
             
        postreq = "Not defined"
        if ts['postreq_passed'] in (True, False):
            prereq = "Failed" if ts['postreq_passed'] == False else "Passed"            
                             
        res += """
        <tr>
          <th>Path:</th>
          <td>{ts_path}</td>
        </tr>
        <tr>
          <th>Description:</th>
          <td>{ts_desc}</td>
        </tr>
        <tr>
          <th>Author:</th>
          <td>{ts_author}</td>
        </tr>
        <tr>
          <th>Version:</th>
          <td>{ts_version}</td>
        </tr>
        <tr>
          <th>Prerequisities:</th>
          <td>{prereq}</td>
        </tr>
        <tr>
          <th>Postrequisities:</th>
          <td>{postreq}</td>
        </tr>
        <tr>
          <th>Start time:</th>
          <td>{start_time}</td>
        </tr>
        <tr>
          <th>End time:</th>
          <td>{end_time}</td>
        </tr>
        <tr>
          <th>Total time:</th>
          <td>{total_time} s</td>
        </tr>
        <tr>
          <th>Total tests:</th>
          <td>{total_tests}</td>
        </tr>
        <tr>
          <th>Passed tests:</th>
          <td>{passed_tests}</td>          
        </tr>
        <tr>
          <th>Failed tests:</th>
          <td>{failed_tests}</td>          
        </tr>
        <tr>
          <th>Log:</th>
          <td>{log}</td>          
        </tr>               
                       
        """.format(
                   ts_path = ts_path,
                   ts_desc = ts_desc,
                   ts_author = ts_author,
                   ts_version = ts_version,
                   prereq = prereq,
                   postreq = postreq,
                   start_time = datetime.datetime.fromtimestamp(int(ts['start_time'])).strftime('%Y-%m-%d %H:%M:%S'), 
                   end_time = datetime.datetime.fromtimestamp(int(ts['end_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                   total_time = round(ts['end_time'] - ts['start_time'],3),
                   total_tests = ts['total_tests'],
                   passed_tests = ts['passed_tests'],
                   failed_tests = ts['failed_tests'],
                   log = ts['log'].replace("\n","<br>") 
                  )
        
        ts_opt_rest_all = {}                      
        for opt_dict in ts_opt_rest:
            if opt_dict['key'] not in ts_opt_rest_all:
                ts_opt_rest_all[opt_dict['key']] = {
                                                    'key'   : opt_dict['key'],
                                                    'value' : opt_dict['value'],
                                                    'pickled' : opt_dict['pickled'],
                                                    'options' : { } 
                                                   }
            if opt_dict['opt_name'] is not None:    
                ts_opt_rest_all[opt_dict['key']]['options'][opt_dict['opt_name']] = opt_dict['opt_value']
        
        if len(ts_opt_rest_all) > 0:            
            res += self._process_custom_data_opt(ts_opt_rest_all)
               
        return res
     
    def _process_custom_data_opt(self, opt_dict):
        res = ""        
        for k,v in opt_dict.items():                            
            if v['pickled'] == 1:
                v['value'] = pickle.loads(opt_dict['value'])
            opt_name = v['key'] if 'label' not in v['options'] else v['options']['label'] 
                
            res += """
                 <tr>
                    <th>{opt_name}</th>
                    <td>{opt_value}</td>
                 </tr> 
               """.format(opt_name = opt_name, opt_value = v['value'])
        return res
               
    def get_test_results(self, test_run_id):
        res = ""
        
        test_sets = self._db_con.db_data("get_test_sets", {'test_run_id' : test_run_id })
                   
        for test_set in test_sets:
            test_set_end_time = "Not completed" if int(test_set['end_time']) == -1 else datetime.datetime.fromtimestamp(int(test_set['end_time'])).strftime('%Y-%m-%d %H:%M:%S')               
            res += """<hr>
            
                      <table>
                            <caption>Test set</caption>
                            <tr>
                               <th>Path:</th>
                               <td>{test_set_id}</td>
                            </tr>            
                            <tr>
                               <th>Start time:</th>
                               <td>{test_set_start_time}</td>
                            </tr>
                            <tr>
                               <th>End time:</th>
                               <td>{test_set_end_time}</td>
                            </tr>
                             <tr>
                               <th>Total time:</th>
                               <td>{test_set_total_time} s</td>
                            </tr>
                            <tr>
                               <th>Total tests:</th>
                               <td>{test_set_total_tests}</td>
                            </tr>
                            <tr>
                               <th>Passed tests:</th>
                               <td>{test_set_passed_tests}</td>
                            </tr>
                            <tr>
                               <th>Failed tests:</th>
                               <td>{test_set_failed_tests}</td>
                            </tr>
                            <tr>
                               <th>Log:</th>
                               <td>{test_set_log}</td>
                            </tr>                                                       
                        """.format(
                                   test_set_id           = test_set['tset_id'],
                                   test_set_start_time   = datetime.datetime.fromtimestamp(int(test_set['start_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                                   test_set_end_time     = test_set_end_time,
                                   test_set_total_time   = 0 if int(test_set['end_time']) == -1 else round(test_set['end_time'] - test_set['start_time'],3),
                                   test_set_total_tests  = test_set['total_tests'],
                                   test_set_passed_tests = test_set['passed_tests'],                                   
                                   test_set_failed_tests = test_set['failed_tests'],
                                   test_set_log          = test_set['log'].replace("\n","<br>"),
                                 )
                        
            test_scenarios = self._db_con.db_data("get_test_scenarios", {'test_run_id' : test_run_id, 'test_set_id' : test_set['id'].decode() })                                                             
            for ts in test_scenarios:
                ts_opt = self._db_con.db_data("get_test_custom_opt", {'test_object_id' : ts['id']})                
                res += """<tr>
                            <td>&nbsp;</td>
                            <td>
                               <table>
                                  <caption>Test Scenario</caption>
                                  {ts_opt}
                                  <tr>
                                    <td>&nbsp;</td>
                                      <td>
                       """.format(ts_opt = self._format_custom_ts_opt(ts, ts_opt))
                test_cases = self._db_con.db_data("get_test_cases", {'test_run_id' : test_run_id, 'test_set_id' : test_set['id'].decode(), 'test_scenario_id' : ts['id'].decode() })                
                for tca in test_cases: 
                    tca_opt = self._db_con.db_data("get_test_custom_opt", {'test_object_id' : tca['id']})  
                    res += """      
                                          <table>
                                            <caption>Test Case</caption>
                                             {tc_opt}
                                             <tr>
                                               <td>&nbsp;</td>
                                               <td>                                      
                          """.format(tc_opt = self._format_custom_tc_opt(tca, tca_opt))
                    test_conditions = self._db_con.db_data("get_test_conditions", {'test_run_id' : test_run_id, 'test_set_id' : test_set['id'].decode(), 'test_scenario_id' : ts['id'].decode(), 'test_case_id' : tca['id'].decode() })        
                    for tco in test_conditions:
                        tco_opt = self._db_con.db_data("get_test_custom_opt", {'test_object_id' : tco['id']})
                        res += """      
                                          <table>
                                            <caption>Test Condition</caption>
                                             {tco_opt}                                             
                                          </table>                                          
                               """.format(tco_opt = self._format_custom_tco_opt(tco, tco_opt))                                      
                    #End of test cases             
                    res +=  """</td>
                       </tr>
                       </table>                                                                                 
                    """      
                #End of test scenarios             
                res +=  """</td>
                       </tr>                                             
                       </table>              
                    """ 
            #end of test set          
            res +=  """</td>
                       </tr>                                             
                       </table>              
                    """ 
        #TODO implement rest of the info
        
                #print(ts)                
        #        print("  {0}".format(mh._trn.msg('yoda_test_scenario_summary', ts['value'].decode() ,ts['total_tests'], ts['failed_tests'],ts['passed_tests'])))                                                                                                         
        #        if ts['failures'] == True:                    
        #            if ts['prereq_passed'] in (True,None):                        
        #                if ts['prereq_passed'] == True: print("    + {0}".format(mh._trn.msg('yoda_test_scenario_prereq_passed')))                       
        #                test_cases = self._db_con.db_data("get_test_cases", {'test_run_id' : test_run.id, 'test_set_id' : test_set['id'].decode(), 'test_scenario_id' : ts['id'].decode() })                                                                                   
        #                for tca in test_cases:                                                                                                                                                                   
        #                    if tca['failures'] > 0: #tca.failed_tco
        #                        print("    {0}".format(mh._trn.msg('yoda_test_case',tca['value'].decode())))
        #                        test_conditions = self._db_con.db_data("get_test_conditions", {'test_run_id' : test_run.id, 'test_set_id' : test_set['id'].decode(), 'test_scenario_id' : ts['id'].decode(), 'test_case_id' : tca['id'].decode() })                                                                                      
        #                        for tco in test_conditions:                                                                    
        #                            if tco['test_resolution'] != None and tco['test_resolution'].decode() == 'failed':
        #                                print("      {0}".format(mh._trn.msg('yoda_test_condition',tco['value'].decode())))
        #                                print("            {0}".format(mh._trn.msg('yoda_expected_result',tco['expected_result'].decode().strip())))                                        
        #                                print("            {0}".format(mh._trn.msg('yoda_actual_result',tco['test_result'].decode() if tco['test_result'] != None else None)))
        #                                print("            {0}".format(mh._trn.msg('yoda_log',colorize(tco['log'].decode(),rgb=0x00bfff))))
        #                            if tco['events_passed'] == False:
        #                                print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_condition_events_failed', tco['log'].decode())),rgb=0xd70000))
        #                            if tco['test_exec_passed'] == False:
        #                                print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_condition_test_exec_failed', tco['log'].decode())),rgb=0xd70000))
        #                            if tco['validate_exec_passed'] == False:
        #                                print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_condition_validate_exec_failed', tco['log'].decode())),rgb=0xd70000))
        #                        
        #                    if tca['events_passed'] == False:
        #                        print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_case_events_failed', tca['log'].decode())),rgb=0xd70000))                                                                                                                              
        #            else:
        #                print(colorize("     ! {0}".format(mh._trn.msg('yoda_test_scenario_prereq_failed', colorize(ts['log'].decode(), rgb=0xd70000))),rgb=0xd70000))
        #            if ts['events_passed'] == False:
        #                print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_scenario_events_failed', ts['log'].decode())),rgb=0xd70000))
        #            if ts['postreq_passed'] == True:
        #                print("    + {0}".format(mh._trn.msg('yoda_test_scenario_postreq_passed')))
        #            elif ts['postreq_passed'] == False:
        #                print(colorize("    ! {0}".format(mh._trn.msg('yoda_test_scenario_postreq_failed', colorize(ts['log'].decode(), rgb=0xd70000))),rgb=0xd70000))
            res += """
              </table> 
              </td>
              </tr>    
            </table>"""   
        return res;    