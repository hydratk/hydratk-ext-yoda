.. _module_ext_yoda_main:

Main
====

This sections contains module documentation of main yoda modules.

bootstrapper
^^^^^^^^^^^^

Module provides bootstrapper (method run_app) for Yoda extension. 
You can run it in standalone mode using method command yoda (i.e. installed to /usr/local/bin/yoda).
Unit tests available at hydratk/extensions/yoda/bootstrapper/01_methods_ut.jedi

algorithm
^^^^^^^^^

Yoda test execution process

 .. graphviz::
   
   digraph G {
      graph [rank=TB,splines=ortho,ranksep="0.50",nodesep="0.70",bgcolor="transparent"]
      
      start [shape=circle,fillcolor=gray]
      end [shape=doublecircle]
      init_repo [shape=box, style=rounded, label="Initialize repositories"]
      get_tests [shape=box, style=rounded, label="Get test files from path"]                
      create_run [shape=box, style=rounded, label="Create test run in DB"]
      proc_tests [shape=box, style=rounded, label="Process test sets in loop"]
      proc_finish [shape=diamond, label="Is processing finished ?"]
      create_set [shape=box, style=rounded, label="Create test set in DB"]
      run_set [shape=box, style=rounded, label="Run test set"]
      update_set [shape=box, style=rounded, label="Update test set in DB"]
      update_run [shape=box, style=rounded, label="Update test run in DB"]
      check_res [shape=box, style=rounded, label="Check test results"]

      start -> init_repo
      init_repo -> get_tests -> create_run -> proc_tests
      proc_tests -> proc_finish
      proc_finish -> create_set[constraint=false] 
      create_set -> run_set -> update_set -> proc_tests      
      proc_finish -> update_run[constraint=true] 
      update_run -> check_res 
      check_res -> end

   }

yoda
^^^^

Modules provides class Extension inherited from class hydratk.core.extension.Extension.
Unit tests available at hydratk/extensions/yoda/yoda/01_methods_ut.jedi, 02_methods_ut.jedi

**Attributes** :

* _test_repo_root - root directory of yoda repository (default /var/local/hydratk/yoda)
* _templates_repo - yoda tests directory (root/yoda-tests)
* _helpers_repo - yoda helpers directory (root/helpers)
* _libs_repo - yoda libraries directory (root/lib)
* _test_run
* _current_test_base_path
* _use_helpers_dir
* _use_lib_dir   
* _test_engine 
* _test_results_db
* _test_results_output_create - enable results creation (enabled by default)
* _test_results_output_handler - results handler (supported console, planned text, html)
* _run_mode - MasterHead run mode
* _pp_attr - test run status for parallel processing (started, completed)
* _active_tickets - list of tickets in message queue for parallel processing

**Methods** :

* _init_extension

Method sets extension metadata (id, name, version, author, year).
Sets _test_results_output_create, _test_results_output_handler according to configuration.
Initializes yoda repositories.

* _check_dependencies

Method checks if all required modules are installed.

* _uninstall

Method returns additional uninstall data.

* _init_repos

Method sets _test_repo_root, _libs_repo, _templates_repo, _helpers_repo according to configuration.

* _update_repos

Method updates repositories according to current root.

* _register_actions

Method registers actions hooks according to profile htk (default mode) or yoda (standalone mode).
It registers event hooks htk_on_cmd_options, yoda_before_init_tests, htk_on_cworker_init, htk_after_load_extensions and initializes TestEngine.

* check_pp_mode

Method registers event hook htk_on_cobserver_ctx_switch for parallel processing (run_mode = 2). 
Initializes libraries and helpers.

* _register_htk_actions

Method registers action hooks for default mode.

commands - yoda-run, yoda-simul, yoda-create-test-results-db, yoda-create-testdata-db
long options - yoda-test-path, yoda-test-repo-root-dir, yoda-db-results-dsn, yoda-db-testdata-dsn, yoda-test-run-name, yoda-test-results-output-create,
yoda-test-results-output-handler

* _register_standalone_actions

Method registers action hooks for standalone mode.

commands - run, simul, create-test-results-db, create-testdata-db, help
long options - test-path, test-repo-root-dir, db-results-dsn, db-testdata-dsn, test-run-name, test-results-output-create, test-results-output-handler
short options - tp, rd, oc, oh, rn
global options - config, debug, debug-channel, language, run-mode, force, interactive, home

* pp_app_check

Method is triggered by event htk_on_cobserver_ctx_switch. It checks _active_tickets (tickets in message queue) and deletes complemented tickets.
When the queue is empty it finishes test run processing (update db record). It fires event yoda_before_check_results and checks the output.
After that stops whole application.

* create_test_results_db

Method handles command yoda-create-test-results-db and creates database storage for results. It gets DSN from configuration and creates db using method create_database.

  .. code-block:: bash
  
     htk --yoda-db-results-dsn sqlite:/var/local/hydratk/yoda/db_results/test.db3 yoda-create-test-results-db
     yoda --db-results-dsn sqlite:/var/local/hydratk/yoda/db_results/test.db3 create-test-results-db

