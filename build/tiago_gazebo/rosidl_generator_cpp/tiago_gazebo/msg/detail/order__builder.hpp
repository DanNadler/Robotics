// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tiago_gazebo:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef TIAGO_GAZEBO__MSG__DETAIL__ORDER__BUILDER_HPP_
#define TIAGO_GAZEBO__MSG__DETAIL__ORDER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tiago_gazebo/msg/detail/order__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tiago_gazebo
{

namespace msg
{

namespace builder
{

class Init_Order_item
{
public:
  explicit Init_Order_item(::tiago_gazebo::msg::Order & msg)
  : msg_(msg)
  {}
  ::tiago_gazebo::msg::Order item(::tiago_gazebo::msg::Order::_item_type arg)
  {
    msg_.item = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tiago_gazebo::msg::Order msg_;
};

class Init_Order_destination_table_number
{
public:
  Init_Order_destination_table_number()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Order_item destination_table_number(::tiago_gazebo::msg::Order::_destination_table_number_type arg)
  {
    msg_.destination_table_number = std::move(arg);
    return Init_Order_item(msg_);
  }

private:
  ::tiago_gazebo::msg::Order msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::tiago_gazebo::msg::Order>()
{
  return tiago_gazebo::msg::builder::Init_Order_destination_table_number();
}

}  // namespace tiago_gazebo

#endif  // TIAGO_GAZEBO__MSG__DETAIL__ORDER__BUILDER_HPP_
