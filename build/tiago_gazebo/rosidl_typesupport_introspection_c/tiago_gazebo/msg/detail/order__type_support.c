// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from tiago_gazebo:msg/Order.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "tiago_gazebo/msg/detail/order__rosidl_typesupport_introspection_c.h"
#include "tiago_gazebo/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "tiago_gazebo/msg/detail/order__functions.h"
#include "tiago_gazebo/msg/detail/order__struct.h"


// Include directives for member types
// Member `item`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  tiago_gazebo__msg__Order__init(message_memory);
}

void tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_fini_function(void * message_memory)
{
  tiago_gazebo__msg__Order__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_member_array[2] = {
  {
    "destination_table_number",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(tiago_gazebo__msg__Order, destination_table_number),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "item",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(tiago_gazebo__msg__Order, item),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_members = {
  "tiago_gazebo__msg",  // message namespace
  "Order",  // message name
  2,  // number of fields
  sizeof(tiago_gazebo__msg__Order),
  tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_member_array,  // message members
  tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_init_function,  // function to initialize message memory (memory has to be allocated)
  tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle = {
  0,
  &tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_tiago_gazebo
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, tiago_gazebo, msg, Order)() {
  if (!tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle.typesupport_identifier) {
    tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &tiago_gazebo__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
