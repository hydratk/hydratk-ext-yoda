# -*- coding: utf-8 -*-
"""Module with check utilities 

.. module:: yoda.util.check
   :platform: Unix
   :synopsis: Module with check utilities
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from lxml.etree import fromstring, XMLSyntaxError, XPathEvalError
from simplejson import loads
from simplejson.scanner import JSONDecodeError
from re import findall
from sre_constants import error


def load_json(document):
    """Methods loads JSON document

    Args:
       document (str): JSON document

    Returns:
       dict

    """

    try:
        return loads(document)
    except JSONDecodeError as ex:
        print(ex)
        return None


def load_xml(document):
    """Methods loads XML document

    Args:
       document (str): XML document

    Returns:
       obj

    """

    try:
        return fromstring(document)
    except XMLSyntaxError as ex:
        print(ex)
        return None


def xpath(document, expression, attribute=None, ns={}, get_text=True):
    """Methods performs XPATH query

    Args:
       document (obj): str or loaded XML document
       expression (str): XPATH expression
       attribute (str): element attribute
       ns (dict): namespaces definition
       get_text (bool): get element text content

    Returns:
       obj: str when get_text = True or attribute != None
            otherwise XPATH query output

    """

    if (document.__class__.__name__ == 'str'):
        document = load_xml(document)
        if (document == None):
            return None

    try:

        output = document.xpath(expression, namespaces=ns)
        if (len(output) > 0):
            if (attribute != None):
                output = output[0].attrib[attribute]
            elif (get_text):
                output = output[0].text
            elif (len(output) == 1):
                output = output[0]

        return output
    except XPathEvalError as ex:
        print(ex)
        return None


def regex(text, expression):
    """Methods performs regular expression search

    Args:
       text (str): text
       expression (str): regular expression

    Returns:
       obj: str or list

    """

    try:

        output = findall(expression, text)
        if (len(output) == 1):
            output = output[0] if (
                output[0].__class__.__name__ != 'tuple') else list(output[0])

        return output

    except error as ex:
        print(ex)
        return None
