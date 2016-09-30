.. _tutor_yoda_tut8_util:

Tutorial 8: Utilities
==============================

This section will show you how to use utilities.
It is intended to use them in Yoda tests and helpers.

Data check
^^^^^^^^^^

Module check provides utilities for JSON, XML and regular expressions.

  .. code-block:: python
  
     # import library
     import hydratk.extensions.yoda.util.check as chk
     
     # load JSON
     # check element via dictionary traversal
     json = '{"store": {"bicycle": {"color": "red", "price": 19.95}}}'
     doc = chk.load_json(json)
     assert (doc['store']['bicycle']['color'] == 'red')
     
     # load XML
     # check element via XPATH
     xml = '<foo><bar at="yyy">xxx</bar></foo>'
     doc = chk.load_xml(xml)
     
     # element text
     expr = '/foo/bar'
     assert (chk.xpath(doc, expr) == 'xxx')
     
     # element attribute     
     assert (chk.xpath(doc, expr, attribute='at') == 'yyy')
     
     # filter
     expr = '/foo/bar[@at="yyy"]'
     assert (chk.xpath(doc, expr) == 'xxx')
     
     # namespaces
     doc = '<a:foo xmlns:a="aaa" xmlns:b="bbb"><b:bar>xxx</b:bar></a:foo>'
     expr = '/a:foo/b:bar'
     assert (chk.xpath(doc, expr, ns={'a':'aaa', 'b':'bbb'}) == 'xxx')    
     
     # regex with single match
     data = 'ab c2e*f'
     expr = '^.*(\d).*$'
     assert (chk.regex(data, expr) == '2') 
     
     # regex with multiple matches
     expr = '^.*([cd]).*(\w)$'
     assert (chk.regex(data, expr) == ('c', 'f'))   
     
Data generation
^^^^^^^^^^^^^^^    

Module data provides utilities for random data generation.
 
To generate valid data Yoda contains own test data database (default installation path /var/local/yoda/db_testdata/testdata.db3)
Database can be manually installed via command yoda create-testdata-db or reinstalled via yoda --force create-testdata-db

