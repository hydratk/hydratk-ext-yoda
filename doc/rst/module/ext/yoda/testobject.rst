.. _module_ext_yoda_testobject:

Test object
===========

This sections contains module documentation of main testobject module.
Unit tests available at hydratk/extensions/yoda/testengine/01_methods_ut.jedi, 02_methods_ut.jedi, 03_methods_ut.jedi, 04_methods_ut.jedi

algorithm
^^^^^^^^^

Test set execution process

 .. graphviz::
   
   digraph G {
      graph [rank=TB,splines=ortho,ranksep="0.50",nodesep="0.70",bgcolor="transparent"]
      
      start [shape=circle,fillcolor=gray]
      end [shape=doublecircle]
      proc_set [shape=box, style=rounded, label="Process test scenarios in loop"]
      scen_finish [shape=diamond, label="Is processing finished ?"]
      create_scen [shape=box, style=rounded, label="Create test scenario in DB"]
      run_scen [shape=box, style=rounded, label="Run test scenario"]
      update_scen [shape=box, style=rounded, label="Update test scenario in DB"]
      proc_scen [shape=box, style=rounded, label="Process test cases in loop"]
      case_finish [shape=diamond, label="Is processing finished ?"]
      create_case [shape=box, style=rounded, label="Create test case in DB"]
      run_case [shape=box, style=rounded, label="Run test case"]
      update_case [shape=box, style=rounded, label="Update test case in DB"] 
      proc_case [shape=box, style=rounded, label="Process test cases in loop"]
      cond_finish [shape=diamond, label="Is processing finished ?"]
      create_cond [shape=box, style=rounded, label="Create test condition in DB"]
      run_cond [shape=box, style=rounded, label="Run test condition"]
      update_cond [shape=box, style=rounded, label="Update test condition in DB"]            

      start -> proc_set -> scen_finish
      scen_finish -> end[constraint=true]
      scen_finish -> create_scen[constraint=false] 
      create_scen -> run_scen -> update_scen -> proc_set
      
      run_scen -> proc_scen -> case_finish
      case_finish -> run_scen[constraint=true]
      case_finish -> create_case[constraint=false]
      create_case -> run_case -> update_case -> proc_scen
      
      run_case -> proc_case -> cond_finish
      cond_finish -> run_case[constraint=true]
      cond_finish -> create_cond[constraint=false]
      create_cond -> run_cond -> update_cond -> proc_case      

   }

Class Testobject
^^^^^^^^^^^^^^^^

**Attributes**

* _attr - attributes
* _attr_opt - attribute options
* _parent - reference to parent test object
* _log - raw log
* _struct_log - structured log

**Properties (Getters)** :

* parent - returns _parent
* attr - returns _attr
* attr_opt - returns _attr_opt
* log - returns _log
* struct_log - returns _struct_log

**Properties (Setters)** :

* log - appends _log

**Methods** :

* exec_test

Method executes test sets on path using testengine method exec_test.

* write_custom_data

Method writes test object data to database. Data specified in object filter are omitted. Methods writes to table custom_data, number or string parameters
are written as is. Other parameters are serialized to binary format using pickle. If parameter is configured in _attr_opt data are written to 
table custom_data_opt.

* setattr_opt

Method sets attribute option in _attr_opt if the parameter is specified in _attr.

* getattr_opt

Method gets attribute option from _attr_opt.

* getattr

Method gets attribute from _attr.

* setattr

Method sets attribute in _attr.

* __getattr__

Method gets attribute from _attr.

* get_auto_break

Method gets auto break exception from configuration.

* _explain

Method prints traceback and additional data when exception raises within test execution. 
Exception, test set, test scenario, test case, test condition. It is used for error analysis and location.

Exceptions
^^^^^^^^^^

Classes used to break test execution on various levels.

* BreakTestRun
* BreakTest
* BreakTestCase
* BreakTestScenario
* BreakTestSet

Class TestRun
^^^^^^^^^^^^^

**Attributes** :

