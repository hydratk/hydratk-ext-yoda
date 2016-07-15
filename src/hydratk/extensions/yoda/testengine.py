# -*- coding: utf-8 -*-
"""Providing automated testing functionality

.. module:: yoda.testengine
   :platform: Unix
   :synopsis: Providing automated testing functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os
import sys
from hydratk.core.masterhead import MasterHead
from hydratk.core.event import Event
import yaml
from hydratk.extensions.yoda import testobject
import pprint
import re
import time
import traceback
from xtermcolor import colorize
from hydratk.lib.system import fs
from hydratk.lib.debugging.simpledebug import dmsg

class This(object):
    """Class This
    """
    
    _obj = None
    
    def __init__(self, map_obj=None):    
        """Class constructor
        
        Called when object is initialized
        
        Args:   
           map_obj (obj): test object     
                
        """   
                            
        if map_obj is not None:
            self._obj = map_obj
    
    def __setattr__(self, name, value):
        """Method sets attribute
        
        Args:   
           name (str): attribute name
           value (obj): attribute value    
           
        Returns:
           void
                
        """   
                
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            setattr(self._obj, name, value)
    
    def __getattr__(self, name):
        """Method gets attribute
        
        Args:   
           name (str): attribute name   
           
        Returns:
           obj: attribute value
           
        Raises:
           error: AttributeError
                
        """ 
                
        if hasattr(self._obj, name):
            f = getattr(self._obj, name)
            if hasattr(f, '__call__'):
                return self._obj[name]
            else:
                return f                  
        else: raise AttributeError('Undefined attribute "{0}"'.format(name))       

class Current(object):
    """Class Current
    """
    
    _tset  = None
    _ts    = None
    _tca   = None
    _tco   = None
    _te    = None    
    
    
    def __init__(self):
        pass

    @property
    def te(self):
        """ te property getter, setter """
        
        return self._te

    @te.setter
    def te(self, te):
        """ te property setter """
        
        self._te = te
    
    @property
    def test_set(self):
        """ test_set property getter, setter """
        
        return self._tset

    @test_set.setter
    def test_set(self, tset):
        """ test_set property setter """
        
        self._tset = tset
    
    @property
    def tset(self):
        """ tset property getter, setter """
        
        return self._tset

    @tset.setter
    def tset(self, tset):
        """ tset property setter """
        
        self._tset = tset     
    
    @property
    def test_scenario(self):
        """ test_scenarion property getter """
        
        return self._ts
    
    @property
    def ts(self):
        """ ts property getter, setter """
        
        return self._ts
   
    @ts.setter
    def ts(self, ts):
        """ ts property setter """
        
        self._ts = ts 
        
    @property
    def test_case(self):
        """ test_case property getter """
        
        return self._tca
        
    @property
    def tca(self):
        """ tca property getter, setter """
        
        return self._tca
    
    @tca.setter
    def tca(self, tca):
        """ tca property setter """
        
        self._tca = tca 
    
    @property
    def test_condition(self):
        """ test_condition property getter """
        
        return self._tco
        
    @property
    def tco(self):
        """ tco property getter, setter """
        
        return self._tco
    
    @tco.setter
    def tco(self, tco):
        """ tco property setter """ 
        
        self._tco = tco 

    
class Parent(object):
    """Class Parent
    """
    
    _tset  = None
    _ts    = None
    _tca   = None    
    
    
    def __init__(self):
        pass
    
    @property
    def test_set(self):
        """ test_property getter, setter """
        
        return self._tset

    @test_set.setter
    def test_set(self, tset):
        """ test_set property setter """
        
        self._tset = tset
    
    @property
    def tset(self):
        """ tset property getter, setter """
        
        return self._tset

    @tset.setter
    def tset(self, tset):
        """ tset property setter """
        
        self._tset = tset     
    
    @property
    def test_scenario(self):
        """ test_scenarion property getter """
        
        return self._ts
    
    @property
    def ts(self):
        """ ts property getter, setter """
        
        return self._ts
   
    @ts.setter
    def ts(self, ts):
        """ ts proeprty setter """
        
        self._ts = ts 
        
    @property
    def test_case(self):
        """ test_case property getter """
        
        return self._tca
        
    @property
    def tca(self):
        """ tca property getter, setter """
        
        return self._tca
    
    @tca.setter
    def tca(self, tca):
        """ tca property setter """
        
        self._tca = tca 
        
class TestSet(testobject.TestSet):
    """Class TestSet
    """
    
    _ts = []
   
    def append_ts(self, ts_obj):
        """Method adds new scenario to test set
        
        Args:   
           ts_obj (obj): test scenario 
           
        Returns:
           void
                
        """     
            
        if isinstance(ts_obj, TestScenario):
            self._ts.append(ts_obj)
            
class TestScenario(testobject.TestScenario):
    """Class TestScenario
    """
    
    _tca = []
    _next = None
    
    def repeat(self):
        """Method enables scenario to be repeated
        
        Args:  
           none 
           
        Returns:
           void
                
        """ 
                
        self._action = 'repeat' 
        
    def append_tca(self, tca):
        """Method adds new test case to test scenario
        
        Args:   
           tca (obj): test case   
           
        Returns:
           void
                
        """ 
                
        if isinstance(tca, TestCase):                                   
            self._tca.append(tca)            
        

class TestCase(testobject.TestCase):
    """Class TestCase
    """
    
    _tco = []
    _next = None
    
    def repeat(self):
        """Method enables case to be repeated
        
        Args: 
           none   
           
        Returns:
           void
                
        """ 
                
        self._action = 'repeat' 
    
    def append_tco(self, tco):
        """Method adds new test condition to test case
        
        Args:   
           tco (obj): test condition   
           
        Returns:
           void
                
        """ 
                
        if isinstance(tco, TestCondition):
            self._tco.append(tco)
            
class TestCondition(testobject.TestCondition):
    """Class TestCondition
    """
    
    _next = None
    
    def repeat(self):
        """Method enables condition to be repeated
        
        Args:   
           none
           
        Returns:
           void
                
        """ 
                
        self._action = 'repeat'     


class MacroParser(object):
    """Class MacroParser
    """
    
    _hooks = {}
    
    def mp_add_hooks(self, *args, **kwargs): 
        """Method registers macro hooks
        
        Macro is identified by name and contains callback
        
        Args:   
           args (args): arguments
           kwargs (kwargs): key value arguments   
           
        Returns:
           void
                
        """ 
                       
        for hdata in args:
            for mdef,cb in hdata.items():
                if type(mdef).__name__ == 'str' and mdef != '' and callable(cb):
                    self._hooks[mdef] = cb  
                    
        for mdef, cb in kwargs.items():
            if type(mdef).__name__ == 'str' and mdef != '' and callable(cb):
                self._hooks[mdef] = cb    
    
    def mp_add_hook(self, name, cb):
        """Method registers macro hook

        Args:   
           name (str): macro
           cb (callable): callback  
           
        Returns:
           void
                
        """ 
                
        if type(name).__name__ == 'str' and callable(cb):
            self._hooks[name] = cb
    
    def mp_parse(self, content):
        """Method parses macro string
        
        Args:   
           content (str): macro string 
           
        Returns:
           obj: regexp group
                
        """ 
                
        return re.sub(r'#<<(.*)::(.*)>>#',self._mp_processor,content)
    
    def _mp_processor(self, match):
        """Method executes macro
        
        Args:   
           match (obj): regexp group
           
        Returns:
           obj: callback result
           str: when macro is not defined
                
        """ 
                
        mdef = match.group(1).strip()
        mval = match.group(2).strip()
        if mdef in self._hooks:
            return self._hooks[mdef](mval)
        else: return '<<{mdef} is undefined>>'.format(mdef=mdef) 
        
        
class TestEngine(MacroParser):
    """Class TestEngine
    """
    
    _mh              = None
    _test_run        = False
    _exec_level      = 1
    _tset_struct     = None
    _tset_obj        = None
    _tset_file       = None
    _this            = None
    _parent          = None
    _current         = None
    _test_simul_mode = False
    _code_stack      = None 
    _run_mode_area   = 'inrepo' # available modes: inrepo, global  
    _run_mode_src    = 'folder' # available modes: folder, singlefile
    _ts_filter       = []
    _tca_filter      = []
    _tco_filter      = [] 
    _config          = {
                         'cache.tset.active' : False,
                         'cache.tset.location' : 'inrepo' #possible: inrepo, customdir, memcache                        
                        }
    _test_repo_root       = None
    _libs_repo            = None
    _templates_repo       = None
    _helpers_repo         = None
    _test_file_ext        = ['yoda','jedi']
    _test_template_ext    = ['padavan']
    _test_results_db      = None
    _have_test_results_db = False
    _use_test_results_db  = False
    
    @property
    def code_stack(self):
        """ code_stack property getter """
        
        return self._code_stack
              
    @property
    def test_repo_root(self):
        """ test_repo_root property getter, setter """
        
        return self._test_repo_root
    
    @test_repo_root.setter
    def test_repo_root(self, path):
        """ test_repo_root property setter """
        
        self._test_repo_root = path
    
    @property
    def libs_repo(self):
        """ libs_repo prooperty getter, setter """
        
        return self._libs_repo
    
    @libs_repo.setter
    def libs_repo(self, path):
        """ libs_repo property setter """
        
        self._libs_repo = path
    
    @property
    def templates_repo(self):
        """ templates_repo property getter, setter """
        
        return self._templates_repo
    
    @templates_repo.setter
    def templates_repo(self, path):
        """ templates_repo property setter """
        
        self._templates_repo = path

    @property
    def have_test_results_db(self):
        """ have_test_results_db property getter """
        
        return self._test_results_db is not None
    
    @property
    def test_results_db(self):
        """ test_results_db property getter, setter """
        
        return self._test_results_db
    
    @test_results_db.setter
    def test_results_db(self, db):
        """ test_results_db property setter """
        
        self._test_results_db = db
        self._have_test_results_db = True if self._test_results_db is not None else False
        
    @property
    def helpers_repo(self):
        """ helpers_repo property getter, setter """
        
        return self._helpers_repo
    
    @helpers_repo.setter
    def helpers_repo(self, path):
        """ helpers_repo property setter """
        
        self._helpers_repo = path

    @property
    def ts_filter(self):
        """ ts_filter property getter, setter """
        
        return self._ts_filter;
    
    @ts_filter.setter
    def ts_filter(self, fltr):
        """ ts_filter property setter """
        
        self._ts_filter = fltr
    
    @property
    def tca_filter(self):
        """ tca_filter property getter, setter """
        
        return self._tca_filter;
    
    @tca_filter.setter
    def tca_filter(self, fltr):
        """ tca_filter property setter """
        
        self._tca_filter = fltr
        
    @property
    def tco_filter(self):
        """ tco_filter property getter, setter """
        
        return self._tco_filter;
    
    @tco_filter.setter
    def tco_filter(self, fltr):
        """ tco_filter property setter """
        
        self._tco_filter = fltr
    
    @property
    def run_mode_area(self):
        """ run_mode_area property getter, setter """
                
        return self._run_mode_area
    
    @run_mode_area.setter
    def run_mode_area(self, mode):
        """ run_mode_area property setter """
                
        if mode in ('inrepo','global'):
            self._run_mode_area = mode
    
    @property
    def run_mode_src(self):
        """ run_mode_src property getter, setter """
        
        return self._run_mode_src
    
    @run_mode_src.setter
    def run_mode_src(self, mode):
        """ run_mode_src property setter """
                
        if mode in ('folder','singlefile'):
            self._run_mode_src = mode
    
    @property
    def exec_level(self):   
        """ exec_level property getter """
             
        return self._exec_level
    
    @property
    def test_simul_mode(self):
        """ test_simul_mode property getter, setter """
                
        return self._test_simul_mode
            
    @test_simul_mode.setter
    def test_simul_mode(self, mode):
        """ test_simul_mode property setter """
                
        if mode in (True,False):
            self._test_simul_mode = mode
    
    @property
    def test_run(self):
        """ test_run property getter, setter """
        
        return self._test_run

    @test_run.setter
    def test_run(self, test_run):
        """ test_run property setter """
        
        self._test_run = test_run    
    
    def __init__(self):   
        """Class constructor
        
        Called when object is initialized
        
        Args:   
           none

        """ 
                    
        self._test_run        = testobject.TestRun(self)
        self._tset_struct     = None
        self._tset_obj        = None
        self._tset_file       = None
        self._this            = None
        self._parent          = Parent()
        self._current         = Current()
        self._current.te      = self
        self._mh              = MasterHead.get_head();
        self._test_simul_mode = False 
        self._code_stack      = CodeStack()
        self._run_mode_area   = 'inrepo'
        self._run_mode_src    = 'folder'
        self._ts_filter       = []
        self._tca_filter      = []
        self._tco_filter      = [] 
        self._exec_level      = 1
                
        self.mp_add_hooks({
                          'include' : self._h_include
                        })
    
    def new_test_run(self):
        """Method creates new test run
        
        Args:  
           none 
           
        Returns:
           void
                
        """ 
                
        self._test_run = testobject.TestRun()
        self._current  = Current()
                  
    def _h_include(self, content_file):
        """Method loads content of included file
        
        Args:  
           content_file (str): filename including path
           
        Returns:
           str: content
                
        """ 
                
        if content_file != '' and content_file[0] != '/': # repo
            content_file = self._templates_repo + content_file
       
        if os.path.exists(content_file) and os.path.isfile(content_file):
            result = fs.file_get_contents(content_file)
        else:
            result = '<<include !! {0} file not found>>'.format(content_file) 
        
        return result
            
    def load_tset_from_file(self, tset_file):       
        """Method loads test content from file
        
        Args:  
           tset_file (str): filename including path 
           
        Returns:
           bool: result
                
        """ 
                 
        result = False
        if tset_file != '' and os.path.exists(tset_file):
            tset_str = fs.file_get_contents(tset_file)
            result = self.load_tset_from_str(tset_str, origin_file = True)
            self._tset_file = tset_file          
        return result 
    
    def load_tset_from_str(self, tset_str, origin_file=False):
        """Method loads test set content from string
        
        Args:  
           tset_str (str): test set content
           origin_file (bool): string loaded from file
           
        Returns:
           dict: test set
                
        """ 
                
        tset_struct = False
        if tset_str != '':
            if origin_file == False:
                self._tset_file = '<str>'
            tset_str = self.mp_parse(tset_str) #apply macros            
            tset_struct = yaml.load(tset_str) #tset_struct                 
        return tset_struct
    
    def _parse_ts_node(self, ts_node, ts):
        """Method parses test scenario
        
        Args:  
           ts_node (dict): test scenario node
           ts (obj): test scenario object
           
        Returns:
           void
                
        """ 
                
        for ts_key, ts_val in ts_node.items():
            if not (re.match('Test-Case', ts_key)):
                self._mh.dmsg('htk_on_debug_info',"Parsing Test-Scenario attributes {0}={1}".format(ts_key,ts_val), self._mh.fromhere(), 5)
                #print("Test-Scenario {0}={1}").format(ts_key,ts_val)
                ts.setattr(ts_key.lower(),ts_val)
            
    def _parse_tca_node(self, tca_node, tca):   
        """Method parses test case
        
        Args:  
           tca_node (dict): test case node
           tca (obj): test case object
           
        Returns:
           void
                
        """ 
                     
        for tca_key, tca_val in tca_node.items():
            if not (re.match('Test-Condition', tca_key)):
                self._mh.dmsg('htk_on_debug_info',"Parsing Test-Case attributes {0}={1}".format(tca_key,tca_val), self._mh.fromhere(), 5)                
                tca.setattr(tca_key.lower(),tca_val)
    
    def _parse_tco_node(self, tco_node, tco):
        """Method parses test condition
        
        Args:  
           tco_node (dict): test condition node
           tco (obj): test condition object
           
        Returns:
           void
                
        """ 
                
        for tco_key, tco_val in tco_node.items():
            if tco_key == 'expected-result':
                tco.expected_result = tco_val
            self._mh.dmsg('htk_on_debug_info',"Parsing Test-Condition attributes {0}={1}".format(tco_key,tco_val), self._mh.fromhere(), 5)    
            tco.setattr(tco_key.lower(), tco_val)            
                       
    def parse_tset_struct(self, tset_struct):
        """Method parses test set
        
        Hierarchy test scenario, case, condition
        
        Args:  
           tset_struct (dict): test set structure
           
        Returns:
           obj: test set
                
        """ 
                
        tset_obj = False
        if (type(tset_struct).__name__ == 'dict'):
            tset_obj = TestSet(self._current, self._tset_file)
                                    
            ts_num = 1
            ts_k = 'Test-Scenario-%d' % ts_num
            while ts_k in tset_struct:                
                ts = TestScenario(ts_num, tset_obj, self._current)                               
                self._parse_ts_node(tset_struct[ts_k], ts)
                tset_obj.parsed_tests['total_ts'] += 1
                tca_num = 1
                tca_k = 'Test-Case-%d' % tca_num                
                while tca_k in tset_struct[ts_k]:                    
                    tca = TestCase(tca_num, ts, self._current)                    
                    self._parse_tca_node(tset_struct[ts_k][tca_k], tca)
                    tset_obj.parsed_tests['total_tca'] += 1
                    tco_num = 1
                    tco_k = 'Test-Condition-%d' % tco_num                    
                    while tco_k in tset_struct[ts_k][tca_k]:                                                                   
                        tco = TestCondition(tco_num, tca, self._current)                        
                        self._parse_tco_node(tset_struct[ts_k][tca_k][tco_k], tco)
                        tset_obj.parsed_tests['total_tco'] += 1
                        tco_num += 1
                        tco_k = 'Test-Condition-%d' % tco_num                        
                        tca.append_tco(tco)
                    
                    tca_num += 1
                    tca_k = 'Test-Case-%d' % tca_num                    
                    ts.append_tca(tca)                              
                    
                ts_num += 1
                ts_k = 'Test-Scenario-%d' % ts_num
                tset_obj.append_ts(ts)                
                
            if ts_num == 1:
                print("Test-Scenario-%d tag expected" % ts_num)     
        else:
            print("Wrong tset structure")                            
        
        return tset_obj
    
    def exec_test(self, test_path):
        """Method executes inline test
        
        Args:  
           test_path (str): test path
           
        Returns:
           void
           
        Raises:
           exception: Exception
           event: yoda_before_parse_test_file
                
        """ 
                
        self._exec_level += 1        
        dmsg('Inline test exec: {0}'.format(test_path))
        if test_path is not None and test_path != '':
            if test_path not in self._test_run.inline_tests:
                self._test_run.inline_tests.append(test_path)
            else:
                raise Exception('Inline test execution loop detected on {0}'.format(test_path))    
            self._mh.dmsg('htk_on_debug_info', 'Inline test execution: {0}'.format(test_path), self._mh.fromhere())
            
            backup_tset = self._current.tset
            backup_ts   = self._current.ts
            backup_tca  = self._current.tca
            backup_tco  = self._current.tco
            
            if test_path != '' and test_path[0] == '/': # global test set
                self.run_mode_area = 'global'                
                self._mh.dmsg('htk_on_debug_info', 'Running test set {0} out of the workspace'.format(test_path), self._mh.fromhere())
            else:                
                self.run_mode_area = 'inrepo'                    
                test_path                       = self._templates_repo + test_path                
                self._mh.dmsg('htk_on_debug_info', 'Running test sets in repository: {0}'.format(test_path), self._mh.fromhere())  
            test_files = self.get_all_tests_from_path(test_path)
            self.test_run.total_test_sets += len(test_files)
            
            for tf in test_files:
                ev = Event('yoda_before_parse_test_file', tf)        
                if (self._mh.fire_event(ev) > 0):
                    tf = ev.argv(0)
                if ev.will_run_default():
                    tset_struct = self.load_tset_from_file(tf)
                    if tset_struct != False:                    
                        tset_obj = self.parse_tset_struct(tset_struct);
                        if tset_obj != False:
                            try:
                                dmsg("Creating test set {0} database record".format(tf), 1)                    
                                tset_obj.create_db_record()
                            except:
                                print(sys.exc_info())
                                raise Exception('Failed to create test_set database record')
                            
                            tset_obj.run()
                            
                            try: 
                                tset_obj.end_time = time.time()                   
                                tset_obj.update_db_record()
                                tset_obj.write_custom_data()
                            except:
                                print(sys.exc_info())
                                raise Exception('Failed to update test_set database record')
                            if test_path in self._test_run.inline_tests:
                                self._test_run.inline_tests.remove(test_path)
            
            self._current.tset = backup_tset 
            self._current.ts   = backup_ts
            self._current.tca  = backup_tca 
            self._current.tco  = backup_tco
            self._exec_level  += 1            
    
    def get_all_tests_from_container(self, container_file):
        """Method returns all tests found in container
        
        Args:  
           container_file (str): filename including path
           
        Returns:
           list: tests 
                
        """ 
                
        dmsg('Parsing test container file: {0}'.format(container_file))
        test_files = []
        if os.path.isfile(container_file):
            cdata = fs.file_get_contents(container_file)
            test_path_tok = cdata.split("\n")
            for test_path in test_path_tok:                
                test_path = test_path.strip() #remove unwanted whitespace characters
                dmsg('Processing test container content: {0}'.format(test_path))
                if test_path != '' and test_path[0] != '/': # in repository test set                                        
                    test_path                       = self._templates_repo + test_path                                    
                test_files = test_files + self.get_all_tests_from_path(test_path)  
                   
        return test_files   
    
    def get_all_tests_from_path(self, test_path):
        """Method returns all found test in path
           
           Test files are filtered by .jedi file extension
        
        Args:
           test_path (str): test path
        
        Returns:            
           list: test_files
                  
        """  
               
        test_files = []
        dmsg("Getting all tests from path: {0}".format(test_path))
                
        if re.search(':', test_path):
            tokens     = test_path.split(':')
            test_path  = tokens[0]
            ts_filter  = None if tokens[1] == '' else tokens[1]
            if ts_filter is not None and ts_filter not in self.ts_filter:            
                self.ts_filter.append(ts_filter)
            tca_filter = None
            tco_filter = None
            if len(tokens) > 2:
                tca_filter = None if tokens[2] == '' else tokens[2]
                if tca_filter is not None and tca_filter not in self.tca_filter:
                    self.tca_filter.append(tca_filter)
            if len(tokens) > 3:
                tco_filter = None if tokens[3] == '' else tokens[3]
                if tco_filter is not None and tco_filter not in self.tco_filter:
                    self.tco_filter.append(tco_filter)
            self._mh.dmsg('htk_on_debug_info', 'Filter parameters:\n\ttest_path: {0}\n\tts_filter: {1}\n\ttca_filter: {2}\n\ttco_filter: {3}'.format(test_path,ts_filter,tca_filter,tco_filter), self._mh.fromhere())                              
        
        if os.path.exists(test_path) == False:
            self._mh.dmsg('htk_on_warning', "Test path {0} doesn't exists".format(test_path), self._mh.fromhere())
            #TODO throw exception here
                
        if os.path.isfile(test_path):
            self.run_mode_src = 'singlefile'
            file_ext          = os.path.splitext(test_path)[1]
            file_ext          = file_ext[1:]
            
            if file_ext in self._test_file_ext:
                if file_ext == 'yoda': #parsing yoda container 
                    container_files = self.get_all_tests_from_container(test_path)
                    if len(container_files) > 1:
                        test_files.append(container_files)
                    elif len(container_files) == 1:                        
                        test_files = test_files + container_files 
                else:
                    test_files.append(test_path) 
            else:
                self._mh.dmsg('htk_on_debug_info', 'Unsupported file extension: {0} in {1}'.format(file_ext, test_path), self._mh.fromhere()) 
        else:
            self.run_mode_src = 'folder'        
            root_dir = test_path
            for dirname, _, filelist in os.walk(root_dir): # subdir_list not used            
                for fname in filelist:
                    file_extension = os.path.splitext(fname)[1][1:]
                    test_file = dirname + '/' + fname
                    if file_extension in self._test_file_ext:                        
                        if file_extension == 'yoda': #parsing yoda container
                            container_files = self.get_all_tests_from_container(test_file)
                            if len(container_files) > 1:
                                test_files.append(container_files)
                            elif len(container_files) == 1:                        
                                test_files = test_files + container_files                                                        
                        else:                              
                            ev = Event('yoda_before_append_test_file', test_file)        
                            if (self._mh.fire_event(ev) > 0):
                                test_file = ev.argv(0)
                            if ev.will_run_default():
                                test_files.append(test_file)
        return test_files  

class CodeStack():
    """Class CodeStack
    """
    
    _locals = {}
    
    def __init__(self):
        self._locals = {}
            
    def execute(self, code, loc):        
        self._locals.update(loc)        
        exec(code, globals(), self._locals)
           
    def compile(self, code):
        pass
