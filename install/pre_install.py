# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd

def run_pre_install(argv):  
    
    if (cmd.is_install_cmd(argv)):      
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            globals()[task]()          

def install_libs_from_repo():       
    
    pckm = cmd.get_pck_manager()[0]  
         
    libs, modules = cfg['libs'], cfg['modules']    
    for key in libs.keys():
        if (key in modules):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)   
                
def install_pip():   
    
    for module in cfg['modules']:
        cmd.install_pip(module)                     