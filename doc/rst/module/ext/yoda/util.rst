.. _module_ext_yoda_util:

Utilities
=========

This sections contains module documentation of util modules.

check
^^^^^

Module check provides various methods for data checking in tests. It uses external modules
`lxml <http://lxml.de/>`_ in version >= 3.3.3, `simplejson <https://github.com/simplejson/simplejson>`_ in version >= 3.8.2
and standard module `re <https://docs.python.org/3.6/library/re.html>`_.

lxml requires non-Python libraries which are automatically installed by setup script (python-lxml, libxml2-dev, libxslt1-dev for apt-get, 
python-lxml, libxml2-devel, libxslt-devel for yum). 
Unit tests available at hydratk/extensions/yoda/util/check/01_methods_ut.jedi

* load_json

Method loads JSON string using simplejson method loads.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.check import load_json
     
     doc = '{"store": {"bicycle": {"color": "red", "price": 19.95}}}'
     res = load_json(doc)

* load_xml

Method loads XML string using lxml method fromstring.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.check import load_xml
     
     doc = '<foo><bar>xxx</bar></foo>'
     res = load_xml(doc)

* xpath

Method performs XPATH query document (using method xpath)and returns the output. Document can be lxml.etree or string (will be loaded automatically).

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.check import xpath
     
     # XPATH query
     doc = '<foo><bar at="yyy">xxx</bar></foo>'
     expr = '/foo/bar'
     res = xpath(doc, expr)
     
     # get attribute
     res = xpath(xml, expr, attribute='at') 
     
     # namespaces
     doc = '<a:foo xmlns:a="aaa" xmlns:b="bbb"><b:bar>xxx</b:bar></a:foo>'
     expr = '/a:foo/b:bar'
     res = xpath(doc, expr, ns={'a':'aaa', 'b':'bbb'})     

* regex 

Methods performs regular expression search using re method search and returns the output.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.check import regex
     
     # single match
     data = 'ab c2e*f'
     expr = '^.*(\d).*$'
     res = regex(data, expr)   
     
     # multiple matches
     expr = '^.*([cd]).*(\w)$'
     res = regex(data, expr)  
     
data
^^^^     

Module data provides various methods data generation used in tests.
Unit tests available at hydratk/extensions/yoda/util/data/01_methods_ut.jedi, 02_methods_ut.jedi
Methods by default generate 1 random sample but can generate list using parameter cnt. 

* gen_number

Method generates random number. It uses random method randint.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_number
     
     # 10-digits integer
     res = gen_number()
     
     # float with 5 integer and 3 fractional digits
     res = gen_number(5,3)
     
     # negative number
     res = gen_number(positive=False)
     
* gen_nondec

Method generates random number with non-decadical base (binary, octal, hexadecimal). It uses random method randint, string is formatted according to base.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_nondec
     
     # 10-digits hexadecimal number
     res = gen_nondec(10, 'hex')
     
     # 10-digits binary number
     res = gen_nondec(10, 'bin')
     
* gen_string

Method generates random string of given category. It uses random method choice with string categories (ascii_letters, ascii_lowercase, ascii_uppercase, digits, printable).

  .. code-block:: python
   
     from hydratk.extensions.yoda.util.data import gen_string
     
     # string with alphanumerical characters
     res = gen_string(10, 'alpha')
     
     # string with uppercase characters
     res = gen_string(10, 'upper')
     
* gen_date

Method generates random date using standard modules `time <https://docs.python.org/3.6/library/time.html>`_, `datetime <https://docs.python.org/3.6/library/datetime.html>_` 
and external module `pytz <http://pythonhosted.org/pytz/>`_ in version >= 2016.6.1. 
It supports multiple formats (ISO default, Unix timestamp, strftime). By default it generates current date.

If time interval is provided (parameters start, end) the method generates random date within interval. It calculates delta interval (count of seconds)
and adds random number to start. If parameter current is provided (values year, month, day, hour, minute) it generates date where current part is fixed
and remaining parts are random.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_date
     
     # iso format 
     res = gen_date('iso')
     
     # unix format 
     res = gen_date('unix')
     
     # custom format with timezone
     res = gen_date('%Y-%m-%d %H:%M:%S %z', time_zone='UTC')
     
     # interval
     dform, start, end = '%Y%m%d%H%M%S' '20160925124536', '20161015132800'
     res = gen_date(dform, start=start, end=end)  
     
* gen_ip

Method generates random IP address of version 4 (4 bytes in decadic form, default) or version 6 (8 double bytes in hexadecimal form).

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_ip
     
     res = gen_ip(4)
     
* gen_birth_no

