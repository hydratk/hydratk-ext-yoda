.. _tutor_yoda_tut7_parallel:

Tutorial 7: Parallel execution
==============================

This section will show you how to execute tests in parallel mode.

Example
^^^^^^^

Scripts can be executed in parallel. Use option -m or --run-mode with value 2.
Directory test contains 2 scripts.

  .. code-block:: bash
  
     $ htk -m 2 --yoda-test-path test yoda-run 
     
     Running hook cmsg_async_ext_fn
     Running hook cmsg_async_ext_fn
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED
     *** scenario 1/case 1/condition 1: PASSED
     *** scenario 1/case 1/condition 2: PASSED
     *** scenario 1/case 2/condition 1: PASSED
     *** scenario 2/case 1/condition 1: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 2, tests - total: 6, failed: 1, passed: 5|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi
       Test Scenario: Example test scenario, tests - total: 2, failed: 1, passed: 1
         Test Case: Example test case
           Test Condition: Example test condition 2
             Expected Result: x-y != 2
             Actual Result: 3
             Log: x-y != 2

    Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
      Test Scenario: scenario 2, tests - total: 1, failed: 0, passed: 1
      Test Scenario: scenario 1, tests - total: 3, failed: 0, passed: 3
      
The output is slightly different. Each test script was executed in own process.
If you want to see more turn on debug mode.

  .. code-block:: bash
  
     $htk -d 1 --run-mode 2 --yoda-test-path test yoda-run
  
     [22/05/2016 20:51:05.531] Debug(1): hydratk.core.masterhead:check_debug:0: Debug level set to 1
     [22/05/2016 20:51:05.532] Debug(1): hydratk.core.corehead:_apply_config:0: Language set to 'English'
     [22/05/2016 20:51:05.532] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [22/05/2016 20:51:05.533] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [22/05/2016 20:51:05.534] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [22/05/2016 20:51:05.534] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [22/05/2016 20:51:05.535] Debug(1): hydratk.core.corehead:_apply_config:0: Run mode set to '2 (CORE_RUN_MODE_PP_APP)'
     [22/05/2016 20:51:05.536] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [22/05/2016 20:51:05.537] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [22/05/2016 20:51:05.538] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [22/05/2016 20:51:05.539] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [22/05/2016 20:51:05.540] Debug(1): hydratk.core.corehead:_apply_config:0: Main message router id set to 'raptor01'
     [22/05/2016 20:51:05.541] Debug(1): hydratk.core.corehead:_apply_config:0: Number of core workers set to: 4
     [22/05/2016 20:51:05.541] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'TestEnv'
     [22/05/2016 20:51:05.581] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.testenv.translation.en.messages'
     [22/05/2016 20:51:05.582] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [22/05/2016 20:51:05.583] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.testenv.translation.en.help'
     [22/05/2016 20:51:05.584] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'TestEnv v0.1.0 (c) [2015 Petr Rašek <bowman@hydratk.org>]' loaded successfully
     [22/05/2016 20:51:05.585] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'BenchMark'
     [22/05/2016 20:51:05.586] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.benchmark.translation.en.messages'
     [22/05/2016 20:51:05.587] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [22/05/2016 20:51:05.588] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.benchmark.translation.en.help'
     [22/05/2016 20:51:05.589] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'BenchMark v0.1.0 (c) [2013 Petr Czaderna <pc@hydratk.org>]' loaded successfully
     [22/05/2016 20:51:05.589] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'Yoda'
     [22/05/2016 20:51:05.601] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.yoda.translation.en.messages'
     [22/05/2016 20:51:05.604] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [22/05/2016 20:51:05.607] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.yoda.translation.en.help'
     [22/05/2016 20:51:05.613] Debug(1): hydratk.extensions.yoda.yoda:_init_repos:0: 
        Init repos: test_repo_root: /var/local/hydratk/yoda
                    libs_repo: /var/local/hydratk/yoda/lib
                    templates_repo: /var/local/hydratk/yoda/yoda-tests/
                    helpers_repo: /var/local/hydratk/yoda/helpers
        
     [22/05/2016 20:51:05.615] Debug(1): hydratk.extensions.yoda.yoda:_register_htk_actions:0: Registering htk actions
     [22/05/2016 20:51:05.616] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'Yoda v0.2.0 (c) [2014 - 2016 Petr Czaderna <pc@hydratk.org>]' loaded successfully
     [22/05/2016 20:51:05.616] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'Datagen'
     [22/05/2016 20:51:05.618] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.datagen.translation.en.messages'
     [22/05/2016 20:51:05.619] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [22/05/2016 20:51:05.620] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.datagen.translation.en.help'
     [22/05/2016 20:51:05.621] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'Datagen v0.1.0 (c) [2016 Petr Rašek <bowman@hydratk.org>]' loaded successfully
     [22/05/2016 20:51:05.622] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'TrackApps'
     [22/05/2016 20:51:05.624] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.trackapps.translation.en.messages'
     [22/05/2016 20:51:05.632] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [22/05/2016 20:51:05.633] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.trackapps.translation.en.help'
     [22/05/2016 20:51:05.635] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'TrackApps v0.1.0 (c) [2016 Petr Rašek <bowman@hydratk.org>]' loaded successfully
     [22/05/2016 20:51:05.636] Debug(1): hydratk.core.corehead:_load_extensions:0: Finished loading internal extensions
     Warning: hydratk.core.corehead:_set_default_cli_params:0: Missing option yoda-db-results-enabled definition, languague en 
     [22/05/2016 20:51:05.644] Debug(1): hydratk.extensions.yoda.yoda:init_check:0: Using database test results
     [22/05/2016 20:51:05.669] Debug(1): hydratk.core.corehead:_init_message_router:0: Message Router 'raptor01' initialized successfully
     [22/05/2016 20:51:05.670] Debug(1): hydratk.core.corehead:_c_observer:0: Core message service 'c01' registered successfully
     [22/05/2016 20:51:05.672] Debug(1): hydratk.core.corehead:_c_observer:0: Core message queue '/tmp/hydratk/core.socket' initialized successfully
     [22/05/2016 20:51:05.672] Debug(1): hydratk.core.corehead:_c_observer:0: Starting to observe
     [22/05/2016 20:51:05.673] Debug(1): hydratk.core.corehead:_c_observer:0: Saving PID 8260 to file: /tmp/hydratk/hydra.pid
     [22/05/2016 20:51:05.680] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 1
     [22/05/2016 20:51:05.683] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 2
     [22/05/2016 20:51:05.699] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 3
     [22/05/2016 20:51:05.712] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 4
     [22/05/2016 20:51:05.729] Debug(1): hydratk.core.corehead:_c_worker:1: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [22/05/2016 20:51:05.739] Debug(1): hydratk.extensions.yoda.yoda:check_test_results_db:0: Initializing test results database, dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3
     [22/05/2016 20:51:05.737] Debug(1): hydratk.core.corehead:_c_worker:1: Starting to work
     [22/05/2016 20:51:05.740] Debug(1): hydratk.core.corehead:_c_worker:2: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [22/05/2016 20:51:05.745] Debug(1): hydratk.core.corehead:_c_worker:2: Starting to work
     [22/05/2016 20:51:05.755] Debug(1): hydratk.core.corehead:_c_worker:3: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [22/05/2016 20:51:05.762] Debug(1): hydratk.core.corehead:_c_worker:3: Starting to work
     [22/05/2016 20:51:05.765] Debug(1): hydratk.extensions.yoda.yoda:check_test_results_db:0: Test result database dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3 check ok.
     [22/05/2016 20:51:05.767] Debug(1): hydratk.extensions.yoda.yoda:init_libs:0: Added shared library directory /var/local/hydratk/yoda/lib
     [22/05/2016 20:51:05.769] Debug(1): hydratk.core.corehead:_c_worker:4: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [22/05/2016 20:51:05.768] Debug(1): hydratk.extensions.yoda.yoda:init_helpers:0: Added helpers directory /var/local/hydratk/yoda/helpers
     [22/05/2016 20:51:05.770] Debug(1): hydratk.extensions.yoda.yoda:init_tests:0: Running test sets in repository: /var/local/hydratk/yoda/yoda-tests/test
     [22/05/2016 20:51:05.771] Debug(1): hydratk.core.corehead:_c_worker:4: Starting to work
     [22/05/2016 20:51:05.773] Debug(1): hydratk.extensions.yoda.testengine:get_all_tests_from_path:0: Getting all tests from path: /var/local/hydratk/yoda/yoda-tests/test
     [22/05/2016 20:51:05.775] Debug(1): hydratk.extensions.yoda.yoda:process_tests:0: Process tests test_simul_mode False, run_mode 2
     [22/05/2016 20:51:05.786] Debug(1): hydratk.extensions.yoda.yoda:process_tests:0: Found 2 test sets for processing
     [22/05/2016 20:51:05.788] Debug(1): hydratk.extensions.yoda.yoda:pp_process_test_set:0: Processing test set /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi in parallel mode
     [22/05/2016 20:51:05.793] Debug(1): hydratk.core.messagehead:_process_cmsg:1: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': 'pp_run_test_set', 'args': ('/var/local/hydratk/yoda/yoda-tests/test/test_break.jedi',), 'ext_name': 'Yoda', 'kwargs': {}}, 'ticket_id': '1463943065.79-0-1'}}
     Running hook cmsg_async_ext_fn
     [22/05/2016 20:51:05.794] Debug(1): hydratk.extensions.yoda.yoda:pp_process_test_set:0: Got ticket id: 1463943065.79-0-1 for test set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
     [22/05/2016 20:51:05.795] Debug(1): hydratk.extensions.yoda.yoda:pp_process_test_set:0: Processing test set /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi in parallel mode
     [22/05/2016 20:51:05.797] Debug(1): hydratk.core.messagehead:_process_cmsg:2: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': 'pp_run_test_set', 'args': ('/var/local/hydratk/yoda/yoda-tests/test/wtest.jedi',), 'ext_name': 'Yoda', 'kwargs': {}}, 'ticket_id': '1463943065.8-0-2'}}
     Running hook cmsg_async_ext_fn
     [22/05/2016 20:51:05.801] Debug(1): hydratk.extensions.yoda.yoda:init_test_results_db:1: Initializing test results database, dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3
     [22/05/2016 20:51:05.800] Debug(1): hydratk.extensions.yoda.yoda:pp_process_test_set:0: Got ticket id: 1463943065.8-0-2 for test set: /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi
     [22/05/2016 20:51:05.807] Debug(1): hydratk.extensions.yoda.yoda:init_test_results_db:2: Initializing test results database, dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3
     [22/05/2016 20:51:05.805] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Got context switch, active tickets: 2
     [22/05/2016 20:51:05.810] Debug(1): hydratk.extensions.yoda.yoda:init_test_results_db:1: Test result database dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3 check ok.
     [22/05/2016 20:51:05.823] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Checking ticket_id 1463943065.79-0-1
     [22/05/2016 20:51:05.825] Debug(1): hydratk.extensions.yoda.yoda:pp_run_test_set:1: Processing test set /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
     [22/05/2016 20:51:05.826] Debug(1): hydratk.extensions.yoda.yoda:init_test_results_db:2: Test result database dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3 check ok.
     [22/05/2016 20:51:05.826] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: There're still 2 wating tickets
     [22/05/2016 20:51:05.830] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Checking ticket_id 1463943065.8-0-2
     [22/05/2016 20:51:05.830] Debug(1): hydratk.extensions.yoda.yoda:pp_run_test_set:2: Processing test set /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi
     [22/05/2016 20:51:05.832] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: There're still 2 wating tickets
     [22/05/2016 20:51:05.892] Debug(1): hydratk.extensions.yoda.yoda:pp_run_test_set:2: Creating test set /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi database record
     [22/05/2016 20:51:05.911] Debug(1): hydratk.extensions.yoda.yoda:pp_run_test_set:1: Creating test set /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi database record
     [22/05/2016 20:51:05.926] Debug(1): hydratk.extensions.yoda.testobject:run:2: Running test scenario ts-01
     [22/05/2016 20:51:05.952] Debug(1): hydratk.extensions.yoda.testobject:run:1: Running test scenario ts-01
     *** scenario 1/case 1/condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED
     *** scenario 1/case 1/condition 2: PASSED
     *** scenario 1/case 2/condition 1: PASSED
     [22/05/2016 20:51:06.106] Debug(1): hydratk.extensions.yoda.testobject:run:1: Running test scenario ts-02
     *** scenario 2/case 1/condition 1: PASSED
     [22/05/2016 20:51:06.837] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Got context switch, active tickets: 2
     [22/05/2016 20:51:06.838] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Checking ticket_id 1463943065.79-0-1
     [22/05/2016 20:51:07.841] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Got context switch, active tickets: 1
     [22/05/2016 20:51:07.842] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Checking ticket_id 1463943065.8-0-2
     [22/05/2016 20:51:08.845] Debug(1): hydratk.extensions.yoda.yoda:pp_app_check:0: Got context switch, active tickets: 0
     [22/05/2016 20:51:08.855] Debug(1): hydratk.extensions.yoda.testresults.handlers.console:create:0: Creating console output

     +--------------------------------------------------------------+
     |Test Run: test sets: 2, tests - total: 6, failed: 1, passed: 5|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi
       Test Scenario: Example test scenario, tests - total: 2, failed: 1, passed: 1
         Test Case: Example test case
           Test Condition: Example test condition 2
                 Expected Result: x-y != 2
                 Actual Result: 3
                 Log: x-y != 2

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 1, tests - total: 3, failed: 0, passed: 3
       Test Scenario: scenario 2, tests - total: 1, failed: 0, passed: 1
     [22/05/2016 20:51:08.867] Debug(1): hydratk.core.corehead:_stop_app:0: Stopping application
     [22/05/2016 20:51:09.870] Debug(1): hydratk.core.masterhead:destroy_core_threads:0: Destroying core thread id: 1
     [22/05/2016 20:51:10.539] Debug(1): hydratk.core.corehead:_c_worker:1: Terminating work
     [22/05/2016 20:51:10.542] Debug(1): hydratk.core.masterhead:destroy_core_threads:0: Destroying core thread id: 2
     [22/05/2016 20:51:11.549] Debug(1): hydratk.core.corehead:_c_worker:2: Terminating work
     [22/05/2016 20:51:11.553] Debug(1): hydratk.core.masterhead:destroy_core_threads:0: Destroying core thread id: 3
     [22/05/2016 20:51:12.381] Debug(1): hydratk.core.corehead:_c_worker:3: Terminating work
     [22/05/2016 20:51:12.388] Debug(1): hydratk.core.masterhead:destroy_core_threads:0: Destroying core thread id: 4
     [22/05/2016 20:51:12.390] Debug(1): hydratk.core.corehead:_c_worker:4: Terminating work
     [22/05/2016 20:51:12.401] Debug(1): hydratk.core.corehead:_c_observer:0: PID file deleted: /tmp/hydratk/hydra.pid
     [22/05/2016 20:51:12.402] Debug(1): hydratk.core.bootstrapper:run_app:0: Application exit      