.. _tutor_yoda_tut4_hlp_lib:

Tutorial 4: Helpers and libraries
=================================

This section will show you the concept of helpers and libraries.

Concept
^^^^^^^

Sample test script implemented in previous tutorials is very simple.
Real automated tests require advanced coding. 
Basic programming principle is to decompose complex code the simpler tasks.

Yoda extension recommends decomposition to 3 levels.

* scripts: Embedded code with basic complexity and usage of helpers. 
* helpers: High level coding with usage of libraries
* libraries: Low level coding

  .. note:: 
  
     Each level has its own directory: yoda-tests, helpers, lib.

We will show the concept on example used on real project.

Library
^^^^^^^

Libraries provides low level methods and classes. 
In our example they access tested application using HydraTK network library.

This library implements interface to Oracle database.
Provides methods to connect, disconnect and read customer entity.

Modules are located in test_repo_root/lib/yodalib by default.

.. code-block:: python

   from hydratk.lib.network.dbi.client import DBClient
   from yodalib.config import params as config
   from yodalib.ba.entities import Customer

   class DB_INT:
    
       _client = None
    
       def __init__(self):
        
          self._client = DBClient('ORACLE')

       def connect(self):         
               
           cfg = config['ba']
           result = self._client.connect(cfg['db_host'], cfg['db_port'], cfg['db_sid'],
                                         config['common']['user'], cfg['db_passw'])
        
           return result

       def disconnect(self):
    
           result = self._client.disconnect()
           return result

       def read_customer(self, cu_ref_no):        

           query = """
                   SELECT a.customer_ref_no, a.account_id, a.status as action_customer, a.document_id, a.document_type, a.segment, a.sfa_id, 
                   a.type, b.status as action_subject, b.first_name, b.surname, to_char(b.birth_date, \'YYYY-MM-DD\') as birth_date, 
                   b.birth_number, b.registration_number, b.tax_number, b.company_name, c.status as action_address, c.street, 
                   c.orientation_number, c.street_number, c.city, c.district, c.zip_code, c.country 
                   FROM ba.customer a, ba.subject b, ba.customer_address c 
                   WHERE a.customer_ref_no = ? AND a.technical_status <> \'H\' 
                   AND a.account_id = b.account_id (+) AND nvl(b.technical_status, \'X\') <> \'H\' 
                   AND a.account_id = c.account_id (+) AND c.technical_status <> \'H\'
                   """
                    
           result, row = self._client.exec_query(query, [cu_ref_no], fetch_one=True)
            
           if (not result or len(row) == 0):
               return None            
                    
           customer_info = CustomerInfo(row['document_id'], row['document_type'], row['segment'],  
                                        row['type'], row['action_customer'], row['sfa_id'])           
           subject = Subject(row['action_subject'], row['first_name'], row['surname'], row['birth_date'],
                             row['birth_number'], row['registration_number'], row['tax_number'], row['company_name'])             
           address = Address(row['street'], row['street_number'], row['city'], row['zip_code'], row['country'], 
                             row['action_address'], row['orientation_number'], row['district'])   
           customer = Customer(row['customer_ref_no'], row['account_id'], customer_info, subject, address) 
                             
           return customer
           
This library implements interface to Weblogic JMS queue.
Provides methods to connect, disconnect and create customer entity.            
           
  .. code-block:: python
  
     from hydratk.lib.network.jms.client import JMSClient
     from hydratk.lib.array.operation import subdict
     from yodalib.config import params as config
     from lxml.etree import Element, SubElement, tostring 

     class JMS_INT:
    
        _client = None
        nsmap = None
        ns = None
        destination = None
        jms_type = None
    
        def __init__(self): 
        
            self._client = JMSClient(); 
        
            self.nsmap = {
                          'int'  : 'http://o2.cz/cip/svc/IntegrationMessage-3.0',
                          'ba_cm': 'http://o2.cz/systems/billing/BA-GF/BA-GF_BillingCustomerManagement/2.0',
                          'ba_pm': 'http://o2.cz/systems/billing/BA-GF/BA-GF_BillingProductManagement/1.0'                      
                         }
            self.ns = {
                       'int'  : '{%s}' % self.nsmap['int'], 
                       'ba_cm': '{%s}' % self.nsmap['ba_cm'],
                       'ba_pm': '{%s}' % self.nsmap['ba_pm']
                      }
        
            self.destination = 'cipesb/gf/cip2ba/queue/request'
            self.jms_type = {
                             'manageCustomer'       : 'BA-GF.BillingCustomerManagement-2.0.manageCustomer.Request',
                             'manageCustomerAccount': 'BA-GF.BillingCustomerManagement-2.0.manageCustomerAccount.Request',
                             'manageProduct'        : 'BA-GF.BillingProductManagement-1.0.manageProduct.Request'    
                            } 
        
        def connect(self):         
             
            cfg = config['esb']                 
            properties = {'initial_context_factory': cfg['initial_context_factory'],
                          'provider_url': cfg['provider_url']}
            result = self._client.connect(cfg['connection_factory'], properties) 
               
            return result

        def disconnect(self):
 
            result = self._client.disconnect()
            return result              
        
        def manage_customer(self, header, cu_ref_no, customer_info=None, subject=None, address=None, 
                            operator='O2_CZ', action='activate'):
                        
            ns = self.ns['ba_cm']
            root = Element(ns+'ManageCustomerRequest', nsmap=subdict(self.nsmap, {'int', 'ba_cm'}))
            root.append(header.toxml(self.ns['int']))    
        
            body = SubElement(root, ns+'requestBody')
            SubElement(body, ns+'cuRefNo').text = cu_ref_no
            SubElement(body, ns+'operator').text = operator
            SubElement(body, ns+'action').text = action 
            if (customer_info != None):
                body.append(customer_info.toxml(ns))
            if (subject != None):
                body.append(subject.toxml(ns))
            if (address != None):
                body.append(address.toxml(ns)) 
            
            message = tostring(root, xml_declaration=True, encoding='UTF-8')
            headers = {'JMSType': self.jms_type['manageCustomer'], 'JMSCorrelationID': header.correlation_id}
            result = self._client.send(self.destination, message, headers=headers) 
            return result                

