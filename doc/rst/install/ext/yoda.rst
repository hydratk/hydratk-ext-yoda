.. install_ext_yoda:

Yoda
====

You have 2 options how to install Yoda extension.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

  .. code-block:: bash
  
     $ sudo pip install --no-binary :all: hydratk-ext-yoda
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-ext-yoda
     
  .. note::
  
     PIP needs option --no-binary to run setup.py install.
     Otherwise it runs setup.py bdist_wheel.    

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-ext-yoda.git
     $ cd ./hydratk-ext-yoda
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://python.org/pypi/hydratk-ext-yoda -O hydratk-ext-yoda.tar.gz
     $ tar -xf hydratk-ext-yoda.tar.gz
     $ cd ./hydratk-ext-yoda
     $ sudo python setup.py install
     
Requirements
^^^^^^^^^^^^     
     
Several python modules are used.
These modules will be installed automatically, if not installed yet.

* hydratk
* lxml
* pytz
* simplejson

Module lxml requires several libraries which will be installed via Linux package managers, if not installed yet.

lxml

* apt-get: python-lxml, libxml2-dev, libxslt1-dev
* yum: python-lxml, libxml2-devel, libxslt-devel   
     
Installation
^^^^^^^^^^^^

See installation example.

  .. code-block:: bash
  
     running install
     running bdist_egg
     running egg_info
     writing requirements to src/hydratk_ext_yoda.egg-info/requires.txt
     writing src/hydratk_ext_yoda.egg-info/PKG-INFO
     writing top-level names to src/hydratk_ext_yoda.egg-info/top_level.txt
     writing dependency_links to src/hydratk_ext_yoda.egg-info/dependency_links.txt
     writing entry points to src/hydratk_ext_yoda.egg-info/entry_points.txt
     reading manifest file 'src/hydratk_ext_yoda.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_ext_yoda.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     creating build/lib.linux-x86_64-2.7/hydratk/extensions
     copying src/hydratk/extensions/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions
     creating build/lib.linux-x86_64-2.7/hydratk/extensions/yoda
     copying src/hydratk/extensions/yoda/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions/yoda
     ...
     
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/extensions/__init__.py to __init__.pyc
     ...
     
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_ext_yoda-0.2.1a0.dev1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_ext_yoda-0.2.1a0.dev1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_ext_yoda-0.2.1a0.dev1-py2.7.egg
     Extracting hydratk_ext_yoda-0.2.1a0.dev1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-ext-yoda 0.2.1a0.dev1 to easy-install.pth file
     Installing yoda script to /usr/local/bin
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_yoda-0.2.1a0.dev1-py2.7.egg
     Processing dependencies for hydratk-ext-yoda==0.2.1a0.dev1
     Finished processing dependencies for hydratk-ext-yoda==0.2.1a0.dev1  

Application installs following (paths depend on your OS configuration)

* yoda command in /usr/local/bin/yoda
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-ext-yoda-0.2.0-py2.7egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-yoda.conf 
* application folder in /var/local/hydratk/yoda
       
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-yoda module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-ext-yoda (0.2.0)
    
Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     Yoda: Yoda v0.2.0 (c) [2014 - 2016 Petr Czaderna <pc@hydratk.org>]
     
Type command htk help and detailed info is displayed.
Type man yoda to display manual page. 

  .. code-block:: bash
  
     $ htk help
     
     Commands:
       yoda-create-test-results-db - creates database for storing test results base on specified dsn configuration
         Options:
           --yoda-db-results-dsn <dsn> - test results database access definition
           --yoda-test-repo-root-dir <path> - test repository root directory
           
       yoda-create-testdata-db - creates database for test data
         Options:
           --yoda-db-testdata-dsn <dsn> - test data database access definition           

       yoda-run - starts the Yoda tester
         Options:
           --yoda-db-results-dsn <dsn> - test results database access definition
           --yoda-test-path <path> - test scenario path
           --yoda-test-repo-root-dir <path> - test repository root directory
           --yoda-test-results-output-create <state> - activates/deactivates native test results output handler
           --yoda-test-run-name <name> - test run identification
           -a, --yoda-test-results-output-handler <type> - set the test results output handler type

       yoda-simul - starts the Yoda tester in test simulation mode
         Options:
           --yoda-db-results-dsn <dsn> - test results database access definition
           --yoda-test-path <path> - test scenario path
           --yoda-test-repo-root-dir <path> - test repository root directory
           --yoda-test-results-output-create <state> - activates/deactivates native test results output handler
           --yoda-test-run-name <name> - test run identification
           -a, --yoda-test-results-output-handler <type> - set the test results output handler type
                  
You can run Yoda also in standalone mode.

  .. code-block:: bash
  
     $ yoda help
     
     Yoda v0.2.0
     (c) 2014 - 2016 Petr Czaderna <pc@hydratk.org>
     Usage: /usr/local/bin/yoda [options] command

     Commands:
       create-test-results-db - creates database for storing test results base on specified dsn configuration
         Options:
           --db-results-dsn <dsn> - test results database access definition
           -tr, --test-repo-root-dir <path> - test repository root directory
           
       create-testdata-db - creates database for test data
         Options:
           --db-testdata-dsn <dsn> - test data database access definition           

       help - prints help
       run - starts the Yoda tester
         Options:
           --db-results-dsn <dsn> - test results database access definition
           -oc, --test-results-output-create <state> - activates/deactivates native test results output handler
           -oh, --test-results-output-handler <type> - set the test results output handler type
           -tn, --test-run-name <name> - test run identification
           -tp, --test-path <path> - test scenario path
           -tr, --test-repo-root-dir <path> - test repository root directory

       simul - starts the Yoda tester in test simulation mode
         Options:
           --db-results-dsn <dsn> - test results database access definition
           -oc, --test-results-output-create <state> - activates/deactivates native test results output handler
           -oh, --test-results-output-handler <type> - set the test results output handler type
           -tn, --test-run-name <name> - test run identification
           -tp, --test-path <path> - test scenario path
           -tr, --test-repo-root-dir <path> - test repository root directory

     Global Options:
       -c, --config <file> - reads the alternate configuration file
       -d, --debug <level> - debug turned on with specified level > 0
       -e, --debug-channel <channel number, ..> - debug channel filter turned on
       -f, --force - enforces command
       -i, --interactive - turns on interactive mode
       -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
       -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs     
       
Upgrade
=======

Use same procedure as for installation. Use command option --upgrade for pip, easy_install, --force for setup.py.
If configuration file differs from default settings the file is backuped (extension _old) and replaced by default. Adapt the configuration if needed.

Uninstall
=========    

Run command htkuninstall. Use option -y if you want to uninstall also dependent Python modules (for advanced user).                                                         