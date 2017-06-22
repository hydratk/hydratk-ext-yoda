# -*- coding: utf-8 -*-
"""Module for random data generation

.. module:: yoda.util.data
   :platform: Unix
   :synopsis: Module for data generation
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.database.dbo.dbo import DBO
import hydratk.lib.system.config as syscfg
from random import randint, choice
from string import digits, ascii_lowercase, ascii_uppercase, ascii_letters, printable
from time import mktime
from datetime import datetime, timedelta
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from sqlite3 import Error
from sys import version_info


def gen_number(n_int=10, n_frac=0, positive=True, cnt=1):
    """Method generates random number

    Args:
       n_int (int): digits for integer part
       n_frac (int): digits for fractional part
       positive (bool): generate positive number
       cnt (int): count of generated samples

    Returns:
       obj: int, float or list 

    Raises:
       error: ValueError

    """

    if (n_int < 0 or n_frac < 0):
        raise ValueError('digits must be positive integer')

    recs = [None] * cnt
    for i in range(0, cnt):
        number = 0
        if (n_int > 0):
            number = randint(10**(n_int - 1), 10**n_int - 1)
        if (n_frac > 0):
            number += 10**(-1 * n_frac) * \
                randint(10**(n_frac - 1), 10**n_frac - 1)
        if (not positive):
            number = -1 * number
        recs[i] = number

    return recs if (cnt > 1) else recs[0]


def gen_nondec(n=10, base='hex', cnt=1):
    """Method generates random number with non-decadical base

    Args:
       n (int): digits
       base (str): numeric base bin|oct|hex
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (n < 0):
        raise ValueError('digits must be positive integer')
    if (base not in ['bin', 'oct', 'hex']):
        raise ValueError('base must bin|oct|hex')

    if (base == 'bin'):
        base = (2, 'b')
    elif (base == 'oct'):
        base = (8, 'o')
    elif (base == 'hex'):
        base = (16, 'x')

    recs = [None] * cnt
    for i in range(0, cnt):
        recs[i] = format(randint(base[0]**(n - 1), base[0]**n - 1), base[1])

    return recs if (cnt > 1) else recs[0]


