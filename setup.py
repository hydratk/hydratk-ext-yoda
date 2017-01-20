# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import argv
import hydratk.lib.install.command as cmd
import hydratk.lib.install.task as task

with open("README.rst", "r") as f:
    readme = f.read()
    
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Programming Language :: Python :: Implementation :: PyPy", 
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

config = {
  'pre_tasks' : [
                 task.install_libs,
                 task.install_modules
                ],

  'post_tasks' : [
                  task.set_config,
                  task.copy_files,
                  task.set_access_rights,
                  task.set_manpage
                 ],
          
  'modules' : [    
               'hydratk',     
               'lxml>=3.3.3',  
               'pytz>=2016.6.1',                
               'simplejson>=3.8.2'                                                 
              ],
          
  'files' : {
             'config'  : {
                          'etc/hydratk/conf.d/hydratk-ext-yoda.conf' : '/etc/hydratk/conf.d'
                         },
             'data'    : {
                          'var/local/hydratk/yoda/yoda-tests/test1/example1.yoda'  : '/var/local/hydratk/yoda/yoda-tests/test1',
                          'var/local/hydratk/yoda/helpers/yodahelpers/__init__.py' : '/var/local/hydratk/yoda/helpers/yodahelpers',
                          'var/local/hydratk/yoda/lib/yodalib/__init__.py'         : '/var/local/hydratk/yoda/lib/yodalib',
                          'var/local/hydratk/yoda/db_testdata/db_struct.sql'       : '/var/local/hydratk/yoda/db_testdata',
                          'var/local/hydratk/yoda/db_testdata/db_data.sql'         : '/var/local/hydratk/yoda/db_testdata'
                         },
             'manpage' : 'doc/yoda.1'         
            },
          
  'libs' : {
            'lxml>=3.3.3' : {
                             'repo'    : [
                                          'python-lxml'
                                         ],
                             'apt-get' : [
                                          'libxml2-dev',
                                          'libxslt1-dev'
                                         ],
                             'yum'     : [
                                          'libxml2-devel',
                                          'libxslt-devel'
                                         ]
                             }                   
           },
          
  'rights' : {
              '/etc/hydratk'       : 'a+r',
              '/var/local/hydratk' : 'a+rwx'
             }                              
}

task.run_pre_install(argv, config)

entry_points = {
                'console_scripts': [
                    'yoda = hydratk.extensions.yoda.bootstrapper:run_app'                               
                ]
               }          
                
setup(
      name='hydratk-ext-yoda',
      version='0.2.3a.dev2',
      description='Test Automation Tool',
      long_description=readme,
      author='Petr Czaderna, HydraTK team',
      author_email='pc@hydratk.org, team@hydratk.org',
      url='http://extensions.hydratk.org/yoda',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False, 
      entry_points=entry_points,
      keywords='hydratk,testing,test automation,engine',
      requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
      platforms='Linux'      
     )

task.run_post_install(argv, config)