* _id - test run identifier
* _obj_name - test run name
* _test_obj_name - test object name  
* _name - custom run name
* _attr - attributes
* _total_test_sets - count of test sets
* _total_tests - count of tests
* _failed_tests - count of failed tests
* _passed_tests - count of passed tests
* _skipped_tests - count of skipped tests (due to filtering)
* _run_tests - count of executed tests
* _norun_tests - count of not executed tests
* _failures - failure occured
* _start_time - run start
* _end_time - run finish
* _status - test run status
* _statuses - allowed statuses (started, finished, repeat, break)
* _log - raw log
* _struct_log - structured log
* _tset - list of TestSet
* _inline_tests - list of inline tests
* _te - TestEngine reference

**Properties (Getters)** :

* te - returns _te
* inline_tests - returns _inline_tests
* id - returns _id
* name - returns _name
* total_test_sets - returns _total_test_sets
* total_tests - returns _total_tests
* failed_tests - returns _failed_tests
* passed_tests - returns _passed_tests
* skipped_tests - returns _skipped_tests
* norun_tests - returns _norun_tests
* run_tests - returns _run_tests
* failures - returns _failures
* status - returns _status
* start_time - returns _start_time
* end_time - returns _end_time
* tset - returns _tset

**Properties (Setters)** :

* te - sets _te
* name - sets _name
* total_test_sets - sets _total_test_sets
* total_tests - sets _total_tests
* failed_tests - sets _failed_tests
* passed_tests - set _passed_tests
* skipped_tests - sets _skipped_tests
* norun_tests - sets _norun_tests
* run_tests - sets _run_tests
* failures - sets _failures
* status - sets _status
* start_time - sets _start_time
* end_time - sets _end_time
* tset - sets _tset

**Methods** :

* __init__

Method sets initial attribute values.

* create_db_record

Method writes to table test_run.

* update_db_record

Method updates in table test_run.

* __repr__

Method returns test run content in human readable format.

* break_test_run

Method sets _status = break and raises BreakTestRun.

Class TestSet
^^^^^^^^^^^^^

**Attributes** :

* _id - test set identifier
* _obj_name - test set name
* _test_obj_name - test object name
* _attr - attributes
* _current_test_base_path - test set path
* _current_test_set_file - test set filename
* _parsed_tests - count of parsed tests (aggregation for scenario, case, condition)
* _total_tests - count of tests
* _failed_tests - count of failed tests
* _passed_tests - count of passed tests
* _failed_ts - count of failed scenarios
* _passed_ts - count of passed scenarios
* _failures - failure occured
* _start_time - set start
* _end_time - run finish
* _log - raw log
* _struct_log - structured log
* _ts - list of scenarios         
* _test_run - test run reference
* _current - reference to current test object

**Properties (Getters)** :

* id - returns _id
* test_run - returns _test_run
* current_test_base_path - returns _current_test_base_path
* current_test_set_file - returns _current_test_set_file
* parsed_tests - returns _parsed_tests
* total_tests - returns _total_tests
* failed_tests - returns _failed_tests
* passed_tests - returns _passed_tests
* failed_ts - returns _failed_ts
* passed_ts - returns _passed_ts
* failures - returns _failures
* ts - returns _ts
* start_time - returns _start_time
* end_time - returns _end_time

**Properties (Setters)** :

* test_run - sets _test_run
* current_test_base_path - sets _current_test_base_path
* current_test_set_file - sets _current_test_set_file
* parsed_tests - sets _parsed_tests
* total_tests - sets _total_tests
* failed_tests - sets _failed_tests
* passed_tests - sets _passed_tests
* failed_ts - sets _failed_ts
* passed_ts - sets _passed_ts
* failures - sets _failures
* ts - sets _ts
* start_time - sets _start_time
* end_time - sets _end_time

**Methods** :

* __init__

Method sets initial attribute values.

* create_db_record

Method writes to table test_set.

* update_db_record

Method updates in table test_set.

* __repr__

Method returns test set content in human readable format.

* append_ts

Method adds TestScenario to _ts.

* reset_data

Method resets some attribute values.

* run

Method goes through test scenarios and checks if the scenario is not omitted by filter. If yes scenario is skipped.
It creates scenario record in database and runs scenario. Then it waits for completion (scenario can be repeated) and updates record in database.
Exceptions BreakTestRun, BreakTestSet stop whole test set execution, exception BreakTestScenario stops just current scenario.

* break_test_set

Method sets _status = break and raises BreakTestSet.

Class TestScenario
^^^^^^^^^^^^^^^^^^