def gen_string(n=10, category='alpha', cnt=1):
    """Method generates random string

    Args:
       n (int): characters
       category (str): category alpha|lower|upper|numeric|alphanumeric|special
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (n < 0):
        raise ValueError('character must be positive integer')
    if (category not in ['alpha', 'lower', 'upper', 'numeric', 'alphanumeric', 'special']):
        raise ValueError(
            'category must be alpha|lower|upper|numeric|alphanumeric|special')

    if (category == 'alpha'):
        category = ascii_letters
    elif (category == 'lower'):
        category = ascii_lowercase
    elif (category == 'upper'):
        category = ascii_uppercase
    elif (category == 'numeric'):
        category = digits
    elif (category == 'alphanumeric'):
        category = ascii_letters + digits
    elif (category == 'special'):
        category = printable

    recs = [None] * cnt
    for i in range(0, cnt):
        s = ''
        for j in range(0, n):
            s += choice(category)
        recs[i] = s

    return recs if (cnt > 1) else recs[0]


def gen_date(date_format='iso', start=None, end=None, current=None, time_zone=None, cnt=1):
    """Method generates random date or datetime

    Current datetime is generated by default    
    When only start or end of interval is provided, second part is set to current datetime

    Args:
       date_format (str): format iso|unix or any format supported by strftime
       start (str): start date with date_format supported by strftime                    
       end (str): end date with date_format suported by strftime
       current (str): current year|month|day|hour|minute
       time_zone (str): time zone, see pytz documentation for info
       cnt (int): count of generated samples

    Returns:
       obj: int (unix format), str (other formats) or list

    Raises:
       error: ValueError

    """

    try:
        time_zone = timezone(time_zone) if (time_zone != None) else None
    except UnknownTimeZoneError as ex:
        raise ValueError(ex)

    recs = [None] * cnt
    if (start != None or end != None):
        start = datetime.strptime(start, date_format) if (
            start != None) else datetime.now(time_zone)
        end = datetime.strptime(end, date_format) if (
            end != None) else datetime.now(time_zone)
        if (end < start):
            raise ValueError('Invalid interval end < start')
        if (version_info[0] == 2 and version_info[1] == 6):
            td = end - start
            delta = int(
                (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6)
        else:
            delta = int((end - start).total_seconds())

        for i in range(0, cnt):
            recs[i] = start + timedelta(seconds=randint(0, delta))

    elif (current != None):
        if (current not in ['year', 'month', 'day', 'hour', 'minute']):
            raise ValueError('current must be year|month|day|hour|minute')
        else:
            dt = datetime.now()
            year, month, day, hour, minute = dt.year, dt.month, dt.day, dt.hour, dt.minute

            for i in range(0, cnt):
                second = randint(0, 59)
                if (current != 'minute'):
                    minute = randint(0, 59)
                    if (current != 'hour'):
                        hour = randint(0, 23)
                        if (current != 'day'):
                            if (month == 2):
                                day = randint(1, 28)
                            elif (month in [4, 6, 9, 11]):
                                day = randint(1, 30)
                            else:
                                day = randint(1, 31)

                            if (current != 'month'):
                                if (day < 29):
                                    month = randint(1, 12)
                                elif (day == 30):
                                    month = [4, 6, 9, 11][randint(0, 3)]
                                else:
                                    month = [1, 3, 5, 7, 8, 10, 12][
                                        randint(0, 6)]

                recs[i] = datetime(
                    year, month, day, hour, minute, second, tzinfo=time_zone)

    else:
        for i in range(0, cnt):
            recs[i] = datetime.now(time_zone)

    for i in range(0, cnt):
        if (date_format == 'iso'):
            recs[i] = recs[i].isoformat()
        elif (date_format == 'unix'):
            recs[i] = int(mktime(recs[i].timetuple()))
        else:
            recs[i] = recs[i].strftime(date_format)

    return recs if (cnt > 1) else recs[0]


def gen_ip(version=4, cnt=1):
    """Method generates random IP address

    Args:
       version (int): protocol version 4|6
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (version not in [4, 6]):
        raise ValueError('version must be 4, 6')

    recs = [None] * cnt
    if (version == 4):
        for i in range(0, cnt):
            ip = [0, 0, 0, 0]
            for j in range(0, 4):
                ip[j] = str(randint(0, 255))
            recs[i] = '.'.join(ip)
    else:
        for i in range(0, cnt):
            ip = [0, 0, 0, 0, 0, 0, 0, 0]
            for j in range(0, 8):
                ip[j] = format(randint(0, 65535), 'x')
            recs[i] = ':'.join(ip)

    return recs if (cnt > 1) else recs[0]


def gen_birth_no(min_age=18, max_age=30, male=True, delimiter=False, cnt=1):
    """Method generates random birth number

    Czech format YYMMDDZZZC

    Args:
       min_age (int): minimum age
       max_age (int): maximum age
       male (bool): generate male birth number, otherwise female
       delimiter (bool): include delimiter /
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (max_age < min_age):
        raise ValueError('Invalid interval max_age < min_age')

    start = datetime.now() - timedelta(days=max_age * 365)
    delta = (max_age - min_age) * 365

    recs = [None] * cnt
    for i in range(0, cnt):
        dt = datetime.strftime(
            start + timedelta(days=randint(0, delta)), '%Y%m%d')
        bn = dt[2:] + choice(digits) + choice(digits) + choice(digits)
        if (not male):
            bn = bn[:2] + str(int(bn[2]) + 5) + bn[3:]

        rem = int(bn) % 11
        bn += '0' if (rem in [0, 10]) else str(rem)
        recs[i] = bn if (not delimiter) else bn[:6] + '/' + bn[6:]

    return recs if (cnt > 1) else recs[0]


def gen_reg_no(cnt=1):
    """Method generates random registration number

    Czech format XXXXXXXX

    Args:
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    """

    recs = [None] * cnt
    for i in range(0, cnt):
        n = [randint(0, 9), randint(0, 9), randint(0, 9), randint(
            0, 9), randint(0, 9), randint(0, 9), randint(0, 9), 0]
        rem = (n[0] * 8 + n[1] * 7 + n[2] * 6 + n[3]
               * 5 + n[4] * 4 + n[5] * 3 + n[6] * 2) % 11
        n[7] = (11 - rem) % 10
        recs[i] = ''.join(map(str, n))

    return recs if (cnt > 1) else recs[0]


def gen_tax_no(prefix='CZ', src='reg_no', cnt=1):
    """Method generates random tax number

    Czech format CZreg_no or CZbirth_no 

    Args:
       prefix (str): prefix
       src (str): source reg_no|birth_no
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (src not in ['reg_no', 'birth_no']):
        raise ValueError('src must be in reg_no|birth_no')

    recs = [None] * cnt
    src = gen_reg_no if (src == 'reg_no') else gen_birth_no
    for i in range(0, cnt):
        recs[i] = prefix + src()

    return recs if (cnt > 1) else recs[0]


