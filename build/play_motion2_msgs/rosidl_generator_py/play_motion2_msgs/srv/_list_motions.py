# generated from rosidl_generator_py/resource/_idl.py.em
# with input from play_motion2_msgs:srv/ListMotions.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ListMotions_Request(type):
    """Metaclass of message 'ListMotions_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('play_motion2_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'play_motion2_msgs.srv.ListMotions_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__list_motions__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__list_motions__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__list_motions__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__list_motions__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__list_motions__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ListMotions_Request(metaclass=Metaclass_ListMotions_Request):
    """Message class 'ListMotions_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_ListMotions_Response(type):
    """Metaclass of message 'ListMotions_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('play_motion2_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'play_motion2_msgs.srv.ListMotions_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__list_motions__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__list_motions__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__list_motions__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__list_motions__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__list_motions__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ListMotions_Response(metaclass=Metaclass_ListMotions_Response):
    """Message class 'ListMotions_Response'."""

    __slots__ = [
        '_motion_keys',
    ]

    _fields_and_field_types = {
        'motion_keys': 'sequence<string>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.motion_keys = kwargs.get('motion_keys', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.motion_keys != other.motion_keys:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def motion_keys(self):
        """Message field 'motion_keys'."""
        return self._motion_keys

    @motion_keys.setter
    def motion_keys(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'motion_keys' field must be a set or sequence and each value of type 'str'"
        self._motion_keys = value


class Metaclass_ListMotions(type):
    """Metaclass of service 'ListMotions'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('play_motion2_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'play_motion2_msgs.srv.ListMotions')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__list_motions

            from play_motion2_msgs.srv import _list_motions
            if _list_motions.Metaclass_ListMotions_Request._TYPE_SUPPORT is None:
                _list_motions.Metaclass_ListMotions_Request.__import_type_support__()
            if _list_motions.Metaclass_ListMotions_Response._TYPE_SUPPORT is None:
                _list_motions.Metaclass_ListMotions_Response.__import_type_support__()


class ListMotions(metaclass=Metaclass_ListMotions):
    from play_motion2_msgs.srv._list_motions import ListMotions_Request as Request
    from play_motion2_msgs.srv._list_motions import ListMotions_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
