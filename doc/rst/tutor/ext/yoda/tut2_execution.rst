.. _tutor_yoda_tut2_execution:

Tutorial 2: Test execution
==========================

This section will show you how to execute test script.

Test repository
^^^^^^^^^^^^^^^

Yoda test repository is installed by default to directory /var/local/hydratk/yoda.
See configuration file /etc/hydratk/cond.d/hydratk-ext-yoda.conf.

 .. code-block:: yaml
 
    Extension:
      Yoda:
        package: hydratk.extensions.yoda
        module: yoda
        enabled: 1
        test_repo_root: /var/local/hydratk/yoda
        
  .. note::
  
     Other configuration parameters will be explained later.
     
Repository contains four subdirectories.     
     
* yoda-tests: test scripts
* helpers: auxiliary high level Python modules used in test scripts
* lib: auxiliary low level Python modules used in helpers
* db_results: reporting database

For now you need to store test script into directory yoda-tests. 
Remaining directories will be used later.

Execution
^^^^^^^^^

Now execute the script using command yoda-run.
Second condition failed as you see in the report.

  .. code-block:: bash
  
     $ htk yoda-run 
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED

     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 2, failed: 1, passed: 1|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test.jedi
       Test Scenario: Example test scenario, tests - total: 2, failed: 1, passed: 1
         Test Case: Example test case
           Test Condition: Example test condition 2
             Expected Result: 2
             Actual Result: 3
             Log: x-y != 2

Filter
^^^^^^

The command yoda-run executes every test script found inside repository directory tree.
When there are many test script it is useful to choose only subset which will be executed.
Create new directory test (inside repository root) and move the script there.

Use option --yoda-test-path to execute only scripts in directory test.

  .. code-block:: bash
  
     $ htk --yoda-test-path test yoda-run             
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED
     
If you want to execute requested script only, set the script filename in option.

  .. code-block:: bash
  
     $ htk --yoda-test-path test/test.jedi yoda-run
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED
     
Sometimes you may want to execute only part of the script (requested scenario, case or condition).

  .. code-block:: bash
  
     # scenario ts-01
     $ htk --yoda-test-path test/test.jedi:ts-01 yoda-run
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED     
     
     # case tc-01
     $ htk --yoda-test-path test/test.jedi:ts-01:tc-01 yoda-run
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED     
     
     # condition tco-01
     $ htk --yoda-test-path test/test.jedi:ts-01:tc-01:tco-01 yoda-run
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 1, failed: 0, passed: 1|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test.jedi
       Test Scenario: Example test scenario, tests - total: 1, failed: 0, passed: 1
     
  .. note::
  
     It makes sense to execute part of the script only if there are no dependencies.
     For example if second condition works with variables set if first condition, it won't work.

Own repository
^^^^^^^^^^^^^^
     
Root repository is configurable. Use option --yoda-test-repo-root-dir or parameter test-repo-root in configuration file.

 .. code-block:: yaml
 
    Extension:
      Yoda:
        test_repo_root: /var/local/hydratk
        
The repository must have subdirectories as default repository (yoda-tests etc.)

If you store test script directly in new repository the engine won't find it. 

  .. code-block:: bash
  
     $ htk --yoda-test-repo-root-dir /var/local/hydratk --yoda-test-path test.jedi yoda-run
     
     +--------------------------------------------------------------+
     |Test Run: test sets: 0, tests - total: 0, failed: 0, passed: 0|
     +--------------------------------------------------------------+  

When you move it to subdirectory yoda-tests it will be executed.

  .. code-block:: bash
  
     $ htk --yoda-test-repo-root-dir /var/local/hydratk --yoda-test-path test.jedi yoda-run
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: FAILED          
        
Simulation
^^^^^^^^^^

If you would like to check if the syntactically correct (Python syntax, YAML format) use command yoda-simul.
The embedded code is not executed so nothing happens if there is some mistake.          
         
When the syntax is correct all tests will pass. Even the condition passed because it syntactically correct
and fails only during execution.         
         
  .. code-block:: bash
  
     $ htk --yoda-test-path test/test.jedi yoda-simul 
     
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 2, failed: 0, passed: 2|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test.jedi
       Test Scenario: Example test scenario, tests - total: 2, failed: 0, passed: 2
       
  .. note::
  
     Command yoda-simul supports same options as yoda-run.   
       
Let's make some errors to see how the simulator detects them.

Python syntactical error

  .. code-block:: yaml
  
     test: |
        x = 
        y = 5
        this.test_result = x - y

  .. code-block:: bash
  
     $ htk --yoda-test-path test/test.jedi yoda-simul 
     
     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 1, failed: 0, passed: 0|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test.jedi
       Test Scenario: Example test scenario, tests - total: 1, failed: 0, passed: 0
         Test Case: Example test case
         ! There were problems in test execution: 

     Exception: <type 'exceptions.SyntaxError'>
        Value: invalid syntax (<string>, line 1)
        Trace:
           from: Test set: /var/local/hydratk/yoda/yoda-tests/test/test.jedi
           from:      File "/usr/local/lib/python2.7/dist-packages/hydratk_ext_yoda-0.2.0-py2.7.egg/hydratk/extensions/yoda/testobject.py", line 2566, in run
           from:      compile(self.test,'<string>','exec')
           from:      File "<string>", line 1
           from:      x =
           from:      ^     
           
Duplicate element

  .. code-block:: yaml
  
     Test-Condition-1:
       id: tco-02
       name: Example test condition 2
       desc: This conditions should fail
           
  .. code-block:: bash
   
     $ htk --yoda-test-path test/test.jedi yoda-simul 
     
     # first condition was not executed
     
     *** Example test scenario/Example test case/Example test condition 2: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 1, failed: 0, passed: 1|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test.jedi
       Test Scenario: Example test scenario, tests - total: 1, failed: 0, passed: 1             
       
Gap between elements      
       
  .. code-block:: yaml       
       
     Test-Condition-3:
       id: tco-02
       name: Example test condition 2
       desc: This conditions should fail       
       
  .. code-block:: bash
  
     $ htk --yoda-test-path test/test.jedi yoda-simul 
  
     # second condition was not executed
  
     *** Example test scenario/Example test case/Example test condition 1: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 1, failed: 0, passed: 1|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test.jedi
       Test Scenario: Example test scenario, tests - total: 1, failed: 0, passed: 1
     