Each method generates one random sample by default, but can generated list of samples using parameter cnt.  

  .. code-block:: python
  
     # import library
     import hydratk.extensions.yoda.util.data as d
     
     # generate number
     # gen_number(n_int=10, n_frac=0, positive=True, cnt=1)
     gen_number()                           # 10-digit integer
     gen_number(5,3)                        # number with 5 integer a 3 fractional digits
     gen_number(positive=False)             # negative number
     
     # generate number with non-decadic base
     # gen_nondec(n=10, base='hex', cnt=1)
     gen_nondec(10, 'bin')                  # 10-digit binary number
     gen_nondec(10, 'oct')                  # 10-digit octal number
     gen_nondec(10, 'hex')                  # 10-digit hexadecimal number
     
     # generate string
     # gen_string(n=10, category='alpha', cnt=1)
     gen_string(10, 'alpha')                # 10-char string with alpha characters
     gen_string(10, 'lower')                # 10-char string with lowercase characters
     gen_string(10, 'upper')                # 10-char string with uppercase characters
     gen_string(10, 'numeric')              # 10-char string with numeric characters
     gen_string(10, 'alphanumeric')         # 10-char string with alphanumeric characters
     gen_string(10, 'special')              # 10-char string with special characters (inc. alphanumeric)
     
     # generate date
     # gen_date(date_format='iso', start=None, end=None, current=None, time_zone=None, cnt=1)
     gen_date('iso')                        # datetime with ISO format YYYY-MM-DDThh:mm:ss.micro
     gen_date('unix')                       # datetime with Unix timestamp format
     gen_date('%Y-%m-%d')                   # date wich given format YYYY-MM-DD
     gen_date('%Y-%m-%d %H:%M:%S')          # datetime with given format YYYY-MM-DD hh:mm:ss
     gen_date('iso', time_zone='UTC')       # datetime with timezone ISO+00:00
     gen_date('%Y-%m-%d %H:%M:%S %z', time_zone='UTC')  # datetime with given format inc. timezone
     gen_date(current='year')               # datetime within current year, supported options year|month|day|hour|minute      
     gen_date('%Y%m%d%h%M%S', start='20160925124536', end='20161015132800')  # datetime within given interval
     
     # generate IP address
     # gen_ip(version=4, cnt=1)
     gen_ip(4)                              # IPv4 format
     gen_ip(6)                              # IPv6 format
     
     # generate birth number
     # gen_birth_no(min_age=18, max_age=30, male=True, delimiter=False, cnt=1)
     gen_birth_no(male=True)                # male birth number YYMMDDXXXX
     gen_birth_no(male=False)               # female birth number (MM+50)
     gen_birth_no(delimiter=True)           # birth number with delimiter YYMMDD/XXXX
     gen_birth_no(min_age=30, max_age=35)   # birth number within given interval
     
     # generate registration number
     # gen_reg_no(cnt=1)
     gen_reg_no()                           # registration number XXXXXXXX
     
     # generate tax number
     # gen_tax_no(prefix='CZ', src='reg_no', cnt=1)
     gen_tax_no(src='birth_no')             # tax number from birth number (for entrepreneur) CZXXXXXXXXXX
     gen_tax_no(src='reg_no')               # tax number from registration number (for company) CZXXXXXX
     
     # generate account number     
     # gen_account_no(form='nat', country='CZ', prefix=False, bank=None, base_len=10, prefix_len=6, cnt=1)
     # bank code is generated from db table bank
     gen_account_no(form='nat')             # national format XXXXXXXXXX/YYYY
     gen_account_no(form='nat', prefix=True) # national format inc. prefix ZZZZZZ-XXXXXXXXXX/YYYY
     gen_account_no(form='iban')            # IBAN format CZYYYYZZZZZZXXXXXXXXXX
     gen_account_no(prefix=True, base_len=6, prefix_len=3) # account with given length ZZZ-XXXXXX/YYYY
     gen_account_no(bank='0100')            # given bank code XXXXXXXXXX/0100
     
     # generate email
     # gen_email(name_len=8, subdomain=None, subdomain_len=6, domain='.com', domain_type='original', cnt=1)
     # domain is generated from db table domain
     gen_email(domain=None, domain_type='original') # original domain (i.e. .com,.edu)
     gen_email(domain=None, domain_type='country') # country domain (i.e. .cz,.de)
     gen_email(domain='.com')               # given domain XXXXXXXX@YYYY.com
     gen_email(subdomain='test')            # given subdomain XXXXXXXX@test.com
     gen_email(name_len=5, subdomain_len=4) # given length XXXXX@YYYY.com
     
     # generate name
     # gen_name(sex='both', tuple_out=True, cnt=1)
     # first_name, surname is generated from db tables, first_name, surname
     gen_name(sex='male')                   # male name tuple, output (first_name, surname)
     gen_name(sex='female')                 # female name
     gen_name(sex='both')                   # male or female name
     gen_name(tuple_out=False)              # string output 'first_name surname'
     
     # generate phone
     # gen_phone(form='int', cc=420, country=None, ndc=601, sn_len=6, cnt=1)
     # country code is generated from db table cc
     gen_phone(form='int')                  # international format +420601XXXXXX
     gen_phone(form='nat')                  # national format 601XXXXXX
     gen_phone(cc='421')                    # given country code +421601XXXXXX
     gen_phone(cc=None)                     # random country code
     gen_phone(country='Slovakia')          # given country, country code read from table cc
     gen_phone(ndc='602')                   # given national destination code +420602XXXXXX
     gen_phone(sn_len=5)                    # given subcriber number length +420601XXXXX
     
     # generate address
     # gen_address(param=None, value=None, street_no_full=True, dict_out=True, cnt=1)
     # address parameters are generated from db tables region, district, are, locality, part, street
     gen_address(street_no_full=True)                     # {'street': 'Sasovské Údolí', 'zip': 58601, 'district': 'Jihlava', 'locality': 'Jihlava', 
                                                             'region': 'Vysočina', 'area': 'Jihlava', 'street_no': '5391/64', 'part': 'Jihlava'}
     gen_address(street_no_full=False)                    # {'street': 'Padělky', 'zip': 78344, 'district': 'Olomouc', 'locality': 'Náměšť na Hané', 
                                                             'region': 'Olomoucký', 'area': 'Olomouc', 'street_no': '10', 'part': 'Náměšť na Hané'}
     gen_address(dict_out=False)                          # string output, F. Čejky 6011/85, Místek, 73801
     gen_address(param='part', value='Kunžak')            # {'street': 'Ke Kostelu', 'zip': 37862, 'district': 'Jindřichův Hradec', 'locality': 'Kunžak', 
                                                             'region': 'Jihočeský', 'area': 'Jindřichův Hradec', 'street_no': '9156/99', 'part': 'Kunžak'}
     gen_address(param='locality', value='Kunžak')        # {'street': 'B. Němcové', 'zip': 37853, 'district': 'Jindřichův Hradec', 'locality': 'Kunžak', 
                                                             'region': 'Jihočeský', 'area': 'Jindřichův Hradec', 'street_no': '9954/45', 'part': 'Terezín'}
     gen_address(param='area', value='Jindřichův Hradec') # {'street': 'Rybničná', 'zip': 37833, 'district': 'Jindřichův Hradec', 'locality': 'Nová Bystřice', 
                                                             'region': 'Jihočeský', 'area': 'Jindřichův Hradec', 'street_no': '9176/6', 'part': 'Nová Bystřice'}
     gen_address(param='district', value='Písek')         # {'street': 'K Libří', 'zip': 25230, 'district': 'Písek', 'locality': 'Lety', 
                                                             'region': 'Jihočeský', 'area': 'Písek', 'street_no': '4609/57', 'part': 'Lety'}
     gen_address(param='region', value='Jihočeský')       # {'street': 'U Studánky', 'zip': 38101, 'district': 'Český Krumlov', 'locality': 'V\xc4\x9bt\xc5\x99n\xc3\xad', 
                                                             'region': 'Jihočeský', 'area': 'Český Krumlov', 'street_no': '1052/61', 'part': 'N\xc4\x9bm\xc4\x8de'}
                                                             