* create_testdata_db

Method handles command yoda-create-testdata-db and creates database storage for data. It gets DSN from option yoda-db-testdata-dsn or configuration. 
Database is created in directory root/db_testdata. It executes scripts db_struct.sql (tables) and db_data.sql (tables content). Database can be recreated by option force.

  .. code-block:: bash
  
     htk --yoda-db-testdata-dsn sqlite:/var/local/hydratk/yoda/db_testdata/test.db3 yoda-create-testdata-db
     yoda --db-testdata-dsn sqlite:/var/local/hydratk/yoda/db_testdata/test.db3 create-testdata-db

* init_check

Method is triggered by event htk_on_cmd_options. It checks for options yoda-test-repo-root-dir, yoda-test-results-output-create, yoda-test-results-output-handler, 
yoda-db-results-dsn. These options override defaults settings from configuration. Options yoda-test-run-name is used to set given name of the test run.

* init_test_simul

Method handles command yoda-simul and initializes tests in simulation mode.

  .. code-block:: bash
  
     # options are similar to command yoda-run
     htk --yoda-test-path test/test.jedi yoda-simul
     yoda --test-path test/test.jedi simul

* init_test_results_db

Method sets results database reference in test engine. It gets DSN from configuration.

* check_test_results_db

Method sets results database reference in test engine. It gets DSN from configuration. If database is not installed it is automatically created 
when enabled by configuration.

* init_tests

Method handles command yoda-run. It sets repositories in test engine, fires event yoda_before_init_tests and gets path from option yoda-test-path.
When path is absolute the tests will be executed in global area. When path is relative or not specified the will be execute in inrepo area.
Method searches path for test files and fires event yoda_before_process_tests where test_files can be rewritten.

Processes all tests. When the tests are executed in parallel mode it fires event yoda_before_check_results and waits for completion.

  .. code-block:: bash
  
     # run all tests in repository
     htk yoda-run 
     yoda run
     
     # tests in repository test (relative path to root)
     htk --yoda-test-path test yoda-run
     yoda --test-path test run
     
     # concrete test file
     htk --yoda-test-path test/test.jedi yoda-run
     htk --test-path test/test.jedi run
     
     # filtering (only 1st condition will)
     htk --yoda-test-path test/test.jedi:ts-01:tc-01:tco-01 yoda-run
     yoda --test-path test/test.jedi:ts-01:tc-01:tco-01 run
     
     # own repository
     htk --yoda-test-repo-root-dir /var/local/hydratk --yoda-test-path test.jedi yoda-run
     yoda -test-repo-root-dir /var/local/hydratk -test-path test.jedi run
     
     # custom test run name
     htk --yoda-test-run-name test yoda-run
     yoda --test-run-name test run
     
     # own results database
     htk --yoda-db-results-dsn sqlite:/var/local/hydratk/yoda/db_results/test.db3 yoda-run
     yoda --db-results-dsn sqlite:/var/local/hydratk/yoda/db_results/test.db3 run

* init_helpers

Method adds helpers repository to Python path. It fires event yoda_before_append_helpers_dir where repository can be rewritten.

* init_libs

Method adds libraries repository to Python path. It fires event yoda_before_append_libs_dir where repository can be rewritten.

* process_tests

Method processes test files. First it create test run record in database. For each test file it fires event yoda_before_parse_test_file where
the file can be rewritten. The processing is handled by method process_test_set or pp_process_test_set (if executed in single or parallel mode).
Test run processing can be stopped by exception BreakTestRun. When test run is finished it updates its database record.

* pp_process_test_set

Method creates new ticket for test set and sends it to message queue for further processing in parallel mode (handled by method pp_run_test_set).

* pp_run_test_set

Method loads test set content from file. If correctly parsed it creates database record and runs the set in parallel mode. When finished it updates record.

* process_test_set

Method loads test set content from file. If correctly parsed it creates database record and runs the set in single mode. When finished it updates record.

* _check_results

Method prepares results using requested output handler. First it fires event yoda_on_check_results. 

configuration
^^^^^^^^^^^^^

Configuration is stored in /etc/hydratk/conf.d/hydratk-ext-yoda.conf

* test_repo_root - yoda repository directory (default /var/local/hydratk/yoda)
* db_results_autocreate - create results database within execution (default 1)
* db_results_dsn - DSN of results database (default sqlite:/var/local/hydratk/yoda/db_results/db_results.db3)
* auto_break - exception which breaks the execution (default break_test_set)
* test_results_output_create - prepare results output (default 1)
* test_results_output_handler - list of output handlers (console supported now, planned handlers test, html)
* db_testdata_dsn - DSN of test data database (default sqlite:/var/local/hydratk/yoda/db_testdata/testdata.db3)    