**Attributes** :

* _id - test scenario identifier
* _obj_name - test scenario name
* _test_obj_name - test object name    
* _num - scenario order
* _attr - attributes
* _tca - list of cases
* _resolution - scenario resolution
* _status - scenario status  
* _statuses - allowed statuses (started, finished, repeat, break)
* _action - scenario action
* _prereq_passed - pre-requirements processing passed
* _postreq_passed - post-requirements processing passed
* _events_passed - events processing passed
* _failures - failure occured 
* _total_tests - count of tests
* _failed_tests - count of failed tests
* _passed_tests - count of passed tests
* _start_time - scenario start
* _end_time - scenario finish
* _parent - reference to parent test object
* _current - reference to current test object
* _log - raw log
* _struct_log - structured log

**Properties (Getters)** :

* obj_id - returns _id
* id - returns _attr[id]
* num - returns _num
* tca - returns _tca
* resolution - returns _resolution
* status - returns _status
* prereq_passed - returns _prereq_passed
* postreq_passed - returns _postreq_passed
* events_passed - returns _events_passed
* failures - returns _failures
* action - returns _action
* total_tests - returns _total_tests
* passed_tests - returns _passed_tests
* failed_tests - returns _failed_tests
* start_time - returns _start_time
* end_time - returns _end_time

**Properties (Setters)** :

* resolution - sets resolution
* status - set _status
* prereq_passed - sets _prereq_passed
* postreq_passed - sets _postreq_passed
* events_passed - sets _events_passed
* failures - sets _failures
* action - sets _action
* total_tests - sets _total_tests
* passed_tests - sets _passed_tests
* failed_tests - sets _failed_tests
* start_time - sets _start_time
* end_time - sets _end_time

**Methods** :

* __init__

Methods sets initial attribute values.

* create_db_record

Method writes to table test_scenario.

* update_db_record

Method updates in table test_scenario.

* run

Method runs test scenario. If exception occurs (BreakTestRun, BreakTestSet, BreakTestScenario) the scenario is stopped. 
If scenario contains pre-requirements, method fires event yoda_before_exec_ts_prereq and the code executed or just syntactically
validated (simulation mode). If scenario contains before_start event the method fires event yoda_events_before_start_ts and executes or checks event code.

Method goes through test cases and checks if the case is not omitted by filter. If yes case is skipped.
It creates case record in database and runs case. Then it waits for completion (case can be repeated) and updates record in database.

If scenario contains after_finish event the method fires event yoda_events_after_finish_ts and executes or checks event code.
If scenario contains post-requirements, method fires event yoda_before_exec_ts_postreq and executes or checks the code.

* break_test_scenario

Method sets _status = break and raises BreakTestScenario.

* break_test_set

Method sets _status = break and breaks parent TestSet.

* break_test_run

Method sets _status = break and breaks TestEngine.

Class TestCase
^^^^^^^^^^^^^^

**Attributes** :

* _id - test case identifier
* _obj_name - test case name
* _test_obj_name - test object name    
* _num - case order
* _attr - attributes
* _resolution - case resolution
* _status - case status  
* _statuses - allowed statuses (started, finished, repeat, break)
* _tco - list of conditions
* _action - scenario action
* _failures - failure occurred 
* _total_tests - count of tests
* _failed_tests - count of failed tests
* _passed_tests - count of passed tests
* _passed_tco - count of passed conditions
* _failed_tco - count of failed conditions
* _parent - reference to parent test object
* _current - reference to current test object
* _start_time - case start
* _end_time - case finish
* _events_passed - events execution passed
* _log - raw log
* _struct_log - structured log

**Properties (Getters)** :

* obj_id - returns _id
* id - returns _attr[id]
* num - returns _num
* tco - returns _tco
* resolution - returns _resolution
* status - returns _status
* failures - returns _failures
* tco_failures - returns _tco_failures
* action - returns _action
* total_tests - returns _total_tests
* passed_tests - returns _passed_tests
* failed_tests - returns _failed_tests
* failed_tco - returns _failed_tco
* passed_tco - returns _passed_tco
* start_time - returns _start_time
* end_time - returns _end_time
* events_passed - returns _events_passed

**Properties (Setters)** :