Data storage
^^^^^^^^^^^^

Module data provides database storage for own data. 
Database contains two tables

* data_type - used to define own data type, data can have 10 parameters (columns) with own titles
* data - used to store own data of given type, data has up 10 parameters and active flag (1-active, 0-deactive)     

  .. code-block:: python
  
     # import library
     import hydratk.extensions.yoda.util.data as d
     
     # create data type 
     # update_type(title, title_new=None, description=None, col_titles_new={}
     title, desc, cols = 'test', 'test desc', ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10']
     create_type(title, desc, cols)                       # title for all columns                                      
     
     # update data type
     # update_type(title, title_new=None, description=None, col_titles_new={}
     title_new, desc, cols = 'test 2', 'test desc 2', {1:'x1', 10:'x10'}  
     update_type(title, title_new, desc, cols)            # update column 1,10 titles
     
     # delete data type
     # delete_type(title, del_records=True)
     delete_type(title_new)                               # delete inc. data records
     delete_type(title_new, del_records=False)            # keep records in table data  
     
     # create data
     # create_data(data_type, active=1, col_values={})
     data_type, active, col_values = title, 1, {1:'x1', 2:'x2', 3:'x3', 4:'x4', 5:'x5', 6:'x6', 7:'x7', 8:'x8', 9:'x9', 10:'x10'}
     create_data(data_type, active, col_values)           # fill all columns
     
     # read data
     # read_data(data_type, active=1, col_filter={})
     # returns dict with column titles according to table data_type
     data_type, active, col_filter = title, 1, {1:'x1', 10:'x10'}
     read_data(data_type, active, col_filter)             # read records where column 1,10 values are x1,x10
                                                          # {'type':data_type, 'active':active, 't1':'x1', 't2':'x2', 't3':'x3', 't4':'x4', 
                                                             't5':'x5', 't6':'x6', 't7':'x7', 't8':'x8', 't9':'x9', 't10':'x10'}
     
     # update data
     # update_data(data_type, active=None, col_filter={}, col_values_new={})
     data_type, active, col_filter, col_values = title, 0, {1:'x1', 10:'x10'}, {1:'xx1', 10:'xx10'}
     update_data(data_type, active, col_filter, col_values) # update columns 1,10 where column 1,10 values are x1,x10
     
     # delete data
     # delete_data(data_type, active=0, col_filter={})    
     data_type, active, col_filter = title, 0, {1:'xx1', 10:'xx10'}
     delete_data(data_type, active, col_filter)           # delete records where column 1,10 values are xx1,xx10 