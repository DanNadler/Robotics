// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tiago_gazebo:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef TIAGO_GAZEBO__MSG__DETAIL__ORDER__STRUCT_HPP_
#define TIAGO_GAZEBO__MSG__DETAIL__ORDER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tiago_gazebo__msg__Order __attribute__((deprecated))
#else
# define DEPRECATED__tiago_gazebo__msg__Order __declspec(deprecated)
#endif

namespace tiago_gazebo
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Order_
{
  using Type = Order_<ContainerAllocator>;

  explicit Order_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->destination_table_number = 0l;
      this->item = "";
    }
  }

  explicit Order_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : item(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->destination_table_number = 0l;
      this->item = "";
    }
  }

  // field types and members
  using _destination_table_number_type =
    int32_t;
  _destination_table_number_type destination_table_number;
  using _item_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _item_type item;

  // setters for named parameter idiom
  Type & set__destination_table_number(
    const int32_t & _arg)
  {
    this->destination_table_number = _arg;
    return *this;
  }
  Type & set__item(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->item = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tiago_gazebo::msg::Order_<ContainerAllocator> *;
  using ConstRawPtr =
    const tiago_gazebo::msg::Order_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tiago_gazebo::msg::Order_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tiago_gazebo::msg::Order_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tiago_gazebo::msg::Order_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tiago_gazebo::msg::Order_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tiago_gazebo::msg::Order_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tiago_gazebo::msg::Order_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tiago_gazebo::msg::Order_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tiago_gazebo::msg::Order_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tiago_gazebo__msg__Order
    std::shared_ptr<tiago_gazebo::msg::Order_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tiago_gazebo__msg__Order
    std::shared_ptr<tiago_gazebo::msg::Order_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Order_ & other) const
  {
    if (this->destination_table_number != other.destination_table_number) {
      return false;
    }
    if (this->item != other.item) {
      return false;
    }
    return true;
  }
  bool operator!=(const Order_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Order_

// alias to use template instance with default allocator
using Order =
  tiago_gazebo::msg::Order_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace tiago_gazebo

#endif  // TIAGO_GAZEBO__MSG__DETAIL__ORDER__STRUCT_HPP_