def gen_account_no(form='nat', country='CZ', prefix=False, bank=None, base_len=10, prefix_len=6, cnt=1):
    """Method generates random account number    

    Args:
       form (str): account format national|iban
       country (str): country code used in IBAN
       prefix (bool): generate account prefix
       bank (str): bank code, generated from db table bank if empty
       base_len (int): length of base part, max 10
       prefix_len (int): length of prefix part, max 6
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (form not in ['nat', 'iban']):
        raise ValueError('form must be in nat|iban')
    if (base_len < 2 or base_len > 10):
        raise ValueError('base_len must be in <2,10>')
    if (prefix_len < 2 or prefix_len > 6):
        raise ValueError('prefix_len must be in <2,6>')

    if (bank == None):
        db = DBO(_get_dsn())._dbo_driver
        query = 'SELECT code FROM bank LIMIT {0} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM bank)'.format(
            cnt if (cnt < 100) else 100)
        banks = db.execute(query).fetchall()
        bank_len = len(banks)

    recs = [None] * cnt
    for i in range(0, cnt):
        base = [0] * 10
        for j in range(10 - base_len, 9):
            base[j] = randint(0, 9)
        rem = (base[0] * 6 + base[1] * 3 + base[2] * 7 + base[3] * 9 + base[4]
               * 10 + base[5] * 5 + base[6] * 8 + base[7] * 4 + base[8] * 2) % 11
        base[9] = (11 - rem) % 10 if (rem > 0) else 0

        if (prefix):
            pref = [0] * 6
            for j in range(6 - prefix_len, 5):
                pref[j] = randint(0, 9)
            rem = (pref[0] * 10 + pref[1] * 5 + pref[2]
                   * 8 + pref[3] * 4 + pref[4] * 2) % 11
            pref[5] = (11 - rem) % 10 if (rem > 0) else 0

        bank_code = bank if (bank != None) else str(
            banks[randint(0, bank_len - 1)][0])
        if (form == 'nat'):
            recs[i] = ''.join(map(str, base[10 - base_len:])) + '/' + bank_code
            if (prefix):
                recs[i] = ''.join(
                    map(str, pref[6 - prefix_len:])) + '-' + recs[i]
        else:
            recs[i] = country + bank_code
            recs[i] += ''.join(map(str, pref)) if (prefix) else '000000'
            recs[i] += ''.join(map(str, base))

    return recs if (cnt > 1) else recs[0]


def gen_email(name_len=8, subdomain=None, subdomain_len=6, domain='.com', domain_type='original', cnt=1):
    """Method generates random email   

    Args:
       name_len (int): name length
       subdomain (str): subdomain, random generated if empty
       subdomain_len (int): subdomain length
       domain (str): domain, generated from db table domain if empty
       domain_type (str): type of domain original (i.e. .com,.org) or country (i.e. .cz,.de)
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (domain_type not in ['original', 'country']):
        raise ValueError('domain_type must be in original|country')

    if (domain == None):
        db = DBO(_get_dsn())._dbo_driver
        query = 'SELECT code FROM domain WHERE type=\'{0}\' LIMIT {1} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM domain WHERE type = \'{2}\')'.format(
            domain_type, cnt if (cnt < 100) else 100, domain_type)
        domains = db.execute(query).fetchall()
        domain_len = len(domains)

    recs = [None] * cnt
    names = gen_string(name_len, 'alphanumeric', cnt)
    subdomains = [
        subdomain] * cnt if (subdomain != None) else gen_string(subdomain_len, 'lower', cnt)
    if (cnt == 1):
        names = [names]
        if (subdomain == None):
            subdomains = [subdomains]

    for i in range(0, cnt):
        email = names[i] + '@' + subdomains[i]
        email += domain if (domain !=
                            None) else str(domains[randint(0, domain_len - 1)][0])
        recs[i] = email

    return recs if (cnt > 1) else recs[0]


