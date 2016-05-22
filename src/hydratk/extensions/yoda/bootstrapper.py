# -*- coding: utf-8 -*-
"""Providing custom bootstrapper for yoda standalone app

.. module:: yoda.bootstrapper
   :platform: Unix
   :synopsis: Providing custom bootstrapper for yoda standalone app
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 2:
    reload(sys)
    sys.setdefaultencoding('UTF8')
    
def run_app(): 
    """Methods runs yoda standalone application
        
    Args:
       none
    
    Returns:
       void
            
    """ 
               
    from hydratk.core.masterhead import MasterHead    
    mh = MasterHead.get_head()
    mh.set_cli_cmdopt_profile('yoda')            
    mh.run_fn_hook('h_bootstrap')
    trn = mh.get_translator()  
    mh.dmsg('htk_on_debug_info', trn.msg('htk_app_exit'), mh.fromhere())                  
    sys.exit(0)