// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/motor_cmds.hpp"


#ifndef INTERFACES__MSG__DETAIL__MOTOR_CMDS__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__MOTOR_CMDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/motor_cmds__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_MotorCmds_t6
{
public:
  explicit Init_MotorCmds_t6(::interfaces::msg::MotorCmds & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::MotorCmds t6(::interfaces::msg::MotorCmds::_t6_type arg)
  {
    msg_.t6 = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

class Init_MotorCmds_t5
{
public:
  explicit Init_MotorCmds_t5(::interfaces::msg::MotorCmds & msg)
  : msg_(msg)
  {}
  Init_MotorCmds_t6 t5(::interfaces::msg::MotorCmds::_t5_type arg)
  {
    msg_.t5 = std::move(arg);
    return Init_MotorCmds_t6(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

class Init_MotorCmds_t4
{
public:
  explicit Init_MotorCmds_t4(::interfaces::msg::MotorCmds & msg)
  : msg_(msg)
  {}
  Init_MotorCmds_t5 t4(::interfaces::msg::MotorCmds::_t4_type arg)
  {
    msg_.t4 = std::move(arg);
    return Init_MotorCmds_t5(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

class Init_MotorCmds_t3
{
public:
  explicit Init_MotorCmds_t3(::interfaces::msg::MotorCmds & msg)
  : msg_(msg)
  {}
  Init_MotorCmds_t4 t3(::interfaces::msg::MotorCmds::_t3_type arg)
  {
    msg_.t3 = std::move(arg);
    return Init_MotorCmds_t4(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

class Init_MotorCmds_t2
{
public:
  explicit Init_MotorCmds_t2(::interfaces::msg::MotorCmds & msg)
  : msg_(msg)
  {}
  Init_MotorCmds_t3 t2(::interfaces::msg::MotorCmds::_t2_type arg)
  {
    msg_.t2 = std::move(arg);
    return Init_MotorCmds_t3(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

class Init_MotorCmds_t1
{
public:
  explicit Init_MotorCmds_t1(::interfaces::msg::MotorCmds & msg)
  : msg_(msg)
  {}
  Init_MotorCmds_t2 t1(::interfaces::msg::MotorCmds::_t1_type arg)
  {
    msg_.t1 = std::move(arg);
    return Init_MotorCmds_t2(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

class Init_MotorCmds_t0
{
public:
  Init_MotorCmds_t0()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorCmds_t1 t0(::interfaces::msg::MotorCmds::_t0_type arg)
  {
    msg_.t0 = std::move(arg);
    return Init_MotorCmds_t1(msg_);
  }

private:
  ::interfaces::msg::MotorCmds msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::MotorCmds>()
{
  return interfaces::msg::builder::Init_MotorCmds_t0();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__MOTOR_CMDS__BUILDER_HPP_