def gen_name(sex='both', tuple_out=True, cnt=1):
    """Method generates random email   

    Args:
       sex (str): sex both|male|female
       tuple_out (bool): tuple output (first_name, surname) otherwise str (first_name+surname)
       cnt (int): count of generated samples

    Returns:
       obj: tuple|str or list

    Raises:
       error: ValueError

    """

    if (sex not in ['both', 'male', 'female']):
        raise ValueError('sex must be in boty|male|female')

    db = DBO(_get_dsn())._dbo_driver
    if (sex == 'both'):
        query = 'SELECT name, sex FROM first_name  LIMIT {0} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM first_name)'.format(
            cnt if (cnt < 100) else 100)
        first_names = db.execute(query).fetchall()
        query = 'SELECT name FROM surname WHERE sex = \'{0}\' LIMIT {1} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM surname WHERE sex = \'{2}\')'
        surnames = [db.execute(query.format('M', cnt if (cnt < 100) else 100, 'M')).fetchall(),
                    db.execute(query.format('F', cnt if (cnt < 100) else 100, 'F')).fetchall()]
    else:
        filter = 'WHERE sex = \'M\'' if (
            sex == 'male') else 'WHERE sex = \'F\''
        query = 'SELECT name FROM first_name {0} LIMIT {1} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM first_name {2})'.format(
            filter, cnt if (cnt < 100) else 100, filter)
        first_names = db.execute(query).fetchall()
        query = 'SELECT name FROM surname {0} LIMIT {1} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM surname {2})'.format(
            filter, cnt if (cnt < 100) else 100, filter)
        surnames = db.execute(query).fetchall()

    first_name_len = len(first_names)
    surname_len = len(surnames) if (
        sex != 'both') else [len(surnames[0]), len(surnames[1])]
    recs = [None] * cnt
    for i in range(0, cnt):
        if (sex == 'both'):
            first_name, db_sex = first_names[randint(0, first_name_len - 1)]
            surname = surnames[0][randint(0, surname_len[
                                          0] - 1)][0] if (db_sex == u'M') else surnames[1][randint(0, surname_len[1] - 1)][0]
        else:
            first_name = first_names[randint(0, first_name_len - 1)][0]
            surname = surnames[randint(0, surname_len - 1)][0]
        if (version_info[0] == 2):
            recs[i] = (first_name.encode('utf-8'), surname.encode('utf-8'))
        else:
            recs[i] = (
                first_name.encode('utf-8').decode(), surname.encode('utf-8').decode())

    if (not tuple_out):
        for i in range(0, cnt):
            recs[i] = '{0} {1}'.format(recs[i][0], recs[i][1])

    return recs if (cnt > 1) else recs[0]


def gen_phone(form='int', cc=420, country=None, ndc=601, sn_len=6, cnt=1):
    """Method generates random phone number  

    Args:
       form (str): number format int|nat international, national
       cc (int): country code, generated from db table cc if empty
       country (str): country title, country code got from table cc if cc empty
       ndc (int): national destination code, random generated if empty or if cc empty
       sn_len (int): length of subcriber number
       cnt (int): count of generated samples

    Returns:
       obj: str or list

    Raises:
       error: ValueError

    """

    if (form not in ['int', 'nat']):
        raise ValueError('form must be in int|nat')

    if (cc == None):
        db = DBO(_get_dsn())._dbo_driver
        query = 'SELECT code FROM cc LIMIT {0} OFFSET ABS(RANDOM()) % (SELECT count(*) FROM cc)'.format(
            cnt if (cnt < 100) else 100)
        codes = db.execute(query).fetchall()
        codes_len = len(codes)
    elif (country != None):
        db = DBO(_get_dsn())._dbo_driver
        query = 'SELECT code FROM cc WHERE title = \'{0}\' LIMIT 1'.format(
            country)
        cc = db.execute(query).fetchone()
        if (cc == None):
            raise ValueError('Unknown country {0}'.format(country))
        cc = cc[0]

    recs = [None] * cnt
    for i in range(0, cnt):
        if (form == 'int'):
            phone = '+' + str(cc) if (cc != None) else '+' + \
                str(codes[randint(0, codes_len - 1)][0])
        else:
            phone = ''
        phone += str(ndc) if (ndc != None) else str(randint(100, 999))
        phone += str(randint(10**(sn_len - 1), 10**sn_len - 1))
        recs[i] = phone

    return recs if (cnt > 1) else recs[0]