* resolution - sets resolution
* status - set _status
* failures - sets _failures
* tco_failures - set _tco_failures
* action - sets _action
* total_tests - sets _total_tests
* passed_tests - sets _passed_tests
* failed_tests - sets _failed_tests
* failed_tco - sets _failed_tco
* passed_tco - sets _passed_tco
* start_time - sets _start_time
* end_time - sets _end_time
* events_passed - sets _events_passed

**Methods** :

* __init__

Methods sets initial attribute values.

* create_db_record

Method writes to table test_case.

* update_db_record

Method updates in table test_case.

* run

Method runs test case. If exception occurs (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase) the case is stopped. 
If case contains before_start event the method fires event yoda_events_before_start_tca and executes or checks event code.

Method goes through test conditions and checks if the condition is not omitted by filter. If yes condition is skipped.
It creates condition record in database and runs condition. Then it waits for completion (condition can be repeated) and updates record in database.
If case contains after_finish event the method fires event yoda_events_after_finish_tca and executes or checks event code.

* break_test_case

Method sets _status = break and raises BreakTestCase.

* break_test_set

Method sets _status = break and breaks parent TestSet.

* break_test_run

Method sets _status = break and breaks TestEngine.

Class TestCondition
^^^^^^^^^^^^^^^^^^^

**Attributes** :

* _id - condition identifier
* _obj_name - condition name
* _test_obj_name - test object name
* _num  - condition order
* _attr - attributes 
* _resolution - condition resolution
* _status - condition status
* _statuses - allowed statuses (started, finished, repeat, break)
* _action - condition action
* _failures - failures occurred
* _expected_result - expected test result
* _test_resolution - resolution
* _test_result - result
* _test_output - output
* _test_assert - assertion
* _test_validate - validation
* _parent - reference to parent test object
* _current - reference to current test object
* _start_time - condition start
* _end_time - condition finish
* _events_passed - events execution passed
* _test_exec_passed - test execution passed
* _validate_exec_passed - test validation passed
* _log - raw log
* _struct_log - structured log

**Properties (Getters)** :

* id - returns _attr[id]
* resolution - returns _resolution
* status - returns _status
* failures - returns _failures
* action - returns _action
* expected_result - returns _expected_result
* test_resolution - returns _test_resolution
* test_result - returns _test_result
* test_output - returns _test_output
* test_assert - returns _test_assert
* test_validate - returns _test_validate
* start_time - returns _start_time
* end_time - returns _end_time
* events_passed - returns _events_passed
* test_exec_passed - returns _test_exec_passed
* validate_exec_passed - returns _validate_exec_passed

**Properties (Setters)** :

* resolution - sets _resolution
* status - sets _status
* failures - sets _failures
* action - sets _action
* expected_result - sets _expected_result
* test_resolution - sets _test_resolution
* test_result - sets _test_result
* test_output - sets _test_output
* test_assert - sets _test_assert
* test_validate - sets _test_validate
* start_time - sets _start_time
* end_time - sets _end_time
* events_passed - sets _events_passed
* test_exec_passed - sets _test_exec_passed
* validate_exec_passed - sets _validate_exec_passed

**Methods** :

* __init__

Method sets initial attribute values.

* create_db_record

Method writes to table test_condition.

* update_db_record

Method updates in table test_condition.

* run

Method runs test condition. If exception occurs (BreakTestRun, BreakTestSet, BreakTestScenario, BreakTestCase, BreakTest) the condition is stopped. 
If condition contains before_start event the method fires event yoda_events_before_start_tco and executes or checks event code.

Method increments total counters, fires event yoda_before_exec_tco_test and executes or checks test code. If execution doesn't raise any errors
the method fires event yoda_before_exec_validate_test and executes or checks validation code. If execution doesn't raises any errors passed counters are incremented,
otherwise failed counters are set. Condition result is printed with green or red color (passed or failed).

If condition contains after_finish event the method fires event yoda_events_after_finish_tco and executes or checks event code.

* break_test

Method sets _status = break and raises BreakTest.

* break_test_case

Method sets _status = break and breaks parent TestCase.

* break_test_scenario

Method sets _status = break and breaks parent TestScenario.

* break_test_set

Method sets _status = break and breaks parent TestSet.

* break_test_run

Method sets _status = break and breaks TestEngine.