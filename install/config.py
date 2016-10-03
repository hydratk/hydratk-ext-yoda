# -*- coding: utf-8 -*-

config = {
  'pre_tasks' : [
                 'install_libs_from_repo',
                 'install_pip'
                ],

  'post_tasks' : [
                  'copy_files',
                  'set_access_rights',
                  'install_manpage',
                  'install_db_testdata'
                 ],
          
  'modules' : [    
               'hydratk',     
               'lxml>=3.3.3',  
               'pytz>=2016.6.1',                
               'simplejson>=3.8.2'                                                 
              ],
          
  'files' : {
             'etc/hydratk/conf.d/hydratk-ext-yoda.conf'               : '/etc/hydratk/conf.d',
             'var/local/hydratk/yoda/yoda-tests/test1/example1.yoda'  : '/var/local/hydratk/yoda/yoda-tests/test1',
             'var/local/hydratk/yoda/helpers/yodahelpers/__init__.py' : '/var/local/hydratk/yoda/helpers/yodahelpers',
             'var/local/hydratk/yoda/lib/yodalib/__init__.py'         : '/var/local/hydratk/yoda/lib/yodalib',
             'var/local/hydratk/yoda/db_testdata/db_struct.sql'       : '/var/local/hydratk/yoda/db_testdata',
             'var/local/hydratk/yoda/db_testdata/db_data.sql'         : '/var/local/hydratk/yoda/db_testdata'         
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