Method generates random birth number (czech format YYMMDD/XXXX) within given age interval (default 18-30). The method calculates random
date within interval and transforms it format YYMMDD (female number contains MM+50, bool parameter male). Then it calculates 3 random digits. Whole number 
is divisible by 11 with no remainder (it determines the last digit). Delimiter / is configurable by bool parameter delimiter.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_birth_no
     
     # male 
     res = gen_birth_no(male=True)
     
     # female with interval and delimiter
     min_age, max_age= 30, 35
        res = gen_birth_no(min_age=min_age, max_age=max_age, male=False, delimiter=True)      
        
* gen_reg_no

Method generates random registration number (czech format XXXXXXXX). It generates 7 random digits. The last digits is calculated
to meet algorithm (weighted sum, divisible by 11).

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_reg_no
     
     res = gen_reg_no()         
     
* gen_tax_no

Method generated random tax number (czech format CZreg_no or CZbirth_no). The type is configurable by parameter src (reg_no, birth_no).

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_tax_no
     
     # from registration number
     res = gen_tax_no(src='reg_no')
     
     # from birth number
     res = gen_tax_no(src='birth_no')           
                       
* gen_account_no

Method generates random bank account number. It supports national czech format (XXXXXX-XXXXXXXXXX/XXXX) and IBAN (CZ20-digits)format.
Bank code, base length and prefix length are configurable (parameters bank, base_len, prefix_len). When bank code is not provided
the method gets random code from database table bank. Base and prefix are calculated to meet algorithm (weighted sum, divisible by 11). 

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_account_no
     
     # national format XXXXXXXXXX/XXXX
     res = gen_account_no(form='nat')                       
     
     # national format with prefix XXXXXX-XXXXXXXXXX/XXXX
     res = gen_account_no(form='nat', prefix=True)
     
     # IBAN format
     res = gen_account_no(form='iban')
     
     # bank code and length
     res = gen_account_no(prefix=True, bank='0100', base_len=6, prefix_len=3)
     
* gen_email

Method generates random email. Domain, subdomain and lengths are configurable (parameters name_len, subdomain, subdomain_len, domain, domain_type).
When domain is not provided the method gets random domain from database table domain (type original or country).

  .. code-block:: python
  
     # random original domain
     res = gen_email(domain=None, domain_type='original')
     
     # lengths
     res = gen_email(name_len=5, subdomain_len=4)
     
* gen_name

Method generates random czech name (firstname and surname) male, female or both. It searches random records in database tables first_name, surname (equal sex).
The output (parameter tuple_out) can be tuple (default) or string.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_name 
     
     # male
     res = gen_name(sex='male')
     
     # both, string output
     res = gen_name(sex='both', tuple_out=False)
     
* gen_phone

Method generates random phone number. It supports national and international format. Country code, destination code and subscriber length are configurable 
(parameters cc, country, nds, sn_len). When cc is not provided the method gets random code from database table cc. When country is provided, it is translated to cc.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_phone
     
     # international format +12-digits
     res = gen_phone(form='int')      
     
     # national format +9-digits
     res = gen_phone(form='nat')
     
     # country code translation
     res = gen_phone(country='Slovakia')
     
* gen_address

Method generates random address. The database contains czech addresses with its hierarchy region -> district -> area -> locality -> part -> street.
By default the method searches random street in table street and then it finds remaining parameters. The initial search point is configurable 
by parameters param (region, district, area, locality, part), value (requested geographical part). The method finds remaining parameters in upper levels (they are fix)
and lower levels (they are random). The output (parameter dict_out) can be dictionary (default) or string.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import gen_address
     
     # random address, full street number (orientation and descriptive number)
     res = gen_address(street_no_full=True)
     
     # given area
     value = 'Jindřichův Hradec'
     res = gen_address(param='area', value=value)
     
     # given region
     value = 'Jihočeský'
     res = gen_address(param='region', value=value)
     
* _get_dsn

Auxiliary method to get database DSN from configuration.

* create_type

Method generates new data type in database table data_type defined parameters (title, description, col_titles).

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import create_type
     
     title, desc, cols = 'test', 'test desc', ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10']
     res = create_type(title, desc, cols)
     
* update_type

Method updates data type in table data_type. 

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import update_type
  
     title_new, desc, cols = 'test 2', 'test desc 2', {1:'x1', 10:'x10'}
     res = update_type(title, title_new, desc, cols)      
     
* delete_type

Method deletes data type in table data_type. By default (parameter del_records) it deletes records in table data which belong to data type.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import delete_type  
     
     res = delete_type(title_new)
     
* read_data

Methods reads data for given data_type from table data. It supports filtering (parameters active, col_filter).
The output is list of dictionary (key - column title from data_type, value - column value from data).

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import read_data
     
     data_type, active, col_filter = title, 1, {1:'x1', 10:'x10'}
     res = read_data(data_type, active, col_filter)
     
* create_data

