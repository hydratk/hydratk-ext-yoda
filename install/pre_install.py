# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from os import system

def run_pre_install(argv):  
    
    requires = cfg['modules']
    
    if (cmd.is_install_cmd(argv)):      
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            requires = globals()[task](requires)          
    
    return requires 

def install_libs_from_repo(requires):       
    
    pckm = cmd.get_pck_manager()[0]  
         
    libs = cfg['libs']    
    for key in libs.keys():
        if (key in requires):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)   
                
    return requires
                
def install_pip(requires):   
    
    system('pip install lxml>=3.3.3')
    requires.append('lxml>=3.3.3')
    return requires                           