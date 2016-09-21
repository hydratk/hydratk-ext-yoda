.. _tutor_yoda_tut6_break:

Tutorial 6: Breaking the tests
==============================

This section will show you how to break tests if some error occurs.

Break whole run
^^^^^^^^^^^^^^^

You can break whole test run.
When tested application is not available, all tests will fail and makes no sense to execute them.

Let's create script test_break.jedi and put it directory with the sample test.jedi (rename it to wtest.jedi).

  .. code-block:: yaml
  
     Test-Scenario-1:
       id: ts-01
       name: scenario 1
       
       pre-req: |
         result = False
         
         if (result != True):
             this.break_test_run('run')  

       Test-Case-1:
         id: tc-01
         name: case 1
              
         Test-Condition-1:
           id: tco-01
           name: condition 1

           test: |
             this.test_result = False
 
             if (this.test_result != True):
                 this.break_test_set('set')

           validate: |
             assert (this.test_result == True)
        
        Test-Condition-2:
          id: tco-02
          name: condition 2

          test: |          
             this.test_result = False
 
             if (this.test_result != True):
                 this.break_test_scenario('scenario')          

          validate: |
              assert (this.test_result == True)

      Test-Case-2:
        id: tc-02
        name: case 2

        Test-Condition-1:
          id: tco-01
          name: condition 1
          
          test: |      
             this.test_result = True
 
             if (this.test_result != True):
                 this.break_test_case('case')      

        
          validate: |
            assert (this.test_result == True)

    Test-Scenario-2:
      id: ts-02
      name: scenario 2

      Test-Case-1:
        id: tc-01
        name: case 1

        Test-Condition-1:
          id: tco-01
          name: condition 1

          test: |          
             this.test_result = True
 
             if (this.test_result != True):
                 this.break_test_condition('condition')          
          
          validate: |
            assert (this.test_result == True)
          
Simulation passes and wtest.jedi is checked as second.          
            
  .. code-block:: bash
  
     $ htk --yoda-test-path test yoda-simul
     
     *** scenario 1/case 1/condition 1: PASSED
     *** scenario 1/case 1/condition 2: PASSED
     *** scenario 1/case 2/condition 1: PASSED
     *** scenario 2/case 1/condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 1: PASSED
     *** Example test scenario/Example test case/Example test condition 2: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 2, tests - total: 6, failed: 0, passed: 6|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 1, tests - total: 3, failed: 0, passed: 3
       Test Scenario: scenario 2, tests - total: 1, failed: 0, passed: 1

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi
       Test Scenario: Example test scenario, tests - total: 2, failed: 0, passed: 2  
       
When you execute run, failed pre-requirement in scenario 1 breaks whole run.
All tests are skipped and second script was not executed.       
       
  .. code-block:: bash
  
     $ htk --yoda-test-path test yoda-run
     
     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 0, failed: 0, passed: 0|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 1, tests - total: 0, failed: 0, passed: 0                          

Break set
^^^^^^^^^

You can break test set. Remaining test sets are executed normally.

Change the code to avoid run break.

  .. code-block:: yaml
  
     pre-req: |
       result = True 

       if (result != True):
           this.break_test_run('run')
           
When you execute run, first condition breaks test set.
All tests are skipped but second script is executed.           
           
  .. code-block:: bash
  
     $ htk --yoda-test-path test yoda-run
     
     +--------------------------------------------------------------+
     |Test Run: test sets: 2, tests - total: 3, failed: 1, passed: 1|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 1, tests - total: 1, failed: 0, passed: 0

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/wtest.jedi
       Test Scenario: Example test scenario, tests - total: 2, failed: 1, passed: 1
                     
Break scenario
^^^^^^^^^^^^^^

You can break test scenario. Remaining test scenarios are executed normally.
     
  .. code-block:: bash
  
     $ htk --yoda-test-path test/test_break.jedi yoda-run
     
     *** scenario 2/case 1/condition 1: PASSED
 
     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 4, failed: 0, passed: 1|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 2, tests - total: 1, failed: 0, passed: 1
       Test Scenario: scenario 1, tests - total: 3, failed: 0, passed: 0

Break case
^^^^^^^^^^

You can break test case. Remaining test cases are executed normally.

  .. code-block:: bash
  
     $ htk --yoda-test-path test/test_break.jedi yoda-run
     
     *** scenario 1/case 1/condition 1: PASSED
     *** scenario 1/case 1/condition 2: PASSED
     *** scenario 2/case 1/condition 1: PASSED
 
     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 4, failed: 0, passed: 3|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 2, tests - total: 1, failed: 0, passed: 1
       Test Scenario: scenario 1, tests - total: 3, failed: 0, passed: 2
     

Break condition
^^^^^^^^^^^^^^^

You can break test condition. Remaining test conditions are executed normally.

  .. code-block:: bash
  
     $ htk --yoda-test-path test/test_break.jedi yoda-run
     
     *** scenario 1/case 1/condition 1: PASSED
     *** scenario 1/case 1/condition 2: PASSED
     *** scenario 1/case 2/condition 1: PASSED

     +--------------------------------------------------------------+
     |Test Run: test sets: 1, tests - total: 4, failed: 0, passed: 3|
     +--------------------------------------------------------------+

     Test Set: /var/local/hydratk/yoda/yoda-tests/test/test_break.jedi
       Test Scenario: scenario 2, tests - total: 1, failed: 0, passed: 0
       Test Scenario: scenario 1, tests - total: 3, failed: 0, passed: 3