def gen_address(param=None, value=None, street_no_full=True, dict_out=True, cnt=1):
    """Method generates random address

    Database contains czech addresses

    Args:
       param (str): type of address parameter region|district|area|locality|part
       value (str): parameter value, searched in db table region|district|area|locality|part
                                                    czech kraj|okres|oblast|obec|cast obce
       street_no (str): generate street number with descriptive and orientation number otherwise descriptive
       dict_out (bool) generate address as dict, otherwise str (street number, part, ZIP code)
       cnt (int): count of generated samples

    Returns:
       obj: dict|str or list

    Raises:
       error: ValueError

    """

    if (param != None and param not in ['region', 'district', 'area', 'locality', 'part']):
        raise ValueError('param must be in region|district|area|locality|part')

    db = DBO(_get_dsn())._dbo_driver
    if (param == None):
        query = 'SELECT count(*) FROM street'
        street_len = db.execute(query).fetchone()[0]
        query = """SELECT a.title as region, b.title as district, c.title as area, d.title as locality, e.title as part, e.zip, f.title as street
                   FROM region a, district b, area c, locality d, part e, street f WHERE f.part = e.code AND e.locality = d.code
                   AND d.area = c.code AND c.district = b.code AND b.region = a.code LIMIT 1 OFFSET ABS(RANDOM()) % {0}""".format(street_len)
    elif (param == 'part'):
        part = db.execute(
            'SELECT code FROM part WHERE title = \'{0}\''.format(value)).fetchone()
        if (part == None):
            raise ValueError('Unknown part {0}'.format(value))
        query = 'SELECT count(*) FROM street WHERE part = {0}'.format(part[0])
        street_len = db.execute(query).fetchone()[0]
        query = """SELECT a.title as region, b.title as district, c.title as area, d.title as locality, e.title as part, e.zip, f.title as street
                   FROM region a, district b, area c, locality d, part e, street f WHERE e.code = {0} AND f.part = e.code AND e.locality = d.code
                   AND d.area = c.code AND c.district = b.code AND b.region = a.code LIMIT 1 OFFSET ABS(RANDOM()) % {1}""".format(part[0], street_len)
    elif (param == 'locality'):
        locality = db.execute(
            'SELECT code FROM locality WHERE title = \'{0}\''.format(value)).fetchone()
        if (locality == None):
            raise ValueError('Unknown locality {0}'.format(value))
        query = 'SELECT count(*) FROM street a, part b WHERE a.part = b.code AND b.locality = {0}'.format(
            locality[0])
        street_len = db.execute(query).fetchone()[0]
        query = """SELECT a.title as region, b.title as district, c.title as area, d.title as locality, e.title as part, e.zip, f.title as street
                   FROM region a, district b, area c, locality d, part e, street f WHERE d.code = {0} AND f.part = e.code AND e.locality = d.code
                   AND d.area = c.code AND c.district = b.code AND b.region = a.code LIMIT 1 OFFSET ABS(RANDOM()) % {1}""".format(locality[0], street_len)
    elif (param == 'area'):
        area = db.execute(
            'SELECT code FROM area WHERE title = \'{0}\''.format(value)).fetchone()
        if (area == None):
            raise ValueError('Unknown area {0}'.format(value))
        query = 'SELECT count(*) FROM street a, part b, locality c WHERE a.part = b.code AND b.locality = c.code AND c.area = {0}'.format(
            area[0])
        street_len = db.execute(query).fetchone()[0]
        query = """SELECT a.title as region, b.title as district, c.title as area, d.title as locality, e.title as part, e.zip, f.title as street
                   FROM region a, district b, area c, locality d, part e, street f WHERE c.code = {0} AND f.part = e.code AND e.locality = d.code
                   AND d.area = c.code AND c.district = b.code AND b.region = a.code LIMIT 1 OFFSET ABS(RANDOM()) % {1}""".format(area[0], street_len)
    elif (param == 'district'):
        district = db.execute(
            'SELECT code FROM district WHERE title = \'{0}\''.format(value)).fetchone()
        if (district == None):
            raise ValueError('Unknown district {0}'.format(value))
        query = """SELECT count(*) FROM street a, part b, locality c, area d WHERE a.part = b.code AND b.locality = c.code 
                AND c.area = d.code AND d.district = {0}""".format(district[0])
        street_len = db.execute(query).fetchone()[0]
        query = """SELECT a.title as region, b.title as district, c.title as area, d.title as locality, e.title as part, e.zip, f.title as street
                   FROM region a, district b, area c, locality d, part e, street f WHERE b.code = {0} AND f.part = e.code AND e.locality = d.code
                   AND d.area = c.code AND c.district = b.code AND b.region = a.code LIMIT 1 OFFSET ABS(RANDOM()) % {1}""".format(district[0], street_len)
    elif (param == 'region'):
        region = db.execute(
            'SELECT code FROM region WHERE title = \'{0}\''.format(value)).fetchone()
        if (region == None):
            raise ValueError('Unknown region {0}'.format(value))
        query = """SELECT count(*) FROM street a, part b, locality c, area d, district e WHERE a.part = b.code AND b.locality = c.code 
                AND c.area = d.code AND d.district = e.code AND e.region = {0}""".format(region[0])
        street_len = db.execute(query).fetchone()[0]
        query = """SELECT a.title as region, b.title as district, c.title as area, d.title as locality, e.title as part, e.zip, f.title as street
                   FROM region a, district b, area c, locality d, part e, street f WHERE a.code = {0} AND f.part = e.code AND e.locality = d.code
                   AND d.area = c.code AND c.district = b.code AND b.region = a.code LIMIT 1 OFFSET ABS(RANDOM()) % {1}""".format(region[0], street_len)

    recs = [None] * cnt
    for i in range(0, cnt):
        addr = db.execute(query).fetchone()
        if (version_info[0] == 2):
            address = {'region': addr[0].encode('utf-8'), 'district': addr[1].encode('utf-8'), 'area': addr[2].encode('utf-8'),
                       'locality': addr[3].encode('utf-8'), 'part': addr[4].encode('utf-8'), 'street': addr[6].encode('utf-8'), 'zip': addr[5]}
        else:
            address = {'region': addr[0].encode('utf-8').decode(), 'district': addr[1].encode('utf-8').decode(), 'area': addr[2].encode('utf-8').decode(),
                       'locality': addr[3].encode('utf-8').decode(), 'part': addr[4].encode('utf-8').decode(), 'street': addr[6].encode('utf-8').decode(), 'zip': addr[5]}
        address['street_no'] = '{0}/{1}'.format(randint(100, 10000), randint(1, 99)) if (
            street_no_full) else str(randint(1, 99))
        if (not dict_out):
            address = '{0} {1}, {2}, {3}'.format(
                address['street'], address['street_no'], address['part'], address['zip'])
        recs[i] = address

    return recs if (cnt > 1) else recs[0]


