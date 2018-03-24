# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

.. module:: yoda.testresults.handlers.html
   :platform: Unix
   :synopsis: Default test results html output handler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.lib.debugging.simpledebug import dmsg
from hydratk.lib.system.fs import file_get_contents, file_put_contents
from hydratk.extensions.yoda.testresults import testresults
from hydratk.core.masterhead import MasterHead
from hydratk.extensions.yoda.testengine import MacroParser
import hydratk.lib.system.config as syscfg
import datetime
import os
import pickle
import base64

class TemplateHooks(object):
    """Class TemplateHooks
    """

    _options = {}
    
    def __init__(self, options):
        """Class constructor

        Called when object is initialized

        Args:
           options (dict): options

        """

        self._options = options
        self._options['style'] = self._options['style'].format(var_dir=syscfg.HTK_VAR_DIR)
        
    def _dispatch_options(self, str_opt):
        """Methods dispatches options

        Args:
           str_opt (str): options in str form

        Returns:
           dict

        """

        res = {}
        if str_opt not in (None,''):
            str_opts = str_opt.split(',')
            for optval in str_opts:
                opt, val = optval.split('=')
                res[opt.strip()] = val.strip()
                
        return res
    
    def get_content_type(self, file_extension):
        """Methods gets file specific content type

        Args:
           file_extension (str): file extension

        Returns:
           str

        """

        res = None        
        if file_extension not in (None,''):
            file_extension = file_extension.strip('.')
            if file_extension == 'png':
                res = 'image/png'
            elif file_extension in ('jpg','jpeg'):
                res = 'image/jpeg'
            elif file_extension == 'gif':
                res = 'image/gif'
            elif file_extension == 'css':
                res = 'text/css'
            elif file_extension == 'js':
                res = 'text/javascript'
            elif file_extension == 'ttf':
                res = 'font/truetype'
        return res
            
    def embed(self, content_opt):
        """Methods embeds content

        Args:
           content_opt (str): options in str form

        Returns:
           str

        """

        dcopt = self._dispatch_options(content_opt)
        src_file = dcopt['file']
        encoding = dcopt['encoding'] if 'encoding' in dcopt else 'no'
        charset  = dcopt['charset'] if 'charset' in dcopt else None        
        if dcopt['file'][0] != '/': #relative path to the current style
            src_file = "{0}/{1}".format(self._options['style'],dcopt['file'])
        if os.path.exists(src_file):
            if encoding == 'no':
                file_data = file_get_contents(src_file, mode='rb').decode()
            elif encoding == 'text':
                file_data = str(file_get_contents(src_file, mode='rb'))                    
            elif encoding == 'base64':
                file_data = base64.b64encode(file_get_contents(src_file, mode='rb')).decode()
                
            if 'content-type' not in dcopt:
                file_extension = os.path.splitext(src_file)[1]
                content_type = self.get_content_type(file_extension)
            else:
                content_type = dcopt['content-type']
            #Put it all together
            if content_type in (None,'none'):                
                res = file_data
            else:
                charset_opt = "charset={0};".format(charset) if charset is not None else ''                                        
                res = "data:{content_type};{charset_opt}base64,{file_data}".format(content_type=content_type, charset_opt=charset_opt, file_data=file_data)
                
        else:
            res = "[{0} doesn't exists]".format(src_file);
             
        return res     
    
