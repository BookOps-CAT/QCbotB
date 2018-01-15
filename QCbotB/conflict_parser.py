import xml.etree.ElementTree as ET
import logging


module_logger = logging.getLogger('QCBtests')


def conflict2dict(conflicts_file=None):
    """
    reads encoded in xml conflicts information and
    returns list of dictionaries with error types and 
    associated SQL queries

    parameters
    ----------
    conflicts_file : xml file or None
        xml file containing error rules

    returns
    -------
    list
        list of dictionaries, example:
            {id=conflict id,
            code=conflict code,
            desc=conflict description,
            query=SQL query used for discovery in datastore,
            level=conflict level}
    """

    try:
        if conflicts_file is None:
            tree = ET.parse('./files/conflicts.xml')
        else:
            tree = ET.parse(conflicts_file)
    except IOError:
        tree = None
        module_logger.critical(
            'IOError while attempting to load xml file with conflicts;'
            'supplied location: {}. Aborting!'.format(
                conflicts_file))

    if tree is not None:
        conflicts = []
        root = tree.getroot()
        for error in root:
            try:
                level = error.attrib['level']
                id = error.attrib['id']
                code = error.attrib['code']
                desc = error.find('description').text
                query = error.find('query').text
            except AttributeError:
                module_logger.critical(
                    'AtrributeError while parsing conflict xml file')
                continue

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
            conflicts.append(dict(
                id=id,
                code=code,
                desc=desc,
                query=query,
                level=level))
        return conflicts
    else:
        return []

if __name__ == '__main__':
    print conflict2dict('./files/conflicts.xml')
