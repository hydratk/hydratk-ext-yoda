.. _module_ext_yoda_testresults:

Test results
============

This sections contains module documentation of main testresults modules.
Unit tests available at hydratk/extensions/yoda/testresults/testresults/01_methods_ut.jedi

Class TestResultsDB
^^^^^^^^^^^^^^^^^^^

**Attributes** :

* _mh - MasterHead reference
* _trdb - results database reference
* _dsn - DSN of results database
* _custom_data_filter - test object tags not stored in database (per TestScenario, TestCase, TestCondition)

**Properties (Getters)** :

* trdb - returns _trdb
* custom_data_filter - returns _custom_data_filter

**Methods** :

* __init__

Method sets DBO reference with given DSN.

* db_check_ok

Method checks if database is correctly installed. Reads count of tables.

* create_database

Method prepares database structure (script is stored in module). Database can be reinstalled if enabled by parameter force.

* db_action

Method executes SQL write query according to given action name.

* db_data

Method executes SQL read query according to given name and returns the output.   

Class TestResultsOutputFactory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Attributes** :

* _mh - MasterHead reference
* _handler_name - console (supported), text, html (planned)
* _handler - handler reference
* _handler_opt - options

**Methods** :

* __init__

Method initializes handler reference. 

* _dispatch_handler_def

Method parses handler definition name:key1=val1:key2:val2 and sets _handler_name, _handler_opt.

* _import_tro_handler

Method imports requested handler module.

console
^^^^^^^

Module provides class TestResultsOutputHandler which implements console handler.

**Attributes** :

* _options - handler options
* _db_dsn - database DSN
* _db_con - database connection

**Methods** :

* __init__ 

Method sets _db_dsn, _options.

* create

Methods prints summary report of test execution. It reads test results from database. 
If some test scenario fails the method prints details for error localization (scenario, case, condition, actual and expected result). 

Database tables
^^^^^^^^^^^^^^^

**test_run**:

Storage for test runs

============  ======== ======== ===========
Column        Datatype Nullable Constraint 
============  ======== ======== ===========
id            varchar     N     primary key
name          varchar     Y
start_time    integer     N
end_time      integer     N
total_tests   integer     Y
failed_tests  integer     Y
passed_tests  integer     Y
log           blob        Y
struct_log    blob        Y 
============  ======== ======== ===========    

**test_set**:

Storage for test sets

============  ======== ======== ==========================
Column        Datatype Nullable Constraint 
============  ======== ======== ==========================
id            varchar     N     primary key
tset_id       varchar     N
test_run_id   varchar     N     foreign key to test_run.id
start_time    integer     N
end_time      integer     N
total_tests   integer     Y
failed_tests  integer     Y
passed_tests  integer     Y
log           blob        Y
struct_log    blob        Y 
============  ======== ======== ==========================   

**test_scenario**:

Storage for test scenarios

==============  ======== ======== =======================
Column          Datatype Nullable Constraint 
==============  ======== ======== =======================
id              varchar     N     primary key
ts_id           varchar     N
test_run_id     varchar     N     
test_set_id     varchar     N     foreign key test_set.id
start_time      integer     N
end_time        integer     N
total_tests     integer     Y
failed_tests    integer     Y
passed_tests    integer     Y
prereq_passed   integer     Y
postreq_passed  integer     Y 
events_passed   integer     Y
failures        integer     Y 
log             blob        Y
struct_log      blob        Y 
==============  ======== ======== =======================   

**test_case**:

Storage for test cases

================  ======== ======== ===============================
Column            Datatype Nullable Constraint 
================  ======== ======== ===============================
id                varchar     N     primary key
tca_id            varchar     N
test_run_id       varchar     N     
test_set_id       varchar     N     
test_scenario_id  varchar     N     foreign key to test_scenario.id
start_time        integer     N
end_time          integer     N
total_tests       integer     Y
failed_tests      integer     Y
passed_tests      integer     Y
events_passed     integer     Y
failures          integer     Y 
log               blob        Y
struct_log        blob        Y 
================  ======== ======== ===============================  

**test_condition**:

Storage for test conditions

====================  ======== ======== ===========================
Column                Datatype Nullable Constraint 
====================  ======== ======== ===========================
id                    varchar     N     primary key
tco_id                varchar     N
test_run_id           varchar     N     
test_set_id           varchar     N     
test_scenario_id      varchar     N     
test_case_id          varchar     N     foreign key to test_case.id
start_time            integer     N
end_time              integer     N
expected_result       varchar     Y
test_result           varchar     Y
test_resolution       varchar     Y
events_passed         integer     Y
test_exec_passed      integer     Y
validate_exec_passed  integer     Y
log                   blob        Y
struct_log            blob        Y 
====================  ======== ======== ===========================

**custom_data**:

Storage for for custom data

=============  ======== ======== =======================
Column         Datatype Nullable Constraint 
=============  ======== ======== =======================
id             varchar     N     primary key
test_run_id    varchar     N     foreign key test_run.id
test_obj_id    varchar     N     
test_obj_name  varchar     N
key            varchar     N
value          varchar     Y
pickled        integer     Y 
=============  ======== ======== =======================  

**custom_data_opt**:

Storage for for custom data options

===========  ======== ======== ==========================
Column       Datatype Nullable Constraint 
===========  ======== ======== ==========================
id           varchar     N     primary key
custom_data  varchar     N     foreign key custom_data.id
opt_name     varchar     N     
opt_value    varchar     Y
===========  ======== ======== ==========================  