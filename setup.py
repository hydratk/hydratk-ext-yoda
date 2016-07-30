# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sys import argv
from os import path
from subprocess import call

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
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

requires = [
            'hydratk'
           ]
         
files = {
         'etc/hydratk/conf.d/hydratk-ext-yoda.conf'               : '/etc/hydratk/conf.d',
         'var/local/hydratk/yoda/yoda-tests/test1/example1.yoda'  : '/var/local/hydratk/yoda/yoda-tests/test1',
         'var/local/hydratk/yoda/helpers/yodahelpers/__init__.py' : '/var/local/hydratk/yoda/helpers/yodahelpers',
         'var/local/hydratk/yoda/lib/yodalib/__init__.py'         : '/var/local/hydratk/yoda/lib/yodalib'            
        }

entry_points = {
                'console_scripts': [
                    'yoda = hydratk.extensions.yoda.bootstrapper:run_app'                               
                ]
               }          
                
setup(
      name='hydratk-ext-yoda',
      version='0.2.1',
      description='Test Automation Tool',
      long_description=readme,
      author='Petr Czaderna',
      author_email='pc@hydratk.org',
      url='http://extensions.hydratk.org/yoda',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False, 
      entry_points=entry_points      
     )

if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):
    
    for file, dir in files.items():    
        if (not path.exists(dir)):
            call('mkdir -p {0}'.format(dir), shell=True)
            
        call('cp {0} {1}'.format(file, dir), shell=True) 
        
    call('chmod -R a+r /etc/hydratk', shell=True)
    call('chmod -R a+rwx /var/local/hydratk', shell=True)