Helper
^^^^^^               

Helpers provides high level methods. 
In our example they use library methods, provide simpler interface and debug messages, prepare data.

This helper prepares customer entity (entity classes are simple, so they are not shown in example).

Modules are located in test_repo_root/helpers/yodahelpers by default.

  .. code-block:: python
  
     from hydratk.lib.data.randgen import gen_id
     from yodalib.ba.entities import Customer

     def customer_complex():     
    
         cu_ref_no = gen_id()
         customer_info = CustomerInfo(document_id='1426', document_type='ID_CARD', segment='R', sfa_id=cu_ref_no, type='Person')
         subject = Subject(first_name='Charlie', surname='Bowman', birth_date='1970-01-01', birth_num='7001010001',
                           registration_number='1234', tax_number='2345', company_name='Bowman')
         address = Address(street_name='Tomickova', orientation_num='2144', street_num='1', city='Praha', district='Chodov',
                           zip_code='14800', country='CZE') 
    
         customer = Customer(cu_ref_no=cu_ref_no, customer_info=customer_info, subject=subject, address=address)
         return customer


This helper provides simpler interface to library methods. 

  .. code-block:: python
  
     from yodalib.ba.db_int import DB_INT
     from yodalib.ba.jms_int import JMS_INT
     from yodalib.utils.interface import wait, gen_header  
  
     db = DB_INT()
     jms = JMS_INT()

     def db_connect():

         print 'Connecting to DB'
         return db.connect()
    
     def db_disconnect():

         print 'Disconnecting from DB'
         return db.disconnect()
    
     def jms_connect():
    
         print 'Connecting to JMS'
         return jms.connect()
    
     def jms_disconnect():

         print 'Disconnecting from JMS'
         return jms.disconnect()
    
     def connect():
     
         res_db = db_connect()        
         res_jms = jms_connect()    
         return res_db and res_jms
    
     def disconnect():
     
         res_db = db_disconnect()    
         res_jms = jms_disconnect()    
         return res_db and res_jms
         
     def read_customer(cu_ref_no):   
    
         print 'Reading customer: {0}'.format(cu_ref_no)
         customer = db.read_customer(cu_ref_no)
         return customer
    
     def manage_customer(customer, action='activate'):  
        
         header = gen_header('ESB', 'BA')
         print 'Sending message manageCustomer: {0}'.format(header.correlation_id)
         res = jms.manage_customer(header, customer.cu_ref_no, customer.customer_info, 
                                   customer.subject, customer.address, action=action)
    
         wait()
         return res, header.correlation_id  
       
Script
^^^^^^

Scripts use helper methods, the embedded code is simple. The complexity is hidden in used methods.

This script prepares customer entity, sends it as JMS message and reads created customer from database.

  .. code-block:: yaml
  
     Test-Scenario-1:
       id: ts_01
       path: SOC/SYS/BA/manageCustomer/manageCustomer_complex.jedi
       name: manageCustomer_complex
       desc: Create customer with complex configuration
       author: Petr Rasek <bowman@hydratk.org>
       version: 1.0
  
       pre-req: |
         import yodahelpers.o2.soc.ba.entities as ent 
         import yodahelpers.o2.soc.ba.interface as int    
    
         this.test_result = int.connect()
         assert (this.test_result == True)
    
       Test-Case-1:
         id: tc_01
         name: create_customer_complex
         desc: Create complex customer
  
         Test-Condition-1: 
           id: tco_01
           name: send_msg
           desc: Send message manageCustomer
           
           test: |
             customer = ent.customer_complex()
             cu_ref_no = customer.cu_ref_no
             this.test_result, corr_id = int.manage_customer(customer) 
                         
           validate: |   
             assert (this.test_result == True)        
        
         Test-Condition-2:
           id: tco_02
           name: read_customer
           desc: Read created customer
           
           test: |
             cu = int.read_customer(cu_ref_no)
             this.test_result = (cu != None)
        
           validate: |    
             assert (this.test_result == True)
             print cu                                
    
      post-req: |
        this.test_result = int.disconnect()
        assert (this.test_result == True) 
        
This example shows new tags:

* pre-req: pre-requirements executed before first test case. 
* post-req: post-requirements executed after last test case.

The purpose of pre-requirements is to import helpers, load data, initialize clients, connections etc.
The purpose of post-requirements is to clean data, close clients, connections etc.                     