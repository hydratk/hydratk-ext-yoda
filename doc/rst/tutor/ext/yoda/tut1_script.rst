.. _tutor_yoda_tut1_script:

Tutorial 1: Scripting
=====================

This section will show you how to write simple test script.

Format
^^^^^^

Yoda implements own test script format based on YAML (used also for configuration).
The format uses hierarchical structure.

* Test set: test script file, 1st level
* Test scenario: 2nd level, test set can have multiple scenario
* Test case: 3rd level, test scenario can have multiple cases
* Test condition: 4th level, test case can have multiple conditions

 .. graphviz::
   
   digraph script_format {
      graph [rankdir=TB]
      node [shape=box, style=filled, color=white, fillcolor=lightgrey]
    
      test_set
      test_scenario_1
      test_scenario_2
      test_case_1_1
      test_case_1_2
      test_case_2_1
      test_condition_1_1_1
      test_condition_1_1_2
      test_condition_1_2_1
      test_condition_2_1_1      
      
      test_set -> test_scenario_1
      test_set -> test_scenario_2
      test_scenario_1 -> test_case_1_1
      test_scenario_1 -> test_case_1_2
      test_scenario_2 -> test_case_2_1
      test_case_1_1 -> test_condition_1_1_1
      test_case_1_1 -> test_condition_1_1_2
      test_case_1_2 -> test_condition_1_2_1
      test_case_2_1 -> test_condition_2_1_1

   }
   
Scenarios, cases and condition elements have special tags which provide metadata (id, name, description etc.).
Condition elements also contain embedded Python code to be executed.

Example
^^^^^^^

Let's create simple test script test.jedi with 1 scenario, 1 case and 2 conditions (positive and negative). 
Yoda defines own file extensions yoda, jedi. Other extensions are not recognized by execution engine.

  .. code-block:: yaml
  
     Test-Scenario-1:
       id: ts-01
       path: filepath within test repository
       name: Example test scenario
       desc: Contains sample test case
       author: Test User <user@test.com>
       version: 1.0
       
       Test-Case-1:
         id: tc-01
         name: Example test case
         desc: Contains sample test condition
              
         Test-Condition-1:
           id: tco-01
           name: Example test condition 1
           desc: This conditions should pass         
              
           test: |
             x = 8
             y = 5
             this.test_result = x - y
      
           validate: |    
             assert (this.test_result == 3), "x-y != 3"       
             
         Test-Condition-2:
           id: tco-02
           name: Example test condition 2
           desc: This conditions should fail         
              
           test: |
             x = 8
             y = 5
             this.test_result = x - y
      
           validate: |    
             assert (this.test_result == 2), "x-y != 2" 
             
Scenario, case and conditions element titles contains numbering. 
Be careful with it, the execution engine expects increasing sequences starting from 1 with no duplicates and gaps.
Tags id, name are mandatory, other metadata tags are optional but help to understand purpose of test.

Conditions have mandatory elements test and validate with embedded Python code.
Test contains code which tests something. Validate checks the result (whether the condition passed or failed) using assertion.
Notice the usage of | character which instructs Yaml parser to consider the content as executable code.

Following example shows minimum test script structure with multiple elements on each level. Each element id must be unique 
within its level. 

 .. code-block:: yaml
 
    Test-Scenario-1:
      id: ts-01
      name: scenario 1
      
      Test-Case-1:
        id: tc-01
        name: case 1
        
        Test-Condition-1:
          id: tco-01
          name: condition 1
          
          test: |
          validate: |
          
        Test-Condition-2
          id: tco-02
          name: condition 2
          
          test: |
          validate: |
          
      Test-Case-2:
        id: tc-02
        name: case 2
        
        Test-Condition-1:
          id: tco-01
          name: condition 1
          
          test: |
          validate: |
          
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
          validate: |                          