class TestResultsOutputHandler(object):
    """Class TestResultsOutputHandler
    """

    _db_dsn               = None
    _db_con               = None
    _options              = {} 
    _have_template_header = False
    _have_template_footer = False
    
    def __init__(self, db_dsn, options={}):
        """Class constructor

        Called when object is initialized

        Args:
           db_dsn (str): dsn
           options (dict): output options

        """

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
    
    def _register_tpl_hooks(self, mp):
        """Method registers template hooks

        Args:
           mp (obj): MacroParser

        Returns:
           void

        """

        tplh = TemplateHooks(self._options)
        mp.mp_add_hooks(
                        {
                          'embed' : tplh.embed
                         }
                        )
                         
    def create(self, test_run):
        """Methods creates test run output for html report
        
        Args:
           test_run (obj): test run object
           
        Returns:
           void
            
        """
        
        mh = MasterHead.get_head()
        if not os.path.exists(self._options['path']):
            print(mh._trn.msg('yoda_html_path_not_exist', self._options['path']))
            return False
        if not os.access(self._options['path'], os.W_OK):
            print(mh._trn.msg('yoda_html_path_not_writable', self._options['path']))
            return False 

        mp = MacroParser(r'\[(.*):(.*)\]')
        self._register_tpl_hooks(mp)
        
        self._db_con     = testresults.TestResultsDB(self._db_dsn)
        test_run_data    = self._db_con.db_data("get_test_run", {'test_run_id' : test_run.id })
        if (test_run_data == None or len(test_run_data) == 0):
            return False

        test_run_id = test_run_data[0]['name'] if test_run_data[0]['name'].decode() != 'Undefined' else test_run.id
        test_report_file = "{0}/{1}{2}.html".format(self._options['path'],datetime.datetime.fromtimestamp(int(test_run_data[0]['start_time'])).strftime('%Y-%m-%d_%H-%M-%S_'),test_run_id)
        template_header_file = "{0}/header.html".format(self._options['style'])
        template_body_file   = "{0}/body.html".format(self._options['style'])
        template_footer_file = "{0}/footer.html".format(self._options['style'])
        
        template_body   = None
        template_header = None
        template_footer = None
        
        if not os.path.exists(template_body_file):
            print(mh._trn.msg('yoda_html_missing_template', template_body_file))
            return False 
        if os.path.exists(template_header_file):
            template_header = file_get_contents(template_header_file)
            self._have_template_header = True
            
        if os.path.exists(template_footer_file):
            template_footer = file_get_contents(template_footer_file)
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
        trf = mp.mp_parse(trf)         
        file_put_contents(test_report_file, trf)
        
    def _format_custom_tco_opt(self, tco, tco_opt):
        """Method formats custom test condition options

        Args:
           tco (dict): test condition
           tco_opt (list): options

        Returns:
           str

        """
        
        res = ""
        res += """
        <tr>
          <th>Id:</th>
          <td class="TestConditionTableValue">{tco_id}</td>
        </tr>
        <tr>
          <th>Name:</th>
          <td class="TestConditionTableValue">{tc_name}</td>
        </tr>       
        """.format(
                   tco_id = tco['tco_id'].decode(),
                   tc_name = tco['value'].decode(),
                  )
        tco_desc = ''
        
        tco_opt_rest = []        
        for opt_dict in tco_opt:          
            if opt_dict['key'] == 'name':               
                continue
            if opt_dict['key'] == 'desc':                 
                tco_desc = opt_dict['value'].decode()              
                continue          
            tco_opt_rest.append(opt_dict)
            
        res += """
         <tr>
           <th>Description:</th>
           <td class="TestConditionTableValue">{tco_desc}</td>
        </tr>
        <tr>   
           <th>Start time:</th>
          <td class="TestConditionTableValue">{start_time}</td>
        </tr>
        <tr>
          <th>End time:</th>
          <td class="TestConditionTableValue">{end_time}</td>
        </tr>
        <tr>
          <th>Total time:</th>
          <td class="TestConditionTableValue">{total_time} s</td>
        </tr>        
        <tr>
          <th>Test resolution:</th>
          <td class="TestConditionTableValue">{test_resolution}</td>
        </tr>
        <tr>
          <th>Expected result:</th>
          <td class="TestConditionTableValue">{expected_result}</td>
        </tr>
        <tr>
          <th>Actual result:</th>
          <td class="TestConditionTableValue">{test_result}</td>
        </tr>
        </tr>
          <th>Log:</th>
          <td class="TestConditionTableValue">{log}</td>          
        </tr>                       
        """.format(
                   tco_desc = tco_desc,
                   start_time = datetime.datetime.fromtimestamp(int(tco['start_time'])).strftime('%Y-%m-%d %H:%M:%S'), 
                   end_time = datetime.datetime.fromtimestamp(int(tco['end_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                   total_time = round(tco['end_time'] - tco['start_time'],3),
                   test_resolution = tco['test_resolution'].decode() if hasattr(tco['test_resolution'], 'decode') else tco['test_resolution'],
                   expected_result = tco['expected_result'].decode() if hasattr(tco['expected_result'], 'decode') else tco['expected_result'],
                   test_result = tco['test_result'].decode() if hasattr(tco['test_result'], 'decode') else tco['test_result'],                  
                   log = tco['log'].decode().replace("\n","<br>")
                  )
        tco_opt_rest_all = {} 
                             
        for opt_dict in tco_opt_rest:
            if opt_dict['key'] not in tco_opt_rest_all:
                tco_opt_rest_all[opt_dict['key']] = {
                                                    'key'   : opt_dict['key'].decode(),
                                                    'value' : opt_dict['value'].decode(),
                                                    'pickled' : opt_dict['pickled'],
                                                    'options' : { } 
                                                   }
            if opt_dict['opt_name'] is not None:    
                tco_opt_rest_all[opt_dict['key']]['options'][opt_dict['opt_name'].decode()] = opt_dict['opt_value'].decode()
        
        if len(tco_opt_rest_all) > 0:            
            res += self._process_custom_data_opt(tco_opt_rest_all, 'TestCondition')
            
        return res  
        
    def _format_custom_tc_opt(self, tc, tc_opt):
        """Method formats custom test case options

        Args:
           tc (dict): test case
           tc_opt (list): options

        Returns:
           str

        """
            
        res = ""
        res += """
        <tr>
          <th>Id:</th>
          <td class="TestCaseTableValue">{tca_id}</td>
        </tr>
        <tr>
          <th>Name:</th>
          <td class="TestCaseTableValue">{tc_name}</td>
        </tr>
        """.format(
                   tca_id = tc['tca_id'].decode(),
                   tc_name = tc['value'].decode()
                   )
        
        tc_desc = ''
        
        tc_opt_rest = []        
        for opt_dict in tc_opt:          
            if opt_dict['key'] == 'name':               
                continue
            if opt_dict['key'] == 'desc':                 
                tc_desc = opt_dict['value'].decode()              
                continue          
            tc_opt_rest.append(opt_dict)
            
        res += """
         <tr>
           <th>Description:</th>
           <td class="TestCaseTableValue">{tc_desc}</td>
        </tr>
         <tr>
          <th>Start time:</th>
          <td class="TestCaseTableValue">{start_time}</td>
        </tr>
        <tr>
          <th>End time:</th>
          <td class="TestCaseTableValue">{end_time}</td>
        </tr>
        <tr>
          <th>Total time:</th>
          <td class="TestCaseTableValue">{total_time} s</td>
        </tr>
        <tr>
          <th>Total tests:</th>
          <td class="TestCaseTableValue">{total_tests}</td>
        </tr>
        <tr>
          <th>Passed tests:</th>
          <td class="TestCaseTableValue">{passed_tests}</td>          
        </tr>
        <tr>
          <th>Failed tests:</th>
          <td class="TestCaseTableValue">{failed_tests}</td>          
        </tr>
        <tr>
          <th>Log:</th>
          <td class="TestCaseTableValue">{log}</td>          
        </tr>                       
        """.format(                   
                   tc_desc = tc_desc,
                   start_time = datetime.datetime.fromtimestamp(int(tc['start_time'])).strftime('%Y-%m-%d %H:%M:%S'), 
                   end_time = datetime.datetime.fromtimestamp(int(tc['end_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                   total_time = round(tc['end_time'] - tc['start_time'],3),
                   total_tests = tc['total_tests'],
                   passed_tests = tc['passed_tests'],
                   failed_tests = tc['failed_tests'],
                   log = tc['log'].decode().replace("\n","<br>")
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
            res += self._process_custom_data_opt(tc_opt_rest_all, 'TestCase')
            
        return res  
    
    def _format_custom_ts_opt(self, ts, ts_opt):
        """Method formats custom test scenario options

        Args:
           ts (dict): test scenario
           ts_opt (list): options

        Returns:
           str

        """

        res = ""
        res += """
        <tr>
          <th>Id:</th>
          <td class="TestScenarioTableValue">{ts_id}</td>
        </tr>
        <tr>
          <th>Name:</th>
          <td class="TestScenarioTableValue">{ts_name}</td>
        </tr>
        """.format(
                   ts_id = ts['ts_id'].decode() if hasattr(ts['ts_id'], 'decode') else ts['ts_id'],
                   ts_name = ts['value'].decode() if hasattr(ts['value'], 'decode') else ts['value']
                   )
                
        ts_path    = ''
        ts_desc    = ''
        ts_author  = ''
        ts_version = ''
        ts_opt_rest = []                
        for opt_dict in ts_opt:          
            if opt_dict['key'] == 'name':               
                continue
            if opt_dict['key'] == 'desc':                 
                ts_desc = opt_dict['value'].decode() if hasattr(opt_dict['value'], 'decode') else opt_dict['value']             
                continue
            if opt_dict['key'] == 'path':                 
                ts_path = opt_dict['value'].decode() if hasattr(opt_dict['value'], 'decode') else opt_dict['value']              
                continue
            if opt_dict['key'] == 'author':    
                ts_author = opt_dict['value'].decode() if hasattr(opt_dict['value'], 'decode') else opt_dict['value']              
                continue
            if opt_dict['key'] == 'version':    
                ts_version = opt_dict['value'].decode() if hasattr(opt_dict['value'], 'decode') else opt_dict['value']                
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
          <td class="TestScenarioTableValue">{ts_path}</td>
        </tr>
        <tr>
          <th>Description:</th>
          <td class="TestScenarioTableValue">{ts_desc}</td>
        </tr>
        <tr>
          <th>Author:</th>
          <td class="TestScenarioTableValue">{ts_author}</td>
        </tr>
        <tr>
          <th>Version:</th>
          <td class="TestScenarioTableValue">{ts_version}</td>
        </tr>
        <tr>
          <th>Prerequisities:</th>
          <td class="TestScenarioTableValue">{prereq}</td>
        </tr>
        <tr>
          <th>Postrequisities:</th>
          <td class="TestScenarioTableValue">{postreq}</td>
        </tr>
        <tr>
          <th>Start time:</th>
          <td class="TestScenarioTableValue">{start_time}</td>
        </tr>
        <tr>
          <th>End time:</th>
          <td class="TestScenarioTableValue">{end_time}</td>
        </tr>
        <tr>
          <th>Total time:</th>
          <td class="TestScenarioTableValue">{total_time} s</td>
        </tr>
        <tr>
          <th>Total tests:</th>
          <td class="TestScenarioTableValue">{total_tests}</td>
        </tr>
        <tr>
          <th>Passed tests:</th>
          <td class="TestScenarioTableValue">{passed_tests}</td>          
        </tr>
        <tr>
          <th>Failed tests:</th>
          <td class="TestScenarioTableValue">{failed_tests}</td>          
        </tr>
        <tr>
          <th>Log:</th>
          <td class="TestScenarioTableValue">{log}</td>          
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
                   log = ts['log'].decode().replace("\n","<br>") 
                  )
        
        ts_opt_rest_all = {}                            
        for opt_dict in ts_opt_rest:
            if opt_dict['key'] not in ts_opt_rest_all:
                ts_opt_rest_all[opt_dict['key']] = {
                                                    'key'   : opt_dict['key'].decode(),
                                                    'value' : opt_dict['value'].decode(),
                                                    'pickled' : opt_dict['pickled'],
                                                    'options' : { } 
                                                   }
            if opt_dict['opt_name'] is not None:    
                ts_opt_rest_all[opt_dict['key']]['options'][opt_dict['opt_name'].decode()] = opt_dict['opt_value'].decode()
        
        if len(ts_opt_rest_all) > 0:            
            res += self._process_custom_data_opt(ts_opt_rest_all, 'TestScenario')
               
        return res
     
    def _process_custom_data_opt(self, opt_dict, td_class):
        """Method processes custom options

        Args:
           opt_dict (dict): options
           td_class (str): TD element class

        Returns:
           str

        """

        res = ""        
        for _,v in opt_dict.items():                            
            if v['pickled'] == 1:
                v['value'] = pickle.loads(opt_dict['value'])
            opt_name = v['key'] if 'label' not in v['options'] else v['options']['label'] 
                
            res += """
                 <tr>
                    <th>{opt_name}</th>
                    <td class="{td_class}TableValue">{opt_value}</td>
                 </tr> 
               """.format(
                          opt_name = opt_name.decode() if hasattr(opt_name, 'decode') else opt_name, 
                          opt_value = v['value'].decode() if hasattr(v['value'], 'decode') else v['value'],
                          td_class = td_class
                          )
        return res
               
    def get_test_results(self, test_run_id):
        """Method creates test results

        Args:
           test_run_id (str): test run id

        Returns:
           str

        """

        res = ""
        
        test_sets = self._db_con.db_data("get_test_sets", {'test_run_id' : test_run_id })
                   
        for test_set in test_sets:
            test_set_end_time = "Not completed" if int(test_set['end_time']) == -1 else datetime.datetime.fromtimestamp(int(test_set['end_time'])).strftime('%Y-%m-%d %H:%M:%S')
            if 'test_set_node_state' in self._options and self._options['test_set_node_state'].lower() == 'open':
                test_set_button_state_class = "ToggleButtonOn"
                test_set_node_state_class   = "NodeOpen"
                test_set_node_char          = "-"
                  
            else: 
                test_set_button_state_class = 'ToggleButtonOff'
                test_set_node_state_class   = "NodeClosed"
                test_set_node_char          = "+"                 
            res += """<hr>
            
                      <table class="TestSetTable">
                            <caption><div id="{test_set_objid}" class="{test_set_button_state_class}">{test_set_node_char}</div>Test set [{test_set_id}]</caption>
                            <tr>                              
                              <td class="TestSetTableContainer">
                                 <div id="{test_set_objid}_container" class="TestSetTableContainerWrapper {test_set_node_state_class}"> 
                                   <table class="TestSetTableContainerTable">
                                    <tr>
                                       <th>Path:</th>
                                       <td class="TestSetTableValue">{test_set_id}</td>
                                    </tr>            
                                    <tr>
                                       <th>Start time:</th>
                                       <td class="TestSetTableValue">{test_set_start_time}</td>
                                    </tr>
                                    <tr>
                                       <th>End time:</th>
                                       <td class="TestSetTableValue">{test_set_end_time}</td>
                                    </tr>
                                     <tr>
                                       <th>Total time:</th>
                                       <td class="TestSetTableValue">{test_set_total_time} s</td>
                                    </tr>
                                    <tr>
                                       <th>Total tests:</th>
                                       <td class="TestSetTableValue">{test_set_total_tests}</td>
                                    </tr>
                                    <tr>
                                       <th>Passed tests:</th>
                                       <td class="TestSetTableValue">{test_set_passed_tests}</td>
                                    </tr>
                                    <tr>
                                       <th>Failed tests:</th>
                                       <td class="TestSetTableValue">{test_set_failed_tests}</td>
                                    </tr>
                                    <tr>
                                       <th>Log:</th>
                                       <td class="TestSetTableValue">{test_set_log}</td>
                                    </tr>                                                       
                        """.format(

                                   test_set_objid            = test_set['id'].decode() if hasattr(test_set['id'], 'decode') else test_set['id'],
                                   test_set_node_state_class = test_set_node_state_class,
                                   test_set_button_state_class = test_set_button_state_class, 
                                   test_set_node_char        = test_set_node_char,                                  
                                   test_set_id               = test_set['tset_id'].decode() if hasattr(test_set['tset_id'], 'decode') else test_set['tset_id'],
                                   test_set_start_time       = datetime.datetime.fromtimestamp(int(test_set['start_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                                   test_set_end_time         = test_set_end_time,
                                   test_set_total_time       = 0 if int(test_set['end_time']) == -1 else round(test_set['end_time'] - test_set['start_time'],3),
                                   test_set_total_tests      = test_set['total_tests'],
                                   test_set_passed_tests     = test_set['passed_tests'],                                   
                                   test_set_failed_tests     = test_set['failed_tests'],
                                   test_set_log              = test_set['log'].decode().replace("\n","<br>"),

                                 )
                        
            test_scenarios = self._db_con.db_data("get_test_scenarios", {'test_run_id' : test_run_id, 'test_set_id' : test_set['id'].decode() })                                                             
            for ts in test_scenarios:
                ts_opt = self._db_con.db_data("get_test_custom_opt", {'test_object_id' : ts['id']})
                
                if 'test_scenario_node_state' in self._options and self._options['test_scenario_node_state'].lower() == 'open':
                    test_scenario_button_state_class = "ToggleButtonOn"
                    test_scenario_node_state_class   = "NodeOpen"
                    test_scenario_node_char          = "-"
                      
                else:
                    test_scenario_button_state_class = 'ToggleButtonOff'
                    test_scenario_node_state_class   = "NodeClosed"
                    test_scenario_node_char          = "+"
                                  
                res += """<tr>
                            <td class="TestSet_TestScenarioNode">&nbsp;</td>
                            <td class="TestSet_TestScenarioNodeContainer">                                
                                <table class="TestScenarioTable">
                                    <caption><div id="{test_scenario_objid}" class="{test_scenario_button_state_class}">{test_scenario_node_char}</div>Test Scenario [{ts_id}\\{ts_name}]</caption>
                                    <tr>
                                       <td class="TestScenarioTableContainer">
                                           <div id="{test_scenario_objid}_container" class="TestSet_TestScenarioNodeContainerWrapper {test_scenario_node_state_class}">
                                              <table class="TestScenarioTableContainerTable"> 
                                                {ts_opt}
                                                <tr>
                                                   <td class="TestScenario_TestCaseNode">&nbsp;</td>
                                                   <td class="TestScenario_TestCaseNodeContainer">
                       """.format(

                                   test_scenario_objid              = ts['id'].decode() if hasattr(ts['id'], 'decode') else ts['id'],
                                   test_scenario_node_state_class   = test_scenario_node_state_class,
                                   test_scenario_button_state_class = test_scenario_button_state_class,
                                   test_scenario_node_char          = test_scenario_node_char,
                                   ts_id                            = ts['ts_id'].decode() if hasattr(ts['ts_id'], 'decode') else ts['ts_id'],
                                   ts_name                          = ts['value'].decode() if hasattr(ts['value'], 'decode') else ts['value'],
                                   ts_opt                           = self._format_custom_ts_opt(ts, ts_opt)
                                 )
                test_cases = self._db_con.db_data("get_test_cases", {'test_run_id' : test_run_id, 'test_set_id' : test_set['id'].decode(), 'test_scenario_id' : ts['id'].decode() })                
                for tca in test_cases: 
                    tca_opt = self._db_con.db_data("get_test_custom_opt", {'test_object_id' : tca['id']})
                    
                    if 'test_case_node_state' in self._options and self._options['test_case_node_state'].lower() == 'open':
                        test_case_button_state_class = "ToggleButtonOn"
                        test_case_node_state_class   = "NodeOpen"
                        test_case_node_char          = "-"
                      
                    else:
                        test_case_button_state_class = 'ToggleButtonOff'
                        test_case_node_state_class   = "NodeClosed"
                        test_case_node_char          = "+"  
                    res += """      
                                          <table class="TestCaseTable">
                                            <caption><div class="ToggleButton">{test_case_node_char}</div>Test Case [{tca_id}\\{tca_name}]</caption>
                                             {tc_opt}
                                             <tr>
                                               <td class="TestCase_TestConditionNode">&nbsp;</td>
                                               <td class="TestCase_TestConditionNode">                                      
                          """.format(
                                     tc_opt              = self._format_custom_tc_opt(tca, tca_opt),
                                     tca_id              = tca['tca_id'].decode(),
                                     test_case_node_char = test_case_node_char,
                                     tca_name            = tca['value'].decode() 
                                    )
                    test_conditions = self._db_con.db_data("get_test_conditions", {'test_run_id' : test_run_id, 'test_set_id' : test_set['id'].decode(), 'test_scenario_id' : ts['id'].decode(), 'test_case_id' : tca['id'].decode() })        
                    for tco in test_conditions:
                        tco_opt = self._db_con.db_data("get_test_custom_opt", {'test_object_id' : tco['id'].decode()})                        
                        res += """      
                                          <table class="TestConditionTable">
                                            <caption><div class="ToggleButton">-</div>Test Condition [{tco_id}\\{tco_name}]</caption>
                                             {tco_opt}                                             
                                          </table>                                          
                               """.format(
                                          tco_opt  = self._format_custom_tco_opt(tco, tco_opt),
                                          tco_id   = tco['tco_id'].decode(),
                                          tco_name = tco['value'].decode()
                                         )                                      
                    #End of test cases             
                    res +=  """
                           </td>
                         </tr>
                       </table>                                                                                 
                    """      
                #End of test scenarios             
                res +=  """     </tr>
                               </table>
                             </div>
                           </td>
                         </tr>                                             
                       </table>
                    </td>
                </tr>              
                    """ 
            #end of test set          
            res +=  """
                               </table>
                              </td>
                             </tr>
                            </div>
                           </td>
                         </tr>                                             
                       </table>              
                    """ 
        #TODO implement rest of the info
        
            res += """
              </table> 
              </td>
              </tr>    
            </table>"""   
        return res;    
