# -*- coding: utf-8 -*-
"""This code is a part of Yoda extension

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
import traceback
from xtermcolor import colorize
from hydratk.lib.system import fs

class This(object):
    _obj = None
    
    def __init__(self, map_obj = None):                
        if map_obj is not None:
            self._obj = map_obj
    
    def __setattr__(self,name,value):
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            setattr(self._obj, name, value)
    
    def __getattr__(self,name):
        if hasattr(self._obj, name):
            f = getattr(self._obj, name)
            if hasattr(f, '__call__'):
                return self._obj[name]
            else:
                return f                  
        else: raise AttributeError('Undefined attribute "{0}"'.format(name))       

class Current(object):
    _tset  = None
    _ts    = None
    _tca   = None
    _tco   = None    
    
    
    def __init__(self):
        pass
    
    @property
    def test_set(self):
        return self._tset

    @test_set.setter
    def test_set(self, tset):
        self._tset = tset
    
    @property
    def tset(self):
        return self._tset

    @tset.setter
    def tset(self, tset):
        self._tset = tset     
    
    @property
    def test_scenario(self):
        return self._ts
    
    @property
    def ts(self):
        return self._ts
   
    @ts.setter
    def ts(self, ts):
        self._ts = ts 
        
    @property
    def test_case(self):
        return self._tca
        
    @property
    def tca(self):
        return self._tca
    
    @tca.setter
    def tca(self, tca):
        self._tca = tca 
    
    @property
    def test_condition(self):
        return self._tco
        
    @property
    def tco(self):
        return self._tco
    
    @tco.setter
    def tco(self, tco):
        self._tco = tco 

    
class Parent(object):
    _tset  = None
    _ts    = None
    _tca   = None    
    
    
    def __init__(self):
        pass
    
    @property
    def test_set(self):
        return self._tset

    @test_set.setter
    def test_set(self, tset):
        self._tset = tset
    
    @property
    def tset(self):
        return self._tset

    @tset.setter
    def tset(self, tset):
        self._tset = tset     
    
    @property
    def test_scenario(self):
        return self._ts
    
    @property
    def ts(self):
        return self._ts
   
    @ts.setter
    def ts(self, ts):
        self._ts = ts 
        
    @property
    def test_case(self):
        return self._tca
        
    @property
    def tca(self):
        return self._tca
    
    @tca.setter
    def tca(self, tca):
        self._tca = tca 
        
class TestSet(testobject.TestSet):
    '''Test Scenarios list'''
    _ts = []
   
    def append_ts(self,ts_obj):
        if isinstance(ts_obj, TestScenario):
            self._ts.append(ts_obj)
    
       
    
class TestScenario(testobject.TestScenario):
    '''Test Cases list'''
    _tc = []
    _next = None
    
    def repeat(self):
        self._action = 'repeat' 
        
    def append_tca(self, tca):
        if isinstance(tca, TestCase):                                   
            self._tca.append(tca)            
        

class TestCase(testobject.TestCase):
    '''Test Condition list'''
    _tco = []
    _next = None
    
    def repeat(self):
        self._action = 'repeat' 
    
    def append_tco(self, tco):
        if isinstance(tco, TestCondition):
            self._tco.append(tco)
            
class TestCondition(testobject.TestCondition):
    _next = None
    
    def repeat(self):
        self._action = 'repeat'     


class MacroParser(object):
    _hooks = {}
    
    def mp_add_hooks(self,*args, **kwargs):        
        for hdata in args:
            for mdef,cb in hdata.items():
                if type(mdef).__name__ == 'str' and mdef != '' and callable(cb):
                    self._hooks[mdef] = cb  
                    
        for mdef, cb in kwargs.items():
            if type(mdef).__name__ == 'str' and mdef != '' and callable(cb):
                self._hooks[mdef] = cb    
    
    def mp_add_hook(self, name, cb):
        if type(name).__name__ == 'str' and callable(cb):
            self._hooks[name] = cb
    
    def mp_parse(self, content):
        return re.sub(r'#<<(.*)::(.*)>>#',self._mp_processor,content)
    
    def _mp_processor(self,match):
        mdef = match.group(1).strip()
        mval = match.group(2).strip()
        if mdef in self._hooks:
            return self._hooks[mdef](mval)
        else: return '<<{mdef} is undefined>>'.format(mdef=mdef) 
        
        
class TestEngine(MacroParser):
    _mh              = None
    _test_run        = False
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
    _test_repo_root  = None
    _libs_repo       = None
    _templates_repo  = None
    _helpers_repo    = None
              
    @property
    def test_repo_root(self):
        return self._test_repo_root
    
    @test_repo_root.setter
    def test_repo_root(self, path):
        self._test_repo_root = path
    
    @property
    def libs_repo(self):
        return self._libs_repo
    
    @libs_repo.setter
    def libs_repo(self, path):
        self._libs_repo = path
    
    @property
    def templates_repo(self):
        return self._templates_repo
    
    @templates_repo.setter
    def templates_repo(self, path):
        self._templates_repo = path

    @property
    def helpers_repo(self):
        return self._helpers_repo
    
    @helpers_repo.setter
    def helpers_repo(self, path):
        self._helpers_repo = path

    @property
    def ts_filter(self):
        return self._ts_filter;
    
    @ts_filter.setter
    def ts_filter(self, fltr):
        self._ts_filter = fltr
    
    @property
    def tca_filter(self):
        return self._tca_filter;
    
    @tca_filter.setter
    def tca_filter(self, fltr):
        self._tca_filter = fltr
        
    @property
    def tco_filter(self):
        return self._tco_filter;
    
    @tco_filter.setter
    def tco_filter(self, fltr):
        self._tco_filter = fltr
    
    @property
    def run_mode_area(self):        
        return self._run_mode
    
    @run_mode_area.setter
    def run_mode_area(self, mode):        
        if mode in ('inrepo','global'):
            self._run_mode_src = mode
    
    @property
    def run_mode_src(self):
        return self._run_mode_src
    
    @run_mode_src.setter
    def run_mode_src(self, mode):        
        if mode in ('folder','singlefile'):
            self._run_mode_src = mode
    
    @property
    def test_simul_mode(self):        
        return self._test_simul_mode
            
    @test_simul_mode.setter
    def test_simul_mode(self, mode):        
        if mode in (True,False):
            self._test_simul_mode = mode
    
    @property
    def test_run(self):
        return self._test_run

    @test_run.setter
    def test_run(self, test_run):
        self._test_run = test_run    
    
    def __init__(self):       
        self._test_run        = testobject.TestRun()
        self._tset_struct     = None
        self._tset_obj        = None
        self._tset_file       = None
        self._this            = None
        self._parent          = Parent()
        self._current         = Current()
        self._mh              = MasterHead.get_head();
        self._test_simul_mode = False 
        self._code_stack      = CodeStack()
        self._run_mode_area   = 'inrepo'
        self._run_mode_src    = 'folder'
        self._ts_filter       = []
        self._tca_filter      = []
        self._tco_filter      = [] 
                
        self.mp_add_hooks({
                          'include' : self._h_include
                        })
              
    def _h_include(self, content_file):
        if content_file != '' and content_file[0] != '/': # repo
            content_file = self._templates_repo + content_file
       
        if os.path.exists(content_file) and os.path.isfile(content_file):
            result = fs.file_get_contents(content_file)
        else:
            result = '<<include !! {0} file not found>>'.format(content_file) 
        
        return result
            
    def load_tset_from_file(self, tset_file):        
        result = False
        if tset_file != '' and os.path.exists(tset_file):
            tset_str = fs.file_get_contents(tset_file)
            result = self.load_tset_from_str(tset_str, origin_file = True)
            self._tset_file = tset_file          
        return result 
    
    def load_tset_from_str(self, tset_str, origin_file = False):
        result = False
        if tset_str != '':
            if origin_file == False:
                self._tset_file = '<str>'
            tset_str = self.mp_parse(tset_str) #apply macros            
            self._tset_struct = yaml.load(tset_str)
            result = True; 
                
        return result
    
    def _parse_ts_node(self,ts_node, ts):
        for ts_key, ts_val in ts_node.items():
            if not (re.match('Test-Case', ts_key)):
                self._mh.dmsg('htk_on_debug_info',"Parsing Test-Scenario attributes {0}={1}".format(ts_key,ts_val), self._mh.fromhere())
                #print("Test-Scenario {0}={1}").format(ts_key,ts_val)
                ts.setattr(ts_key.lower(),ts_val)
            
    def _parse_tca_node(self, tca_node, tca):        
        for tca_key, tca_val in tca_node.items():
            if not (re.match('Test-Condition', tca_key)):
                self._mh.dmsg('htk_on_debug_info',"Parsing Test-Case attributes {0}={1}".format(tca_key,tca_val), self._mh.fromhere())                
                tca.setattr(tca_key.lower(),tca_val)
    
    def _parse_tco_node(self, tco_node, tco):
        for tco_key, tco_val in tco_node.items():
            if tco_key == 'validate':
                tco.expected_result = tco_val
            self._mh.dmsg('htk_on_debug_info',"Parsing Test-Condition attributes {0}={1}".format(tco_key,tco_val), self._mh.fromhere())    
            tco.setattr(tco_key.lower(), tco_val)            
                
    def run_tco(self, tco):        
        if isinstance(tco, TestCondition):
            '''Define missing locals'''            
            self._this        = tco
            this              = self._this
            self._current.tco = tco
            current           = self._current
            parent            = self._parent           
            prev              = None #TODO
            next              = None #TODO           
                            
            test_exception = False
            if tco.events != None and 'before_start' in tco.events:                                
                try:
                    ev = Event('yoda_events_before_start_tco', tco.events['before_start'])        
                    if (self._mh.fire_event(ev) > 0):
                        tco.events['before_start'] = ev.argv(0)
                    if ev.will_run_default():                        
                        if self.test_simul_mode == False:                                                         
                            self._code_stack.execute(tco.events['before_start'], locals())     
                        else:
                            print("Simulation: Running Test Condition %s yoda_events_before_start_tco " % tco.name)
                            compile(tco.events['before_start'],'<string>','exec')
                    
                except Exception as exc:                                   
                    exc_info = sys.exc_info()
                    tco.test_log += "Exception: %s\n" % exc_info[0]
                    tco.test_log += "Value: %s\n" % str(exc_info[1])
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = ''
                    for line in formatted_lines:
                        trace += "%s\n" % str(line)
                    tco.test_log += trace
                    self._tset_obj.failures = True
                    self._parent.ts.failures = True
                    self._parent.tca.failures = True
                    tco.failures = True    
            
            try:                
                self._test_run.total_tests += 1                        
                ev = Event('yoda_before_exec_tco_test', tco.test)        
                if (self._mh.fire_event(ev) > 0):                            
                    tco.test = ev.argv(0)
                if ev.will_run_default():
                    if self.test_simul_mode == False:
                        self._parent.ts.total_tests += 1                                                                                                                                                
                        self._code_stack.execute(tco.test, locals())                          
                    else:                        
                        print("Simulation: Running Test case: %s, Test condition: %s" % (self._parent.tca.name, tco.name))
                        compile(tco.test,'<string>','exec')
            except Exception as exc:
                exc_info = sys.exc_info()
                tco.test_log += "Exception: %s\n" % exc_info[0]
                tco.test_log += "Value: {0}\n".format(str(exc_info[1]))
                tco.test_log += tco.test
                formatted_lines = traceback.format_exc().splitlines()
                trace = ''
                for line in formatted_lines:
                    trace += "%s\n" % str(line)
                tco.test_log += trace
                test_exception = True
                tco.test_resolution = 'Failed'                        
                self._parent.ts.failed_tests +=1
                self._parent.tca.failed_tco += 1
                self._tset_obj.failures   = True
                self._parent.ts.failures  = True
                self._parent.tca.failures = True
                tco.action                = 'break'
                                           
            if test_exception == False:                
                try:
                    ev = Event('yoda_before_exec_validate_test', tco.validate)        
                    if (self._mh.fire_event(ev) > 0):                            
                        tco.validate = ev.argv(0)
                    if ev.will_run_default():
                        if self.test_simul_mode == False:                                                                                 
                            self._code_stack.execute(tco.validate, locals())     
                        else:
                            print("Simulation: Validating result, Test case: %s, Test condition: %s" % (self._parent.tca.name, tco.name))
                            compile(tco.validate,'<string>','exec')                                
                    self._parent.ts.passed_tests += 1
                    self._parent.tca.passed_tco += 1                            
                    tco.test_resolution = 'Passed'
                    self._test_run.passed_tests += 1                    
                    tco_note = "*** {ts}/{tca}/{tco}: ".format(ts=self._parent.ts.name,tca=self._parent.tca.name,tco=tco.name)
                    tco_note = colorize(tco_note, rgb=0x00bfff) + colorize('PASSED',rgb=0x00ff00)
                    print(tco_note)                                                    
                        
                except (AssertionError) as ae:                                               
                    self._parent.ts.failed_tests += 1
                    self._parent.tca.failed_tco += 1
                    self._tset_obj.failures = True
                    self._test_run.failed_tests += 1                    
                    self._parent.ts.failures = True
                    self._parent.tca.failures = True
                    tco.test_log += bytes(ae)
                    tco.test_resolution = 'Failed'
                    tco.expected_result = ae                         
                        
                except Exception as exc:
                    exc_info = sys.exc_info()
                    tco.test_log += "Exception: %s\n" % exc_info[0]
                    tco.test_log += "Value: %s\n" % str(exc_info[1])
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = ''
                    for line in formatted_lines:
                        trace += "%s\n" % str(line)
                    print("Exception %s" % trace)                            
                    tco.test_log += trace
                    test_exception = True
                    tco.test_resolution = 'Failed'                        
                    self._parent.ts.failed_tests +=1
                    self._parent.tca.failed_tco += 1
                    self._tset_obj.failures = True          
             
            if tco.test_resolution == 'Failed':
                tco_note = "*** {ts}/{tca}/{tco}: ".format(ts=self._parent.ts.name,tca=self._parent.tca.name,tco=tco.name)
                tco_note = colorize(tco_note, rgb=0x00bfff) + colorize('FAILED',rgb=0xff0000)
                print(tco_note)              
                                        
            if tco.action == None:
                tco.status = "finished"
                
            elif tco.action == "repeat":
                tco.status = "repeat"
                tco.action = None
            
            elif tco.action == 'break':
                tco.status = 'break'
                tco.action = None 
                     
    
    def run_tca(self, tca):        
        if isinstance(tca, TestCase):
            '''Define missing locals'''
            self._this        = tca
            this              = self._this
            self._current.tca = tca
            current           = self._current
            parent            = self._parent           
            prev              = None #TODO
            next              = None #TODO
                                           
                        
            if tca.events != None and 'before_start' in tca.events:                
                try:
                    ev = Event('yoda_events_before_start_tca', tca.events['before_start'])        
                    if (self._mh.fire_event(ev) > 0):
                        tca.events['before_start'] = ev.argv(0)
                    if ev.will_run_default():
                        if self.test_simul_mode == False:                                                                                                                                       
                            self._code_stack.execute(tca.events['before_start'], locals())                                                                      
                        else:
                            print("Simulation: Running Test Case %s yoda_events_before_start_tca " % tca.name)
                            compile(tca.events['before_start'],'<string>','exec')
                    
                except Exception as exc:                                   
                    exc_info = sys.exc_info()
                    tca.test_log += "Exception: %s\n" % exc_info[0]
                    tca.test_log += "Value: %s\n" % str(exc_info[1])
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = ''
                    for line in formatted_lines:
                        trace += "%s\n" % str(line)
                    tca.test_log += trace
                    self._tset_obj.failures = True
                    self._parent.ts.failures = True
                    tca.failures = True                    
                    print(tca.test_log)            
            
            self._parent.tca  = tca              
            for tco in tca.tco:
                run_tco = True
                if self.tco_filter is not None and type(self.tco_filter).__name__ == 'list' and len(self.tco_filter) > 0:
                    if tco.id is not None and tco.id != '' and tco.id not in self.tco_filter:
                        run_tco = False
                
                if run_tco:
                    #print("Running test condition {0}".format(tco.id))                                                
                    tco.status     = 'started'
                    self._this     = tco                
                    while tco.status != 'finished':
                        if tco.status in ('started','repeat'):                        
                            self.run_tco(tco)
                        elif tco.status == 'break':
                            break;
                    tco.resolution = 'completed'
                else:
                    tco.resolution = 'skipped'
                    print("Filter: Skippind test condition {0}".format(tco.id))    
            if tca.action == None:
                tca.status = "finished" 
               
    def run_ts(self, ts):          
        if isinstance(ts, TestScenario):            
            '''Define missing locals'''
            self._this        = ts             
            this              = self._this
            self._current.ts  = ts
            current           = self._current
            current.tset      = self._tset_obj
            current.test_set  = self._tset_obj
            parent            = self._parent
            parent.tset       = self._tset_obj
            parent.test_set   = self._tset_obj
            parent            = self._parent 
            parent.ts         = None #TODO
            parent.tc         = None #TODO
            prev              = None #TODO
            next              = None #TODO
                        
            if ts.pre_req != None:
                try:
                    ev = Event('yoda_before_exec_ts_prereq', ts.pre_req)        
                    if (self._mh.fire_event(ev) > 0):
                        ts.pre_req = ev.argv(0)
                    if ev.will_run_default():
                        if self.test_simul_mode == False:
                            self._code_stack.execute(ts.pre_req, locals())                                                                                   
                        else:
                            print("Simulation: Running Test scenario %s pre-req" % ts.name)
                            compile(ts.pre_req,'<string>','exec')
                    ts.prereq_passed = True
                except Exception as exc:
                    ts.prereq_passed = False                    
                    exc_info = sys.exc_info()
                    ts.test_log += "Exception: %s\n" % exc_info[0]
                    ts.test_log += "Value: %s\n" % str(exc_info[1])
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = ''
                    for line in formatted_lines:
                        trace += "%s\n" % str(line)
                    ts.test_log += trace
                    self._tset_obj.failures = True
                    ts.failures = True
                                                                        
            
            if ts.events != None and 'before_start' in ts.events:                
                try:
                    ev = Event('yoda_events_before_start_ts', ts.events['before_start'])        
                    if (self._mh.fire_event(ev) > 0):
                        ts.events['before_start'] = ev.argv(0)
                    if ev.will_run_default():
                        if self.test_simul_mode == False:                                                        
                            self._code_stack.execute(ts.events['before_start'], locals())                              
                        else:
                            print("Simulation: Running Test scenario %s yoda_events_before_start_ts " % ts.name)
                            compile(ts.events['before_start'],'<string>','exec')
                    
                except Exception as exc:                                   
                    exc_info = sys.exc_info()
                    ts.test_log += "Exception: %s\n" % exc_info[0]
                    ts.test_log += "Value: %s\n" % str(exc_info[1])
                    formatted_lines = traceback.format_exc().splitlines()
                    trace = ''
                    for line in formatted_lines:
                        trace += "%s\n" % str(line)
                    ts.test_log += trace
                    self._tset_obj.failures = True
                    ts.failures = True                
                
            self._parent.ts  = ts             
            for tca in ts.tca:
                run_tca = True
                if self.tca_filter is not None and type(self.tca_filter).__name__ == 'list' and len(self.tca_filter) > 0:
                    if tca.id is not None and tca.id != '' and tca.id not in self.tca_filter:
                        run_tca = False
                
                if run_tca:
                    #print("Running test case {0}".format(tca.id))  
                    tca.status     = 'started'
                    self._this     = tca               
                    while tca.status != 'finished':
                        if tca.status in ('started','repeat'):
                            self.run_tca(tca)
                        elif tca.status == 'break':
                            break;
                    #tca finished event here
                    tca.resolution = 'completed'
                else:
                    tca.resolution = 'skipped'
                    print("Filter: Skippind test case {0}".format(tca.id))
                                    
            if ts.action == None:
                ts.status = "finished"
          
    def run_tset(self):
        if self._tset_obj != None and isinstance(self._tset_obj, TestSet):
            self._parent.tset  = self._tset_obj
            self._current.tset = self._tset_obj
            self._current.test_set = self._tset_obj                
            for ts in self._tset_obj.ts:
                run_ts = True
                if self.ts_filter is not None and type(self.ts_filter).__name__ == 'list' and len(self.ts_filter) > 0:                    
                    if ts.id is not None and ts.id != '' and ts.id not in self.ts_filter:
                        print(ts.id)
                        pprint.pprint(self.ts_filter)
                        run_ts = False
                    
                if run_ts:
                    print("Running test scenario {0}".format(ts.id)) 
                    ts.status          = 'started'
                    self._this         = ts
                               
                    while ts.status != 'finished':
                        if ts.status in ('started','repeat'):
                            self.run_ts(ts)
                        elif ts.status == 'break':
                            break;
                    ts.resolution = 'completed'
                else:
                    ts.resolution = 'skipped'
                    print("Filter: Skippind test scenario {0}".format(ts.id))
            self._test_run.tset.append(self._tset_obj)
                
        
    def parse_tset_struct(self):
        if (type(self._tset_struct).__name__ == 'dict'):
            self._tset_obj = TestSet()
            if self._tset_file != '<str>':
                self._tset_obj.current_test_base_path = os.path.dirname(self._tset_file)
            self._tset_obj.current_test_set_file = self._tset_file
                        
            ts_num = 1
            ts_k = 'Test-Scenario-%d' % ts_num
            while ts_k in self._tset_struct:                
                ts = TestScenario(ts_num)                               
                self._parse_ts_node(self._tset_struct[ts_k], ts)
                
                tca_num = 1
                tca_k = 'Test-Case-%d' % tca_num                
                while tca_k in self._tset_struct[ts_k]:                    
                    tca = TestCase(tca_num)                    
                    self._parse_tca_node(self._tset_struct[ts_k][tca_k], tca)
                    
                    tco_num = 1
                    tco_k = 'Test-Condition-%d' % tco_num                    
                    while tco_k in self._tset_struct[ts_k][tca_k]:                                                                   
                        tco = TestCondition(tco_num)                        
                        self._parse_tco_node(self._tset_struct[ts_k][tca_k][tco_k], tco)
                        
                        tco_num += 1
                        tco_k = 'Test-Condition-%d' % tco_num                        
                        tca.append_tco(tco)
                    
                    tca_num += 1
                    tca_k = 'Test-Case-%d' % tca_num                    
                    ts.append_tca(tca)                              
                    
                ts_num += 1
                ts_k = 'Test-Scenario-%d' % ts_num
                self._tset_obj.append_ts(ts)                
                
            if ts_num == 1:
                print("Test-Scenario-%d tag expected" % ts_num)     
        else:
            print("Wrong tset structure")        


class CodeStack():
    _locals = {}
    
    def __init__(self):
        self._locals = {}
            
    def execute(self, code, loc):        
        self._locals.update(loc)        
        exec(code, globals(), self._locals)
           
    def compile(self, code):
        pass


        
    
    