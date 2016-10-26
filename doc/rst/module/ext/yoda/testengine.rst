.. _module_ext_yoda_testengine:

Test engine
===========

This sections contains module documentation of main testengine module.
Unit tests available at hydratk/extensions/yoda/testengine/01_methods_ut.jedi, 02_methods_ut.jedi, 03_methods_ut.jedi

Class TestEngine
^^^^^^^^^^^^^^^^

**Attributes** :

* _mh - MasterHead reference
* _test_run - test run reference
* _exec_level - execution level
* _tset_struct - parsed test set
* _tset_obj - test set reference
* _tset_file - test set file
* _this
* _parent - reference to parent test object
* _current - reference to current tes object
* _test_simul_mode - True if running simulation
* _code_stack - CodeStack reference
* _run_mode_area - run area (global, inrepo)
* _run_mode_src - run source (folder, singlefile)
* _ts_filter - test scenario filter
* _tca_filter - test case filter
* _tco_filter - test condition filter
* _config
* _test_repo_root - yoda repository directory
* _libs_repo - libraries directory
* _templates_repo - test directory
* _helpers_repo - helpers directory
* _test_file_ext - extensions for test files (yoda, jedi)
* _test_template_ext - extensions for test template (padavan)
* _test_results_db - results database reference
* _have_test_results_db - bool, True if _test_results_db is set 
* _use_test_results_db

**Properties (Getters)** :

* code_stack - returns _code_stack
* test_repo_root - returns _test_repo_root
* libs_repo - returns _libs_repo
* templates_repo - returns _templates_repo
* have_test_results_db - bool, True if _test_results_db is set
* test_results_db - returns _test_results_db
* helpers_repo - returns _helpers_repo
* ts_filter - returns _ts_filter
* tca_filter - returns _tca_filter
* tco_filter - returns _tco_filter
* run_mode_area - returns _run_mode_area
* run_mode_src - returns _run_mode_src
* exec_level - returns _exec_level
* test_simul_mode - returns _test_simul_mode
* test_run - returns _test_run

**Properties (Setters)** :

* test_repo_root - sets _test_repo_root
* libs_repo - sets _libs_repo
* templates_repo - sets _templates_repo
* test_results_db - sets _test_results_db, _have_test_results_db
* helpers_repo - sets _helpers_repo
* ts_filter - sets _ts_filter
* tca_filter - sets _tca_filter
* tco_filter - sets _tco_filter
* run_mode_area - sets _run_mode_area if allowed (global, inrepo)
* run_mode_src - sets _run_mode_src if allowed (folder, singlefile)
* test_simul_mode - sets _test_simul_mode
* test_run - sets _test_run

**Methods** :

* __init__

Methods sets initial attribute values.

* new_test_run

Method initializes test run (testobject.TestRun).

* _h_include

Method reads referenced test file (using macro). Relative path is allowed only.

* load_tset_from_file

Method loads test set content from file using method load_tset_from_str.

* load_tset_from_str

Methods loads test set content from string to YAML format. Also it parses macros.

* _parse_ts_node

Method parses test scenario dictionary. It sets only metadata (elements Test-Case are omitted).

* _parse_tca_node

Method parses test case dictionary. It sets only metadata (elements Test-Condition are omitted).  

* _parse_tco_node

Method parses test condition dictionary. It sets all elements.

* parse_tset_struct

Method parses test set hierarchy Test-Scenario -> Test-Case -> Test-Condition. For each element it creates appropriate object
(TestScenario, TestCase, TestCondition). They must be numbered and ordered Test-Scenario-%d, Test-Case-%d, Test-Condition-%d.
Metadata elements are processing by auxiliary methods _parse_ts_node, _parse_tca_node, _parse_tco_node.

* exec_test

Method executes all tests found on path. It sets run area, global if path is absolute, inrepo if path is relative.
It searches test files on path. For each test file it fires event yoda_before_parse_test_file. The file is loaded and parsed.
If correctly parsed it creates test set database record, runs the set and updates database record.

* get_all_tests_from_container

Method gets test paths specified in container file. Each line is considered as test path and is searched using method get_all_tests_from_path.

* get_all_tests_from_path

Method gets all test files found on path. The path can contain filters (path:ts_filter:tca_filter:tca_filter) which are parsed.
When path is file method sets singlefile run source. The file must extensions jedi (test set) or yoda (container, method parses it using get_all_tests_from_container).
When path is directory method sets folder run source. Then it goes through directory tree and searches jedi, yoda files.

Class CodeStack
^^^^^^^^^^^^^^^

**Attributes** :

* _locals - local scope

**Methods** :   

* __init__

Method sets _locals

* execute

Method executes piece of code (using system method exec) within local and global scope.

Class MacroParser
^^^^^^^^^^^^^^^^^

**Attributes** :

* _hooks - macro hooks

**Methods** :

* mp_add_hooks

Method registers macro hooks dictionary (key - name, value - callback).

* mp_add_hook

Method registers macro hook specified by name, callback.

* mp_parse

Method parses macro string #<<(.*)::(.*)>># (callback, parameters).

* _mp_processor

Method calls macro with given parameters if registered.

Class Current
^^^^^^^^^^^^^

It is used as reference to current test object.

**Attributes** :

* _tset - TestSet reference
* _ts - TestScenario reference
* _tca - TestCase reference
* _tco - TestCondition reference
* _te - TestEngine reference

**Properties (Getters)** :

* te - returns _te
* test_set - returns _tset
* tset - returns _tset
* test_scenario - returns _ts
* ts - returns _ts
* test_case - returns _tca
* tca - returns _tca
* test_condition - returns _tco
* tco - returns _tco

**Properties (Setters)** :

* te - sets _te
* test_set - sets _tset
* tset - sets _tset
* ts - sets _ts
* tca - sets _tca
* tco - sets _tco

Class Parent
^^^^^^^^^^^^

It is used as reference to parent test object.

**Attributes** :

* _tset - TestSet reference
* _ts - TestScenario reference
* _tca - TestCase reference

**Properties (Getters)** :

* test_set - returns _tset
* tset - returns _tset
* test_scenario - returns _ts
* ts - returns _ts
* test_case - returns _tca
* tca - returns _tca

**Properties (Setters)** :

* test_set - sets _tset
* tset - sets _tset
* ts - sets _ts
* tca - sets _tca

Class TestSet
^^^^^^^^^^^^^

Inherited from testobject.TestSet.

**Attributes** :

* _ts - list of test scenarios

**Methods** :

* append_ts

Method adds TestScenario to _ts.

Class TestScenario
^^^^^^^^^^^^^^^^^^

Inherited from testobject.TestScenario.

**Attributes** :

* _tca - list of test cases
* _next - reference to next scenario
* _action

**Methods** :

* repeat

Method enables test scenario to be repeated.

* append_tca

Method adds TestCase to _tca.

Class TestCase
^^^^^^^^^^^^^^

Inherited from testobject.TestCase.

**Attributes** :

* _tco - list of test conditions
* _next - reference to next case
* _action

**Methods** :

* repeat

Method enables test case to be repeated.

* append_tco

Method adds TestCondition to _tco.

Class TestCondition
^^^^^^^^^^^^^^^^^^^

Inherited from testobject.TestCondition.

**Attributes** :

* _next - reference to next condition
* _action

**Methods** :

* repeat

Method enables test condition to be repeated.