def dummy_method(*args):
    
    return 'True'

tco = {
       'Id'       : 'tco-01',
       'Name'     : 'tco_test',
       'Desc'     : 'Test condition',
       'Test'     : 'a = 1',
       'Validate' : 'assert True'
      }

tc = {
      'Id'               : 'tc-01',
      'Name'             : 'tc_test',
      'Desc'             : 'Test case',
      'Test-Condition-1' : tco
     }

ts = {
      'Id'          : 'ts-01',
      'Path'        : 'yodahelpers/hydratk/extensions/yoda/tscript.py',
      'Name'        : 'ts_test',
      'Desc'        : 'Test scenario',
      'Author'      : 'Petr Rasek <bowman@hydratk.org>',
      'Version'     : '0.1',
      'Test-Case-1' : tc
     }

tset = {
        'Test-Scenario-1' : ts
       }