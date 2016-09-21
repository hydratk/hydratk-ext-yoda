.. _tutor_yoda_tut3_reporting:

Tutorial 3: Reporting
=====================

This section will show Yoda reporting features.

Initialization
^^^^^^^^^^^^^^

Yoda provides reporting database implemented using SQLite (file database).
When you execute some test the database is created by default in /var/local/hydratk/yoda/db_results.

  .. code-block:: bash
  
     $ htk --yoda-test-path test/test.jedi yoda-run
    
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED
     
     $ ls -l /var/local/hydratk/yoda/db_results
     
     db_results.db3
     
You can see the database content using command sqlite3 and its command .dump.

  .. code-block:: sql
  
     $ sqlite3 db_results.db3
     
     SQLite version 3.8.2 2013-12-06 14:53:30
     Enter ".help" for instructions
     Enter SQL statements terminated with a ";"
     
     $ sqlite> .dump
     
     PRAGMA foreign_keys=OFF;
     BEGIN TRANSACTION;
     CREATE TABLE test_run(
                           id VARCHAR NOT NULL, -- unique string + timestamp + process id
                           name VARCHAR,
                           start_time INTEGER NOT NULL,
                           end_time INTEGER NOT NULL, 
                           total_tests INTEGER,
                           failed_tests INTEGER,
                           passed_tests INTEGER,
                           log BLOB,
                           struct_log BLOB,
                           PRIMARY KEY(id)
                          );
     INSERT INTO "test_run" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','Undefined',1.46392220404155302048e+09,1.46392220414224290842e+09,2,1,1,'','(dp1
     .');
     CREATE TABLE test_set(
                           id VARCHAR NOT NULL, -- test_run.id + test_set.tset_id
                           tset_id VARCHAR NOT NULL, -- test set path 
                           test_run_id VARCHAR NOT NULL,
                           start_time INTEGER NOT NULL,
                           end_time INTEGER NOT NULL, 
                           total_tests INTEGER,
                           failed_tests INTEGER,
                           passed_tests INTEGER,
                           log BLOB,
                           struct_log BLOB,
                           PRIMARY KEY(id),
                           FOREIGN KEY(test_run_id) REFERENCES test_run(id)
                          );
    INSERT INTO "test_set" VALUES('8dd1eb2d6bb0409a352e83f35ee6eddf','/var/local/hydratk/yoda/yoda-tests/test/test.jedi','8c7c269498cc9afd3e777ab4ac18eafc',1.46392220407623696327e+09,1.46392220414043593406e+09,2,1,1,'','(dp1
    .');
    CREATE TABLE test_scenario(
                               id VARCHAR NOT NULL, -- test_run.id + test_set.id + TestScenario._num
                               ts_id VARCHAR NOT NULL,
                               test_run_id VARCHAR NOT NULL,
                               test_set_id VARCHAR NOT NULL,
                               start_time INTEGER NOT NULL,
                               end_time INTEGER NOT NULL, 
                               total_tests INTEGER,
                               failed_tests INTEGER,
                               passed_tests INTEGER,
                               prereq_passed INTEGER,
                               postreq_passed INTEGER,
                               events_passed INTEGER,
                               failures INTEGER,
                               log BLOB,
                               struct_log BLOB,
                               PRIMARY KEY(id),
                               FOREIGN KEY(test_set_id) REFERENCES test_set(id)
                              );
    INSERT INTO "test_scenario" VALUES('be79ac31b234ebd2e64578075711a0cf','ts-01','8c7c269498cc9afd3e777ab4ac18eafc','8dd1eb2d6bb0409a352e83f35ee6eddf',1.46392220408862590783e+09,1.4639222041292090416e+09,2,1,1,NULL,NULL,NULL,1,'','(dp1
    .');
    CREATE TABLE test_case(
                           id VARCHAR NOT NULL, -- test_run.id + test_set.id + test_scenario.id + TestCase._num
                           tca_id VARCHAR NOT NULL,
                           test_run_id VARCHAR NOT NULL,
                           test_set_id VARCHAR NOT NULL,
                           test_scenario_id VARCHAR NOT NULL,
                           start_time INTEGER NOT NULL,
                           end_time INTEGER NOT NULL, 
                           total_tests INTEGER,
                           failed_tests INTEGER,
                           passed_tests INTEGER,
                           events_passed INTEGER,
                           failures INTEGER,
                           log BLOB,
                           struct_log BLOB,
                           PRIMARY KEY(id),
                           FOREIGN KEY(test_scenario_id) REFERENCES test_scenario(id)
                          );
    INSERT INTO "test_case" VALUES('1b49e665c38a956c32d4a2eab33072f6','tc-01','8c7c269498cc9afd3e777ab4ac18eafc','8dd1eb2d6bb0409a352e83f35ee6eddf','be79ac31b234ebd2e64578075711a0cf',1463922204.09805,1.46392220412294888493e+09,2,1,1,NULL,1,'','(dp1
    .');
    CREATE TABLE test_condition(
                                id VARCHAR NOT NULL,  -- test_run.id + test_set.id + test_scenario.id + test_case.id + TestCondition._num
                                tco_id VARCHAR NOT NULL,
                                test_run_id VARCHAR NOT NULL,
                                test_set_id VARCHAR NOT NULL,
                                test_scenario_id VARCHAR NOT NULL,
                                test_case_id VARCHAR NOT NULL,
                                start_time INTEGER NOT NULL,
                                end_time INTEGER NOT NULL, 
                                expected_result VARCHAR,                        
                                test_result VARCHAR,
                                test_resolution VARCHAR,
                                events_passed INTEGER,
                                test_exec_passed INTEGER,
                                validate_exec_passed INTEGER,   
                                log BLOB,
                                struct_log BLOB,
                                PRIMARY KEY(id),
                                FOREIGN KEY(test_case_id) REFERENCES test_case(id)
                               );
    INSERT INTO "test_condition" VALUES('0f1104dee0d6cf3cf32cc49924604f66','tco-01','8c7c269498cc9afd3e777ab4ac18eafc','8dd1eb2d6bb0409a352e83f35ee6eddf','be79ac31b234ebd2e64578075711a0cf','1b49e665c38a956c32d4a2eab33072f6',1.46392220410427188878e+09,1.46392220410709190375e+09,NULL,'3','passed',NULL,NULL,NULL,'','(dp1
    .'); 
    INSERT INTO "test_condition" VALUES('43c01b239963e9759cdbad5eecf30d2c','tco-02','8c7c269498cc9afd3e777ab4ac18eafc','8dd1eb2d6bb0409a352e83f35ee6eddf','be79ac31b234ebd2e64578075711a0cf','1b49e665c38a956c32d4a2eab33072f6',1.46392220411347198484e+09,1.46392220411663293837e+09,'x-y != 2','3','failed',NULL,NULL,NULL,'x-y != 2','(dp1
    .');
    CREATE TABLE custom_data(
                             test_run_id VARCHAR NOT NULL,
                             test_obj_id VARCHAR NOT NULL, -- test_run.id, test_set.id ..
                             test_obj_name VARCHAR NOT NULL, -- test_run, test_set, ...
                             key VARCHAR NOT NULL,
                             value VARCHAR NOT NULL,
                             pickled INTEGER,
                             FOREIGN KEY(test_run_id) REFERENCES test_run(id)
                            );
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','desc','Contains sample test case',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','version','1.0',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','name','Example test scenario',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','author','Test User <user@test.com>',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','1b49e665c38a956c32d4a2eab33072f6','Test-Case','desc','Contains sample test condition',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','1b49e665c38a956c32d4a2eab33072f6','Test-Case','name','Example test case',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','0f1104dee0d6cf3cf32cc49924604f66','Test-Condition','desc','This conditions should pass',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','0f1104dee0d6cf3cf32cc49924604f66','Test-Condition','name','Example test condition 1',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','43c01b239963e9759cdbad5eecf30d2c','Test-Condition','desc','This conditions should fail',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','43c01b239963e9759cdbad5eecf30d2c','Test-Condition','name','Example test condition 2',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','1b49e665c38a956c32d4a2eab33072f6','Test-Case','desc','Contains sample test condition',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','1b49e665c38a956c32d4a2eab33072f6','Test-Case','name','Example test case',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','desc','Contains sample test case',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','version','1.0',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','name','Example test scenario',0);
    INSERT INTO "custom_data" VALUES('8c7c269498cc9afd3e777ab4ac18eafc','be79ac31b234ebd2e64578075711a0cf','Test-Scenario','author','Test User <user@test.com>',0);
    COMMIT;
    
    sqlite> 
    
When you execute second run the database already exists and is updated only.    
    
Structure
^^^^^^^^^

Database structure follows test script format.
Each level set, scenario, case and conditions has its own table.

Table test_run is used to store summary of each execution.

Table custom_data is used to store metadata of each level.   
    
 .. graphviz::
   
   digraph db_format {
      graph [rankdir=TB]
      node [shape=box, style=filled, color=white, fillcolor=lightgrey]
    
      test_run
      test_set
      test_scenario
      test_case
      test_condition
      custom_data   
      
      test_run -> test_set
      test_run -> test_scenario
      test_run -> test_case
      test_run -> test_condition
      
      test_set -> test_scenario
      test_scenario -> test_case
      test_case -> test_condition
      
      test_run -> custom_data
      test_set -> custom_data
      test_scenario -> custom_data
      test_case -> custom_data
      test_condition -> custom_data

   }    
   
It is quite straightforward to prepare your own queries.

Configuration
^^^^^^^^^^^^^

Database file is created automatically by default configuration.
You can configure the location via parameter db-results-dsn.

  .. code-block:: yaml
  
     Extensions:
     Yoda:
       db_results_autocreate: 1
       db_results_dsn: sqlite:/var/local/hydratk/yoda/db_results/db_results.db3  
       
Also you can use option --yoda-db-results-dsn.

  .. code-block:: bash
  
     $ htk --yoda-db-results-dsn sqlite:/var/local/hydratk/yoda/db_results/db_report.db3 --yoda-test-path test/test.jedi yoda-run   
     
     $ ls /var/local/hydratk/yoda/db_results
     
     db_report.db3 
     
If you want to create the database before first execution use command yoda-create-test-results-db.
The command creates tables only, reporting data are stored after execution.

  .. code-block:: bash
  
     $ htk --yoda-db-results-dsn sqlite:/var/local/hydratk/yoda/db_results/db_report.db3 yoda-create-test-results-db
     
     $ ls /var/local/hydratk/yoda/db_results
     
     db_report.db3   
     
Database is created automatically if it doesn't exist. It is possible to disable it via configuration parameter db_results_autocreate: 0.                  