Method creates data for given data_type in table data.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import create_data
     
     data_type, active, col_values = title, 1, {1:'x1', 2:'x2', 3:'x3', 4:'x4', 5:'x5', 6:'x6', 7:'x7', 8:'x8', 9:'x9',10:'x10'}
     res = create_data(data_type, active, col_values)
     
* update_data

Method updates data for given data_type in table data.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import update_data
     
     data_type, active, col_filter, col_values = title, 0, {1:'x1', 10:'x10'}, {1:'xx1', 10:'xx10'}
     res = update_data(data_type, active, col_filter, col_values)
     
* delete_data

Method deletes data for given data_type in table data.

  .. code-block:: python
  
     from hydratk.extensions.yoda.util.data import delete_data
     
     data_type, active, col_filter = title, 0, {1:'xx1', 10:'xx10'}
     res = delete_data(data_type, active, col_filter)          

Database tables
^^^^^^^^^^^^^^^

**bank**:

List of bank codes

======  ======== ======== ===========
Column  Datatype Nullable Constraint 
======  ======== ======== ===========
code    varchar     N     primary key
title   varchar     Y
swift   varchar     Y     
======  ======== ======== ===========            

**domain**:

List of email domains

======  ======== ======== ===========
Column  Datatype Nullable Constraint 
======  ======== ======== ===========
code    varchar     N     primary key
title   varchar     Y
type    varchar     N     
======  ======== ======== ===========    

**first_name**:

List of first names

======  ======== ======== ===========
Column  Datatype Nullable Constraint 
======  ======== ======== ===========
name    varchar     N     primary key
sex     varchar     N
======  ======== ======== ===========   

**surname**:

List of surnames

======  ======== ======== ===========
Column  Datatype Nullable Constraint 
======  ======== ======== ===========
name    varchar     N     primary key
sex     varchar     N     
======  ======== ======== ===========   

**cc**:

List of country codes

======  ======== ======== ===========
Column  Datatype Nullable Constraint 
======  ======== ======== ===========
code    integer     N     primary key
title   varchar     Y
======  ======== ======== ===========  

**region**:

List of regions (czech Kraj)

======  ======== ======== ===========
Column  Datatype Nullable Constraint 
======  ======== ======== ===========
code    varchar     N     primary key
title   varchar     N
======  ======== ======== ===========     

**district**:

List of districts (czech Okres)

======  ======== ======== ==========================
Column  Datatype Nullable Constraint 
======  ======== ======== ==========================
code    varchar     N     primary key
title   varchar     N
region  integer     N     foreign key to region.code
======  ======== ======== ==========================   

**area**:

List of areas (czech Oblast)

========  ======== ======== ============================
Column    Datatype Nullable Constraint 
========  ======== ======== ============================
code      varchar     N     primary key
title     varchar     N
district  integer     N     foreign key to district.code
========  ======== ======== ============================   

**locality**:

List of localities (czech Obec)

======  ======== ======== ========================
Column  Datatype Nullable Constraint 
======  ======== ======== ========================
code    varchar     N     primary key
title   varchar     N
area    integer     N     foreign key to area.code
======  ======== ======== ========================                                 

**part**:

List of parts (czech Cast obce)

========  ======== ======== ============================
Column    Datatype Nullable Constraint 
========  ======== ======== ============================
code      varchar     N     primary key
title     varchar     N
zip       integer     N
locality  integer     N     foreign key to locality.code
========  ======== ======== ============================ 

**street**:

List of streets (czech ulice)

======  ======== ======== ========================
Column  Datatype Nullable Constraint 
======  ======== ======== ========================
code    varchar     N     primary key
title   varchar     N
part    integer     N     foreign key to part.code
======  ======== ======== ======================== 

**data_type**:

Custom data types (empty after installation)

===========  ======== ======== =========================
Column       Datatype Nullable Constraint 
===========  ======== ======== =========================
id           integer     N     primary key autoincrement
title        varchar     N     unique
description  varchar     Y     
col1_title   varchar     Y
col2_title   varchar     Y
col3_title   varchar     Y
col4_title   varchar     Y
col5_title   varchar     Y
col6_title   varchar     Y
col7_title   varchar     Y
col8_title   varchar     Y
col9_title   varchar     Y
col10_title  varchar     Y
===========  ======== ======== ========================= 

**data**:

Custom data records (empty after installation)

===========  ======== ======== ===========================
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========================
id           integer     N     primary key autoincrement
type         integer     N     foreign key to data_type.id
active       integer     Y     
col1         varchar     Y
col2         varchar     Y
col3         varchar     Y
col4         varchar     Y
col5         varchar     Y
col6         varchar     Y
col7         varchar     Y
col8         varchar     Y
col9         varchar     Y
col10        varchar     Y
===========  ======== ======== ===========================