"""Common Configuration."""

from functools import partial

from google.protobuf.json_format import MessageToDict, ParseDict

MESSAGE_TO_DICT_KWARGS = {'preserving_proto_field_name': True, 'use_integers_for_enums': True}
PARSE_DICT_KWARGS = {'ignore_unknown_fields': True}

message_to_dict = partial(MessageToDict, **MESSAGE_TO_DICT_KWARGS)
parse_dict = partial(ParseDict, **PARSE_DICT_KWARGS)
