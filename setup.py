# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sys import argv
from install.pre_install import run_pre_install
from install.post_install import run_post_install

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

run_pre_install(argv)

entry_points = {
                'console_scripts': [
                    'yoda = hydratk.extensions.yoda.bootstrapper:run_app'                               
                ]
               }          
                
setup(
      name='hydratk-ext-yoda',
      version='0.2.3a.dev1',
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

run_post_install(argv)