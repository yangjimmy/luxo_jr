// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/motor_cmds.hpp"


#ifndef INTERFACES__MSG__DETAIL__MOTOR_CMDS__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__MOTOR_CMDS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__MotorCmds __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__MotorCmds __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorCmds_
{
  using Type = MotorCmds_<ContainerAllocator>;

  explicit MotorCmds_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->t0 = 0.0;
      this->t1 = 0.0;
      this->t2 = 0.0;
      this->t3 = 0.0;
      this->t4 = 0.0;
      this->t5 = 0.0;
      this->t6 = 0.0;
    }
  }

  explicit MotorCmds_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->t0 = 0.0;
      this->t1 = 0.0;
      this->t2 = 0.0;
      this->t3 = 0.0;
      this->t4 = 0.0;
      this->t5 = 0.0;
      this->t6 = 0.0;
    }
  }

  // field types and members
  using _t0_type =
    double;
  _t0_type t0;
  using _t1_type =
    double;
  _t1_type t1;
  using _t2_type =
    double;
  _t2_type t2;
  using _t3_type =
    double;
  _t3_type t3;
  using _t4_type =
    double;
  _t4_type t4;
  using _t5_type =
    double;
  _t5_type t5;
  using _t6_type =
    double;
  _t6_type t6;

  // setters for named parameter idiom
  Type & set__t0(
    const double & _arg)
  {
    this->t0 = _arg;
    return *this;
  }
  Type & set__t1(
    const double & _arg)
  {
    this->t1 = _arg;
    return *this;
  }
  Type & set__t2(
    const double & _arg)
  {
    this->t2 = _arg;
    return *this;
  }
  Type & set__t3(
    const double & _arg)
  {
    this->t3 = _arg;
    return *this;
  }
  Type & set__t4(
    const double & _arg)
  {
    this->t4 = _arg;
    return *this;
  }
  Type & set__t5(
    const double & _arg)
  {
    this->t5 = _arg;
    return *this;
  }
  Type & set__t6(
    const double & _arg)
  {
    this->t6 = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::MotorCmds_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::MotorCmds_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::MotorCmds_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::MotorCmds_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::MotorCmds_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::MotorCmds_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::MotorCmds_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::MotorCmds_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::MotorCmds_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::MotorCmds_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__MotorCmds
    std::shared_ptr<interfaces::msg::MotorCmds_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__MotorCmds
    std::shared_ptr<interfaces::msg::MotorCmds_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorCmds_ & other) const
  {
    if (this->t0 != other.t0) {
      return false;
    }
    if (this->t1 != other.t1) {
      return false;
    }
    if (this->t2 != other.t2) {
      return false;
    }
    if (this->t3 != other.t3) {
      return false;
    }
    if (this->t4 != other.t4) {
      return false;
    }
    if (this->t5 != other.t5) {
      return false;
    }
    if (this->t6 != other.t6) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorCmds_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorCmds_

// alias to use template instance with default allocator
using MotorCmds =
  interfaces::msg::MotorCmds_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__MOTOR_CMDS__STRUCT_HPP_
