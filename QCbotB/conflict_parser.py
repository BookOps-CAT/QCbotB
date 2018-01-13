# reads rules for error file and returns list of dictonaries with
# conflicts

import xml.etree.ElementTree as ET
import logging


module_logger = logging.getLogger('QCBtests')


def conflict2dict(fh=None):

    """
    reads encoded in xml conflicts data
    returns list of dictionaries with error types and 
    associated SQL queries
    """

    try:
        if fh is None:
            tree = ET.parse('./files/conflicts.xml')
        else:
            tree = ET.parse(fh)
    except IOError:
        tree = None
        module_logger.critical(
            'IOError while attempting to load xml file with conflicts;'
            'supplied location: {}. Aborting!'.format(
                fh))

    if tree is not None:
        conflicts = []
        root = tree.getroot()
        for level in root:
            level_name = level.attrib['name']
            for error in level:
                code = error.attrib['code']
                try:
                    id = int(error.attrib['id'])
                except TypeError:
                    module_logger.critical(
                        'TypeError on id in "conflicts.xml", '
                        'found data: code={}, id={}. Conflict will not '
                        'be added to datastore'.format(
                            code,
                            error.attrib['id']))
                    continue
                desc = error.find('description').text
                query = error.find('query').text
                conflicts.append(dict(
                    id=id,
                    code=code,
                    desc=desc,
                    query=query,
                    level=level_name))
        return conflicts
    else:
        return []
