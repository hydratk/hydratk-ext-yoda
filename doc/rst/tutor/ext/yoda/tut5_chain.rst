.. _tutor_yoda_tut5_chain:

Tutorial 5: Test chaining
=========================

This section will show you how to chain test scripts.

Inline tests
^^^^^^^^^^^^

Test script can execute other inline scripts.

This is very useful when some test depends on other test which already exists and works.
It would be redundant to write same test twice.

Our example shows two scripts: create_group.jedi, assign_member.jedi. The first script creates group. 
The second script assigns member to group. Before you can assign member to group, the group must exist.

As a pre-requirement the group is created first (using method exec_test) and then the member is assigned.
Notice the usage of variable gid (group identifier) which is created in first script and is automatically
visible in second script.

  .. code-block:: yaml
  
     Test-Scenario-1:
       id: ts_01
       path: create_group.jedi
    
       Test-Case-1:
         id: tc_01
  
       Test-Condition-1: 
         id: tco_01

         test: |
           gid = create_group()
           this.test_result = gid
                         
         validate: |   
           assert (this.test_result > 0)     
           
  .. code-block:: yaml
  
     Test-Scenario-1:
       id: ts_01
       path: assign_member.jedi
       
       pre-req: |
         self.exec_test('create_group.jedi')  
    
       Test-Case-1:
         id: tc_01
  
       Test-Condition-1: 
         id: tco_01

         test: |
           member = gen_id()
           result = assign_member(gid, member)
           this.test_result = result
                         
         validate: |   
           assert (this.test_result == True)                                           
   