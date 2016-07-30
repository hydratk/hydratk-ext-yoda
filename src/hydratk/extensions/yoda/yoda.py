# -*- coding: utf-8 -*-
"""Providing automated testing functionality

.. module:: yoda.yoda
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
yoda_on_check_results
yoda_before_append_helpers_dir
yoda_before_append_lib_dir
yoda_before_parse_test_file
yoda_before_exec_ts_prereq
yoda_before_exec_tco_test
yoda_before_exec_validate_test
yoda_before_exec_ts_postreq

"""
import os
import yaml
import traceback
import sys
import time
from hydratk.core import extension
from hydratk.core import event
from hydratk.core import const
from hydratk.lib.console.commandlinetool import CommandlineTool
from hydratk.extensions.yoda.testengine import TestEngine
from hydratk.extensions.yoda.testresults.testresults import TestResultsDB
from hydratk.extensions.yoda.testresults.testresults import TestResultsOutputFactory
from hydratk.lib.debugging.simpledebug import dmsg
from hydratk.extensions.yoda.testobject import BreakTestRun
from hydratk.extensions.yoda.testobject import BreakTestSet


class Extension(extension.Extension):
    """Class Extension
    """
    
    _test_repo_root                      = None
    _templates_repo                      = None
    _helpers_repo                        = None
    _libs_repo                           = None
    _test_run                            = None
    _current_test_base_path              = None 
    _use_helpers_dir                     = []
    _use_lib_dir                         = []    
    _test_engine                         = None    
    _test_results_db                     = None
    _test_results_output_create          = True
    _test_results_output_handler         = ['console'] 
    _run_mode               = const.CORE_RUN_MODE_SINGLE_APP
    _pp_attr                = {
                                'test_run_started'   : False,
                                'test_run_completed' : False                               
                              }
    _active_tickets         = []    
    
    def __getstate__(self):        
        return self.__dict__
    
    def __setstate__(self, d): self.__dict__.update(d)

    def _init_extension(self):
        """Method initializes extension
        
        Args: 
           none 
           
        Returns:
           void
                
        """ 
           
        self._ext_id      = 'yoda'        
        self._ext_name    = 'Yoda'
        self._ext_version = '0.2.1'
        self._ext_author  = 'Petr Czaderna <pc@hydratk.org>'
        self._ext_year    = '2014 - 2016'
        
        self._run_mode    = self._mh.run_mode #synchronizing run mode
        if int(self._mh.cfg['Extensions']['Yoda']['test_results_output_create']) in (0,1):
            self._test_results_output_create = bool(int(self._mh.cfg['Extensions']['Yoda']['test_results_output_create']))
        if type(self._mh.cfg['Extensions']['Yoda']['test_results_output_handler']).__name__ == 'list':
            self._test_results_output_handler = self._mh.cfg['Extensions']['Yoda']['test_results_output_handler']
             
        self._init_repos()          
        
    def _check_dependencies(self):
        return True
    
    def _init_repos(self):
        """Method initializes test repositories
        
        Configuration option Extensions/Yoda/test_repo_root
        lib - low level auxiliary test methods
        helpers - high level auxiliary test methods
        yoda-tests - test scripts
        
        Args:  
           none
           
        Returns:
           void
                
        """ 
                
        self._test_repo_root = self._mh.cfg['Extensions']['Yoda']['test_repo_root']
        self._libs_repo      = self._mh.cfg['Extensions']['Yoda']['test_repo_root'] + '/lib'
        self._templates_repo = self._mh.cfg['Extensions']['Yoda']['test_repo_root'] + '/yoda-tests/'
        self._helpers_repo   = self._mh.cfg['Extensions']['Yoda']['test_repo_root'] + '/helpers'
        dmsg = '''
        Init repos: test_repo_root: {0}
                    libs_repo: {1}
                    templates_repo: {2}
                    helpers_repo: {3}
        '''.format(self._test_repo_root, self._libs_repo, self._templates_repo, self._helpers_repo)
        self._mh.dmsg('htk_on_debug_info', dmsg, self._mh.fromhere())
    
    def _update_repos(self):
        """Method updates test repositories
        
        Args:  
           none
           
        Returns:
           void
                
        """ 
                
        self._libs_repo      = self._test_repo_root + '/lib'
        self._templates_repo = self._test_repo_root + '/yoda-tests/'
        self._helpers_repo   = self._test_repo_root + '/helpers'
        dmsg = '''
        Update repos: test_repo_root: {0}
                    libs_repo: {1}
                    templates_repo: {2}
                    helpers_repo: {3}
        '''.format(self._test_repo_root, self._libs_repo, self._templates_repo, self._helpers_repo)
        self._mh.dmsg('htk_on_debug_info', dmsg, self._mh.fromhere())
            
    def _do_imports(self):
        pass                 
    
    #def __getstate__(self):
    #    odict = self.__dict__.copy() # copy the dict since we change it
    #    odict['_mh'] = None              # remove filehandle entry
    #    return odict

    #def __setstate__(self, d):
    #    self.__dict__.update(d)
        
    def _register_actions(self): 
        """Method registers event hooks
        
        Args:  
           none
           
        Returns:
           void
                
        """ 
                              
        hook = [
                {'event' : 'htk_on_cmd_options', 'callback' : self.init_check },
                {'event' : 'yoda_before_init_tests', 'callback' : self.check_test_results_db },
                {'event' : 'htk_on_cworker_init', 'callback' : self.pp_actions },
                {'event' : 'htk_after_load_extensions', 'callback' : self.check_pp_mode },                                               
               ]            
                
        self._mh.register_event_hook(hook)
        if self._mh.cli_cmdopt_profile == 'yoda':
            self._register_standalone_actions()             
        else:
            self._register_htk_actions()
             
        self._test_engine = TestEngine()
    
    #def __getinitargs__(self):
    #    return (None,)
                                
    def check_pp_mode(self, ev):
        """Method registers event hooks for parallel processing 
        
        Args:  
           none
           
        Returns:
           void
                
        """ 
                
        if self._mh.run_mode == const.CORE_RUN_MODE_PP_APP:
            hook = [{'event' : 'htk_on_cobserver_ctx_switch', 'callback' : self.pp_app_check },
                    #{'event' : 'htk_on_cobserver_ctx_switch', 'callback' : self.pp_app_check2 }
                   ]
            self._mh.register_event_hook(hook)           
            #self._mh.register_async_fn('pp_test', worker1)
            #self._mh.register_async_fn_ex('pp_test2',worker2, Extension.worker_result)
            self.init_libs()                   
            self.init_helpers()
         
    def _register_htk_actions(self):
        """Method registers command hooks
        
        Args:  
           none        
           
        Returns:
           void
           
        """ 
                
        dmsg("Registering htk actions")
        self._mh.match_cli_command('yoda-run')              
        self._mh.match_cli_command('yoda-simul')
        self._mh.match_cli_command('yoda-create-test-results-db')
        
        hook = [
                {'command' : 'yoda-run', 'callback' : self.init_tests },                
                {'command' : 'yoda-simul', 'callback' : self.init_test_simul },
                {'command' : 'yoda-create-test-results-db', 'callback' : self.create_test_results_db }
               ]  
       
            
        self._mh.register_command_hook(hook)
        
        self._mh.match_long_option('yoda-test-path', True, 'yoda-test-path')
        self._mh.match_long_option('yoda-test-repo-root-dir', True, 'yoda-test-repo-root-dir')      
        self._mh.match_long_option('yoda-db-results-dsn', True, 'yoda-db-results-dsn')
        self._mh.match_long_option('yoda-test-run-name', True, 'yoda-test-run-name')
        self._mh.match_long_option('yoda-test-results-output-create', True, 'yoda-test-results-output-create')
        self._mh.match_long_option('yoda-test-results-output-handler', True, 'yoda-test-results-output-handler')
          
    
    def _register_standalone_actions(self):
        """Method registers command hooks for standalone mode
        
        Args:  
           none
           
        Returns:
           void
                
        """ 
                
        dmsg("Registering standalone actions")
        option_profile = 'yoda'
        help_title       = '{h}' + self._ext_name + ' v' + self._ext_version + '{e}'
        cp_string        = '{u}' + "(c) "+ self._ext_year +" "+ self._ext_author  + '{e}'
        self._mh.set_cli_appl_title(help_title, cp_string)
        
        self._mh.match_cli_command('run', option_profile)              
        self._mh.match_cli_command('simul',option_profile)
        self._mh.match_cli_command('create-test-results-db',option_profile)
        self._mh.match_cli_command('help', option_profile)
      
        hook = [
                {'command' : 'run', 'callback' : self.init_tests },                
                {'command' : 'simul', 'callback' : self.init_test_simul },
                {'command' : 'create-test-results-db', 'callback' : self.create_test_results_db },               
               ]    
            
        self._mh.register_command_hook(hook)
        
        self._mh.match_cli_option(('tp','test-path'), True, 'yoda-test-path', False, option_profile)        
        self._mh.match_cli_option(('rd','test-repo-root-dir'), True, 'yoda-test-repo-root-dir', False, option_profile) 
        self._mh.match_cli_option(('oc','test-results-output-create'), True, 'yoda-test-results-output-create', False, option_profile)
        self._mh.match_cli_option(('oh','test-results-output-handler'), True, 'yoda-test-results-output-handler', False, option_profile)
        self._mh.match_long_option('db-results-dsn', True, 'yoda-db-results-dsn', False, option_profile)
        self._mh.match_cli_option(('rn','test-run-name'), True, 'yoda-test-run-name', False, option_profile)        
        self._mh.match_cli_option(('c','config'), True, 'config', False, option_profile)
        self._mh.match_cli_option(('d','debug'), True, 'debug', False, option_profile)   
        self._mh.match_cli_option(('e','debug-channel'), True, 'debug-channel', False, option_profile)
        self._mh.match_cli_option(('l','language'), True, 'language', False, option_profile)
        self._mh.match_cli_option(('m','run-mode'), True, 'run-mode', False, option_profile)
        self._mh.match_cli_option(('f','force'), False, 'force', False, option_profile)
        self._mh.match_cli_option(('i','interactive'), False, 'interactive', False, option_profile)
    
    def pp_actions(self,ev):
        pass
         
    def pp_app_check(self, ev):
        """Method ensures test run completion when all parallel execution are completed
        
        Args:  
           ev (obj): not used
           
        Returns:
           void
           
        Raises:
           exception: Exception
           event: yoda_before_check_results
                
        """ 
                
        dmsg("Got context switch, active tickets: {0}".format(len(self._active_tickets)))
        if len(self._active_tickets) > 0:
            for index, ticket_id in enumerate(self._active_tickets):
                dmsg("Checking ticket_id {0}".format(ticket_id))
                if self._mh.async_ticket_completed(ticket_id):
                    self._mh.delete_async_ticket(ticket_id)
                    del self._active_tickets[index]
                else:
                    dmsg("There're still {0} wating tickets".format(len(self._active_tickets)))
                    
        else:
            self._pp_attr['test_run_completed'] = True
            try:
                self._test_engine.test_run.end_time = time.time()                    
                self._test_engine.test_run.update_db_record()
                self._test_engine.test_run.write_custom_data()
            except:
                print(sys.exc_info())
                ex_type, ex, tb = sys.exc_info()
                traceback.print_tb(tb)
                raise Exception('Failed to update test_run database record')
            ev = event.Event('yoda_before_check_results')        
            self._mh.fire_event(ev)                           
            if ev.will_run_default(): 
                self._check_results()
            self._mh.stop_pp_app()
            
              
    def create_test_results_db(self):
        """Method creates results database
        
        Args: 
           none 
           
        Returns:
           obj: database
                
        """ 
                
        dsn = self._mh.ext_cfg['Yoda']['db_results_dsn']
        dmsg("Create db results dsn: {0}".format(dsn))
        trdb = TestResultsDB(dsn)
        trdb.create_database()
        return trdb
        
    def init_check(self, ev):
        """Event listener waiting for htk_on_cmd_options event
           
           If there's --yoda-test-repo-root-dir parameter presence, it will try to override current settings
        
        Args:
           ev (object): hydratk.core.event.Event
           
        Returns:
           void
        
        """             
        test_repo = CommandlineTool.get_input_option('yoda-test-repo-root-dir')             
        if test_repo != False and os.path.exists(test_repo) and os.path.isdir(test_repo):
            self._test_repo_root = test_repo    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_test_repo_root_override',test_repo), self._mh.fromhere())
            self._update_repos()
                
        test_results_output_create = CommandlineTool.get_input_option('yoda-test-results-output-create')
        if test_results_output_create != False and int(test_results_output_create) in (0,1):
            self._mh.ext_cfg['Yoda']['test_results_output_create']  = int(test_results_output_create)
            self._test_results_output_create = bool(int(test_results_output_create))
            dmsg("Overriding test results output create settings with: {0}".format(self._mh.ext_cfg['Yoda']['test_results_output_create'] ),3) 
        
        test_results_output_handler = CommandlineTool.get_input_option('yoda-test-results-output-handler')
        if test_results_output_handler != False and int(test_results_output_handler) in (0,1):
            self._mh.ext_cfg['Yoda']['test_results_output_handler']  = int(test_results_output_handler)
            self._test_results_output_handler = bool(int(test_results_output_handler))
            dmsg("Overriding test results output handler settings with: {0}".format(self._mh.ext_cfg['Yoda']['test_results_output_handler'] ),3) 
            
        db_results_dsn = CommandlineTool.get_input_option('yoda-db-results-dsn')
        if db_results_dsn != False and db_results_dsn not in (None,''):
            self._mh.ext_cfg['Yoda']['db_results_dsn']  = db_results_dsn
            dmsg("Overriding database test results dsn with: {0}".format(self._mh.ext_cfg['Yoda']['db_results_dsn'] ),3) 
            
        test_run_name = CommandlineTool.get_input_option('yoda-test-run-name')
        if test_run_name != False:
            self._test_engine.test_run.name = test_run_name                   
    
    def init_test_simul(self):    
        """Method enables simulated execution
        
        Args:  
           none
           
        Returns:
           void
                
        """ 
                    
        self._test_engine.test_simul_mode = True              
        self.init_tests()    
    
    def init_test_results_db(self):  
        """Method initialized results database
        
        Configuration option - Yoda/db_results_dsn
        
        Args:  
           none
           
        Returns:
           void
    
        Raises:
           exception: Exception
                
        """ 
                      
        dsn = self._mh.ext_cfg['Yoda']['db_results_dsn']                  
        dmsg("Initializing test results database, dsn: {0}".format(dsn))            
        trdb = TestResultsDB(dsn)            
        if trdb.db_check_ok() == False:
            raise Exception("Required test results database not available dsn: {0} check failed".format(dsn))
        else:
            dmsg("Test result database dsn: {0} check ok.".format(dsn))
            self._test_engine.test_results_db = trdb
                    
    def check_test_results_db(self, ev):        
        """Method check if results database is successfully created
        
        Configuration option - Yoda/db_results_autocreate
        It is created if autocreate enabled
        
        Args:  
           ev: not used
           
        Returns:
           void
           
        Raises:
           exception: Exception
                
        """                 
        
        dsn = self._mh.ext_cfg['Yoda']['db_results_dsn']                  
        dmsg("Initializing test results database, dsn: {0}".format(dsn))            
        trdb = TestResultsDB(dsn)            
        if trdb.db_check_ok() == False:
            if int(self._mh.ext_cfg['Yoda']['db_results_autocreate']) == 1:
                try:
                    dmsg("Create db results dsn: {0}".format(dsn))
                    trdb.create_database()
                    self._test_engine.test_results_db = trdb
                except:
                    print(str(sys.exc_info()))                       
            else:
                raise Exception("Required test results database not available dsn: {0} check failed".format(dsn))
        else:
            dmsg("Test result database dsn: {0} check ok.".format(dsn))
            self._test_engine.test_results_db = trdb

             
    def init_tests(self):
        """Method is initializing tests 
        
        Args:
           none
        
        Returns:
           void
           
        Raises:
           event: yoda_before_init_tests
           event: yoda_before_process_tests     
           event: yoda_before_check_results     
                  
        """
        
        self._test_engine.test_repo_root = self._test_repo_root
        self._test_engine.libs_repo      =  self._libs_repo
        self._test_engine.templates_repo = self._templates_repo
        self._test_engine.helpers_repo   = self._helpers_repo
                 
        ev = event.Event('yoda_before_init_tests')        
        self._mh.fire_event(ev)                    
        if ev.will_run_default():     
            test_path = CommandlineTool.get_input_option('yoda-test-path')            
            if test_path == False:
                test_path = ''           
                                
            self.init_libs()                     
            self.init_helpers()
            if test_path != '' and test_path[0] == '/': # global test set
                self._test_engine.run_mode_area = 'global'                
                self._mh.dmsg('htk_on_debug_info', 'Running test set {0} out of the workspace'.format(test_path), self._mh.fromhere())
            else:                
                self._test_engine.run_mode_area = 'inrepo'                    
                test_path                       = self._templates_repo + test_path                
                self._mh.dmsg('htk_on_debug_info', 'Running test sets in repository: {0}'.format(test_path), self._mh.fromhere())                                                  
                                          
            test_files = self._test_engine.get_all_tests_from_path(test_path)
                            
            ev = event.Event('yoda_before_process_tests', test_files)        
            if (self._mh.fire_event(ev) > 0):
                test_files = ev.argv(0)
            if ev.will_run_default():
                self.process_tests(test_files)
                
            if self._mh.run_mode == const.CORE_RUN_MODE_SINGLE_APP:
                ev = event.Event('yoda_before_check_results')        
                self._mh.fire_event(ev)                           
                if ev.will_run_default(): 
                    self._check_results()
             
    
    def init_global_tests(self,test_base_path):        
        pass
    
    def init_inrepo_tests(self, test_base_path):      
        
        if os.path.exists(self._test_repo_root):
            if os.path.exists(self.test_base_path):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_start_test_from', test_base_path), self._mh.fromhere())
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('yoda_invalid_test_base_path', self._current_test_base_path), self._mh.fromhere())                
        else:           
            self._mh.dmsg('htk_on_error', self._mh._trn.msg(' yoda_invalid_test_repo_root', self._test_repo_root), self._mh.fromhere())      
    
    def init_helpers(self):  
        """Method initializes helpers repository
        
        Args:
           none
        
        Returns:
           void
           
        Raises:
           event: yoda_before_append_helpers_dir  
                  
        """              

        self._use_helpers_dir.append(self._helpers_repo)  
        ev = event.Event('yoda_before_append_helpers_dir', self._use_helpers_dir)        
        if (self._mh.fire_event(ev) > 0):
            self._use_helpers_dir = ev.argv(0)
        if ev.will_run_default():
            if isinstance(self._use_helpers_dir, list):
                for helpers_dir in self._use_helpers_dir:
                    '''TODO also check with warning helpers_dir/__init__.py presence to see if it's proper package directory'''    
                    if os.path.exists(helpers_dir):
                        sys.path.append(helpers_dir)                         
                        self._mh.dmsg('htk_on_debug_info',self._mh._trn.msg('yoda_added_helpers_dir', helpers_dir), self._mh.fromhere())                        
                    else:
                        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_helpers_dir_not_exists', helpers_dir), self._mh.fromhere())                             
    
    def init_libs(self):        
        """Method initializes libraries repository
        
        Args:
           none
        
        Returns:
           void
           
        Raises:
           event: yoda_before_append_lib_dir  
                  
        """ 
        
        self._use_lib_dir.append(self._libs_repo)  
        ev = event.Event('yoda_before_append_lib_dir', self._use_lib_dir)        
        if (self._mh.fire_event(ev) > 0):
            self._use_lib_dir = ev.argv(0)
        if ev.will_run_default():
            if isinstance(self._use_lib_dir, list):
                for lib_dir in self._use_lib_dir:
                    '''TODO also check with warning lib_dir/__init__.py presence to see if it's proper package directory'''    
                    if os.path.exists(lib_dir):
                        sys.path.append(lib_dir)                         
                        self._mh.dmsg('htk_on_debug_info',self._mh._trn.msg('yoda_added_lib_dir', lib_dir), self._mh.fromhere())                        
                    else:
                        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_lib_dir_not_exists',lib_dir), self._mh.fromhere())
                             
    def process_tests(self, test_files):
        """Method determines whether test sets will be executed in single or parallel mode
        
        Args:
           test_files (obj): list or str, test files
        
        Returns:
           void
           
        Raises:
           exception: Exception
           event: yoda_before_parse_test_file  
                  
        """ 
                
        dmsg("Process tests test_simul_mode {0}, run_mode {1}".format(self._test_engine._test_simul_mode, self._mh.run_mode))
        total_ts = len(test_files)
        if total_ts > 0:
            self._test_engine.test_run.total_test_sets = total_ts
            if self._test_engine.have_test_results_db:
                try:                    
                    self._test_engine.test_run.create_db_record()
                except:
                    print(sys.exc_info())
                    raise Exception('Failed to create test_run database record')
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_process_test_sets_total', total_ts), self._mh.fromhere())            
            for tf in test_files:
                if type(tf).__name__ == 'list':
                    for ctf in tf:
                        ev = event.Event('yoda_before_parse_test_file', ctf)        
                        if (self._mh.fire_event(ev) > 0):
                            ctf = ev.argv(0)
                        if ev.will_run_default():
                            try:
                                if self._mh.run_mode == const.CORE_RUN_MODE_SINGLE_APP:                                                                         
                                    self.process_test_set(ctf)
                                else:                                   
                                    self.pp_process_test_set(ctf)
                            except BreakTestSet as exc:
                                dmsg('Received break test set')
                                continue    
                            except BreakTestRun as exc:
                                dmsg('Received break test run')
                                break 
                else:
                    ev = event.Event('yoda_before_parse_test_file', tf)        
                    if (self._mh.fire_event(ev) > 0):
                        tf = ev.argv(0)
                    if ev.will_run_default():                                           
                        try:                                         
                            if self._mh.run_mode == const.CORE_RUN_MODE_SINGLE_APP:                                                                            
                                self.process_test_set(tf)
                            else:                                
                                self.pp_process_test_set(tf)
                        except BreakTestSet as exc:
                            dmsg('Received break test set')
                            continue
                        except BreakTestRun as exc:
                            dmsg('Received break test run')
                            break
                        
            if self._mh.run_mode == const.CORE_RUN_MODE_SINGLE_APP:
                try:
                    self._test_engine.test_run.end_time = time.time()                    
                    self._test_engine.test_run.update_db_record()
                    self._test_engine.test_run.write_custom_data()
                except:
                    print(sys.exc_info())
                    ex_type, ex, tb = sys.exc_info()
                    traceback.print_tb(tb)
                    raise Exception('Failed to update test_run database record')
        else:
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('yoda_no_tests_found_in_path', self._current_test_base_path), self._mh.fromhere())
    
    def pp_process_test_set(self, test_set_file):
        """Method creates ticket to execute test set in parallel mode
        
        Args:
           test_set_file (str): filename
        
        Returns:
           void
                  
        """ 
                
        dmsg("Processing test set {0} in parallel mode".format(test_set_file))
        ticket_id = self._mh.async_ext_fn((self,'pp_run_test_set'), None, test_set_file)
        dmsg("Got ticket id: {0} for test set: {1}".format(ticket_id,test_set_file))
        self._active_tickets.append(ticket_id)
    
    def pp_run_test_set(self, test_set_file):
        """Method executes test set in parallel mode
        
        Args:
           test_set_file (str): filename
        
        Returns:
           void
           
        Raises:
           exception: Exception 
                  
        """ 
                
        self.init_test_results_db()
        dmsg("Processing test set {0}".format(test_set_file), 1)
        tset_struct = self._test_engine.load_tset_from_file(test_set_file)
        if tset_struct != False:                    
            tset_obj = self._test_engine.parse_tset_struct(tset_struct);
            self._test_engine.test_run.norun_tests += tset_obj.parsed_tests['total_tco']
            if tset_obj != False:
                if self._test_engine.have_test_results_db:
                    try:
                        dmsg("Creating test set {0} database record".format(test_set_file), 1)                    
                        tset_obj.create_db_record()
                    except:
                        print(sys.exc_info())
                        raise Exception('Failed to create test_set database record')
                else:
                    raise Exception("No test results database")
                tset_obj.run()
                
                if self._test_engine.have_test_results_db:
                    try: 
                        tset_obj.end_time = time.time()                   
                        tset_obj.update_db_record()
                        tset_obj.write_custom_data()
                    except:
                        print(sys.exc_info())
                        raise Exception('Failed to update test_set database record')
        else:
            raise Exception("Failed to load tset_struct")
        
    def process_test_set(self,test_set_file):
        """Method executes test set in single mode
        
        Args:
           test_set_file (str): filename
        
        Returns:
           void
           
        Raises:
           exception: Exception 
                  
        """ 
                
        tset_struct = self._test_engine.load_tset_from_file(test_set_file)
        if tset_struct != False:                    
            tset_obj = self._test_engine.parse_tset_struct(tset_struct);
            self._test_engine.test_run.norun_tests += tset_obj.parsed_tests['total_tco']
            if tset_obj != False:
                if self._test_engine.have_test_results_db:
                    try:                    
                        tset_obj.create_db_record()
                    except:
                        print(sys.exc_info())
                        raise Exception('Failed to create test_set database record')
                
                tset_obj.run()
                
                if self._test_engine.have_test_results_db:
                    try: 
                        tset_obj.end_time = time.time()                   
                        tset_obj.update_db_record()
                        tset_obj.write_custom_data()
                    except:
                        print(sys.exc_info())
                        raise Exception('Failed to update test_set database record')
                    
 
    
    def _check_results(self):  
        """Method prepares results in requested format
        
        Args:
           none
        
        Returns:
           void
           
        Raises:
           event: yoda_on_check_results 
                  
        """ 
                      
        ev = event.Event('yoda_on_check_results', self._test_engine.test_run.id)
        self._mh.fire_event(ev)
        if ev.will_run_default():
            if self._test_results_output_create == True:                
                for output_handler in self._test_results_output_handler:   
                    trof = TestResultsOutputFactory(self._mh.ext_cfg['Yoda']['db_results_dsn'], output_handler)
                    trof.create(self._test_engine.test_run)
        