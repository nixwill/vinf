from typing import Dict, Optional, Tuple

import re

from .common import Data


pattern = re.compile(
    r'<http://rdf\.freebase\.com/ns/(?P<s_id>(?P<s_domain>.+?)(?:\.(?P<s_type>.+?)(?:\.(?P<s_property>.+?))?)?)>\t'
    r'<http://rdf\.freebase\.com/ns/(?P<p_id>(?P<p_domain>.+?)(?:\.(?P<p_type>.+?)(?:\.(?P<p_property>.+?))?)?)>\t'
    r'(?:'
    r'<http://rdf\.freebase\.com/ns/(?P<o_id>(?P<o_domain>.+?)(?:\.(?P<o_type>.+?)(?:\.(?P<o_property>.+?))?)?)>'
    r'|"(?P<literal>.*)"(?:@(?P<locale>.+?))?'
    r')\t'
    r'\.'
)


def is_object_instance_of_type(groupdict: Dict[str, str]) -> bool:
    return (groupdict['p_id'] == 'type.type.instance'
            and groupdict['s_property'] is None
            and groupdict['s_type'] is not None
            and groupdict['o_property'] is None
            and groupdict['o_type'] is not None
            and groupdict['o_domain'] in ('m', 'g', 'en'))


def is_subject_of_topic_type(groupdict: Dict[str, str]) -> bool:
    return (groupdict['p_id'] == 'type.object.type'
            and groupdict['s_property'] is None
            and groupdict['s_type'] is not None
            and groupdict['s_domain'] in ('m', 'g', 'en')
            and groupdict['o_id'] == 'common.topic')


def is_object_type_of_subject(groupdict: Dict[str, str]) -> bool:
    return (groupdict['p_id'] == 'type.object.type'
            and groupdict['s_property'] is None
            and groupdict['s_type'] is not None
            and groupdict['s_domain'] in ('m', 'g', 'en')
            and groupdict['o_id'] != 'common.topic'
            and groupdict['o_domain'] != 'base')


def is_object_name_of_subject(groupdict: Dict[str, str]) -> bool:
    return (groupdict['p_id'] == 'type.object.name'
            and groupdict['s_property'] is None
            and groupdict['s_type'] is not None
            and groupdict['s_domain'] in ('m', 'g', 'en')
            and groupdict['literal'] is not None
            and (groupdict['locale'] is None or groupdict['locale'].startswith('en')))


def is_object_alias_of_topic(groupdict: Dict[str, str]) -> bool:
    return (groupdict['p_id'] == 'common.topic.alias'
            and groupdict['s_property'] is None
            and groupdict['s_type'] is not None
            and groupdict['s_domain'] in ('m', 'g', 'en')
            and groupdict['literal'] is not None
            and (groupdict['locale'] is None or groupdict['locale'].startswith('en')))


def parse_line_into_kv_pair(line: str) -> Optional[Tuple[str, Data]]:

    if match := pattern.fullmatch(line.strip()):
        groupdict = match.groupdict()

        if is_object_instance_of_type(groupdict):
            return groupdict['o_id'], Data(types={groupdict['s_type']})

        if is_object_type_of_subject(groupdict):
            return groupdict['s_id'], Data(types={groupdict['o_type']})

        if is_object_name_of_subject(groupdict):
            return groupdict['s_id'], Data(title=groupdict['literal'])

        if is_subject_of_topic_type(groupdict):
            return groupdict['s_id'], Data(topic=True, types={'topic'})

        if is_object_alias_of_topic(groupdict):
            return groupdict['s_id'], Data(aliases={groupdict['literal']})

    return None