def _get_dsn():
    """Method gets dsn from config

    Args:
       none

    Returns:
       str 

    """

    mh = MasterHead.get_head()
    return mh.ext_cfg['Yoda']['db_testdata_dsn'].format(var_dir=syscfg.HTK_VAR_DIR)


def create_type(title, description=None, col_titles=[]):
    """Method creates data type

    Args:
       title (str): type title
       description (str): type description
       col_titles (list): list of string, max length 10 

    Returns:
       bool 

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        cnt = db.execute(
            'SELECT count(*) FROM data_type WHERE TITLE = \'{0}\''.format(title)).fetchone()[0]
        if (cnt > 0):
            raise Error('Type {0} already exists'.format(title))

        query = """INSERT INTO data_type (title, description, col1_title, col2_title, col3_title, col4_title, col5_title,
                   col6_title, col7_title, col8_title, col9_title, col10_title) VALUES (\'{0}\'""".format(title)
        query += ', \'{0}\''.format(description) if (description !=
                                                     None) else ', null'
        col_len = len(col_titles)
        for i in range(0, 10):
            query += ', \'{0}\''.format(col_titles[i]
                                        ) if (i < col_len) else ', null'
        query += ')'
        db.execute(query)
        db.commit()

        return True
    except Error as ex:
        print(ex)
        db.rollback()
        return False


def update_type(title, title_new=None, description=None, col_titles_new={}):
    """Method creates data type

    Args:
       title (str): current type title
       title_new (str): new type title
       description (str): type description
       col_titles_new (dict): new column values (key - col id, value - col value)

    Returns:
       bool 

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        cnt = db.execute(
            'SELECT count(*) FROM data_type WHERE title = \'{0}\''.format(title)).fetchone()[0]
        if (cnt == 0):
            raise Error('Type {0} does not exist'.format(title))

        query = 'UPDATE data_type SET '
        if (title_new != None):
            query += 'title = \'{0}\', '.format(title_new)
        if (description != None):
            query += 'description = \'{0}\', '.format(description)
        for key, value in col_titles_new.items():
            query += 'col{0}_title = \'{1}\', '.format(key, value)
        query = query[:-2]
        query += ' WHERE title = \'{0}\''.format(title)
        db.execute(query)
        db.commit()

        return True
    except Error as ex:
        print(ex)
        db.rollback()
        return False


def delete_type(title, del_records=True):
    """Method deletes data type

    Args:
       title (str): type title
       del_records (bool): delete assigned records in table data

    Returns:
       bool 

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        cnt = db.execute(
            'SELECT count(*) FROM data_type WHERE title = \'{0}\''.format(title)).fetchone()[0]
        if (cnt == 0):
            raise Error('Type {0} does not exist'.format(title))

        if (del_records):
            query = 'DELETE FROM data WHERE type = (SELECT id FROM data_type WHERE title = \'{0}\')'.format(
                title)
            db.execute(query)
        query = 'DELETE FROM data_type WHERE title = \'{0}\''.format(title)
        db.execute(query)
        db.commit()

        return True
    except Error as ex:
        print(ex)
        db.rollback()
        return False


def read_data(data_type, active=1, col_filter={}):
    """Method reads data

    Args:
       data_type (str): data_type
       active (int): column active value (1-active, 0-deactive)
       col_filter (dict): column values to set filter (key - col id, value - col value)

    Returns:
       list: list of dict (key - column title, value - column value)

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        res = db.execute(
            'SELECT id FROM data_type WHERE title = \'{0}\''.format(data_type)).fetchone()
        if (res == None):
            raise Error('Unknown data type {0}'.format(data_type))
        type_id = res[0]

        query = """SELECT b.title, a.active, b.col1_title, a.col1, b.col2_title, a.col2, b.col3_title, a.col3, b.col4_title, a.col4,
                   b.col5_title, a.col5, b.col6_title, a.col6, b.col7_title, a.col7, b.col8_title, a.col8, b.col9_title, a.col9, 
                   b.col10_title, a.col10 FROM data a, data_type b WHERE a.type = {0} AND a.type = b.id AND a.active = {1} AND """.format(type_id, active)
        for key, value in col_filter.items():
            query += 'a.col{0} = \'{1}\' AND '.format(key, value)
        query = query[:-5]

        rows = db.execute(query).fetchall()
        recs = []
        for r in rows:
            if (version_info[0] == 2):
                rec = {'type': r[0].encode('utf-8'), 'active': int(r[1]), r[2].encode('utf-8'): r[3].encode('utf-8'), r[4].encode('utf-8'): r[5].encode('utf-8'),
                       r[6].encode('utf-8'): r[7].encode('utf-8'), r[8].encode('utf-8'): r[9].encode('utf-8'), r[10].encode('utf-8'): r[11].encode('utf-8'),
                       r[12].encode('utf-8'): r[13].encode('utf-8'), r[14].encode('utf-8'): r[15].encode('utf-8'), r[16].encode('utf-8'): r[17].encode('utf-8'),
                       r[18].encode('utf-8'): r[19].encode('utf-8'), r[20].encode('utf-8'): r[21].encode('utf-8')}
            else:
                rec = {'type': r[0].encode('utf-8').decode(), 'active': int(r[1]), r[2].encode('utf-8').decode(): r[3].encode('utf-8').decode(),
                       r[4].encode('utf-8').decode(): r[5].encode('utf-8').decode(), r[6].encode('utf-8').decode(): r[7].encode('utf-8').decode(),
                       r[8].encode('utf-8').decode(): r[9].encode('utf-8').decode(), r[10].encode('utf-8').decode(): r[11].encode('utf-8').decode(),
                       r[12].encode('utf-8').decode(): r[13].encode('utf-8').decode(), r[14].encode('utf-8').decode(): r[15].encode('utf-8').decode(),
                       r[16].encode('utf-8').decode(): r[17].encode('utf-8').decode(), r[18].encode('utf-8').decode(): r[19].encode('utf-8').decode(),
                       r[20].encode('utf-8'): r[21].encode('utf-8')}
            recs.append(rec)

        return recs
    except Error as ex:
        print(ex)
        return None


def create_data(data_type, active=1, col_values={}):
    """Method creates data

    Args:
       data_type (str): data_type
       active (int): column active value (1-active, 0-deactive)
       col_values (dict): column values (key - col id, value - col value)

    Returns:
       bool

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        res = db.execute(
            'SELECT id FROM data_type WHERE title = \'{0}\''.format(data_type)).fetchone()
        if (res == None):
            raise Error('Unknown data type {0}'.format(data_type))
        type_id = res[0]

        query = """INSERT INTO data (type, active, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10)
                   VALUES ({0}, {1}, """.format(type_id, active)
        for i in range(1, 11):
            query += '\'{0}\', '.format(col_values[i]
                                        ) if (i in col_values.keys()) else 'null, '
        query = query[:-2] + ')'

        db.execute(query)
        db.commit()

        return True

    except Error as ex:
        print(ex)
        db.rollback()
        return False


def update_data(data_type, active=None, col_filter={}, col_values_new={}):
    """Method updates data

    Args:
       data_type (str): data_type
       active (int): column active value (1-active, 0-deactive)
       col_filter (dict): column values to set filter (key - col id, value - col value)
       col_values_new (dict): new column values (key - col id, value - col value)

    Returns:
       bool

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        res = db.execute(
            'SELECT id FROM data_type WHERE title = \'{0}\''.format(data_type)).fetchone()
        if (res == None):
            raise Error('Unknown data type {0}'.format(data_type))
        type_id = res[0]

        query = 'UPDATE data SET '
        if (active != None):
            query += 'active = {0}, '.format(active)
        for key, value in col_values_new.items():
            query += 'col{0} = \'{1}\', '.format(key, value)
        query = query[:-2] + ' WHERE type = {0} AND '.format(type_id)
        for key, value in col_filter.items():
            query += 'col{0} = \'{1}\' AND '.format(key, value)
        query = query[:-5]

        db.execute(query)
        db.commit()

        return True

    except Error as ex:
        print(ex)
        db.rollback()
        return False


def delete_data(data_type, active=0, col_filter={}):
    """Method deletes data

    Args:
       data_type (str): data_type
       active (int): column active value (1-active, 0-deactive)
       col_filter (dict): column values to set filter (key - col id, value - col value)

    Returns:
       bool

    """

    try:
        db = DBO(_get_dsn())._dbo_driver
        res = db.execute(
            'SELECT id FROM data_type WHERE title = \'{0}\''.format(data_type)).fetchone()
        if (res == None):
            raise Error('Unknown data type {0}'.format(data_type))
        type_id = res[0]

        query = 'DELETE FROM data WHERE type = {0} AND active = {1} AND '.format(
            type_id, active)
        for key, value in col_filter.items():
            query += 'col{0} = \'{1}\' AND '.format(key, value)
        query = query[:-5]

        db.execute(query)
        db.commit()

        return True

    except Error as ex:
        print(ex)
        db.rollback()
        return False
