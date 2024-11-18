// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from tiago_gazebo:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef TIAGO_GAZEBO__MSG__DETAIL__ORDER__STRUCT_H_
#define TIAGO_GAZEBO__MSG__DETAIL__ORDER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'item'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Order in the package tiago_gazebo.
/**
  * Order.msg
 */
typedef struct tiago_gazebo__msg__Order
{
  int32_t destination_table_number;
  rosidl_runtime_c__String item;
} tiago_gazebo__msg__Order;

// Struct for a sequence of tiago_gazebo__msg__Order.
typedef struct tiago_gazebo__msg__Order__Sequence
{
  tiago_gazebo__msg__Order * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tiago_gazebo__msg__Order__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TIAGO_GAZEBO__MSG__DETAIL__ORDER__STRUCT_H_
