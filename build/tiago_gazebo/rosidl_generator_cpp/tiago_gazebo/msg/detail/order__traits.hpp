// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from tiago_gazebo:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef TIAGO_GAZEBO__MSG__DETAIL__ORDER__TRAITS_HPP_
#define TIAGO_GAZEBO__MSG__DETAIL__ORDER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "tiago_gazebo/msg/detail/order__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace tiago_gazebo
{

namespace msg
{

inline void to_flow_style_yaml(
  const Order & msg,
  std::ostream & out)
{
  out << "{";
  // member: destination_table_number
  {
    out << "destination_table_number: ";
    rosidl_generator_traits::value_to_yaml(msg.destination_table_number, out);
    out << ", ";
  }

  // member: item
  {
    out << "item: ";
    rosidl_generator_traits::value_to_yaml(msg.item, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Order & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: destination_table_number
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "destination_table_number: ";
    rosidl_generator_traits::value_to_yaml(msg.destination_table_number, out);
    out << "\n";
  }

  // member: item
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "item: ";
    rosidl_generator_traits::value_to_yaml(msg.item, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Order & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace tiago_gazebo

namespace rosidl_generator_traits
{

[[deprecated("use tiago_gazebo::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const tiago_gazebo::msg::Order & msg,
  std::ostream & out, size_t indentation = 0)
{
  tiago_gazebo::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use tiago_gazebo::msg::to_yaml() instead")]]
inline std::string to_yaml(const tiago_gazebo::msg::Order & msg)
{
  return tiago_gazebo::msg::to_yaml(msg);
}

template<>
inline const char * data_type<tiago_gazebo::msg::Order>()
{
  return "tiago_gazebo::msg::Order";
}

template<>
inline const char * name<tiago_gazebo::msg::Order>()
{
  return "tiago_gazebo/msg/Order";
}

template<>
struct has_fixed_size<tiago_gazebo::msg::Order>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<tiago_gazebo::msg::Order>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<tiago_gazebo::msg::Order>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // TIAGO_GAZEBO__MSG__DETAIL__ORDER__TRAITS_HPP_
