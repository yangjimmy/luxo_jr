// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/motor_cmds.hpp"


#ifndef INTERFACES__MSG__DETAIL__MOTOR_CMDS__TRAITS_HPP_
#define INTERFACES__MSG__DETAIL__MOTOR_CMDS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces/msg/detail/motor_cmds__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotorCmds & msg,
  std::ostream & out)
{
  out << "{";
  // member: t0
  {
    out << "t0: ";
    rosidl_generator_traits::value_to_yaml(msg.t0, out);
    out << ", ";
  }

  // member: t1
  {
    out << "t1: ";
    rosidl_generator_traits::value_to_yaml(msg.t1, out);
    out << ", ";
  }

  // member: t2
  {
    out << "t2: ";
    rosidl_generator_traits::value_to_yaml(msg.t2, out);
    out << ", ";
  }

  // member: t3
  {
    out << "t3: ";
    rosidl_generator_traits::value_to_yaml(msg.t3, out);
    out << ", ";
  }

  // member: t4
  {
    out << "t4: ";
    rosidl_generator_traits::value_to_yaml(msg.t4, out);
    out << ", ";
  }

  // member: t5
  {
    out << "t5: ";
    rosidl_generator_traits::value_to_yaml(msg.t5, out);
    out << ", ";
  }

  // member: t6
  {
    out << "t6: ";
    rosidl_generator_traits::value_to_yaml(msg.t6, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorCmds & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: t0
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t0: ";
    rosidl_generator_traits::value_to_yaml(msg.t0, out);
    out << "\n";
  }

  // member: t1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t1: ";
    rosidl_generator_traits::value_to_yaml(msg.t1, out);
    out << "\n";
  }

  // member: t2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t2: ";
    rosidl_generator_traits::value_to_yaml(msg.t2, out);
    out << "\n";
  }

  // member: t3
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t3: ";
    rosidl_generator_traits::value_to_yaml(msg.t3, out);
    out << "\n";
  }

  // member: t4
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t4: ";
    rosidl_generator_traits::value_to_yaml(msg.t4, out);
    out << "\n";
  }

  // member: t5
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t5: ";
    rosidl_generator_traits::value_to_yaml(msg.t5, out);
    out << "\n";
  }

  // member: t6
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t6: ";
    rosidl_generator_traits::value_to_yaml(msg.t6, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorCmds & msg, bool use_flow_style = false)
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

}  // namespace interfaces

namespace rosidl_generator_traits
{

[[deprecated("use interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces::msg::MotorCmds & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const interfaces::msg::MotorCmds & msg)
{
  return interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces::msg::MotorCmds>()
{
  return "interfaces::msg::MotorCmds";
}

template<>
inline const char * name<interfaces::msg::MotorCmds>()
{
  return "interfaces/msg/MotorCmds";
}

template<>
struct has_fixed_size<interfaces::msg::MotorCmds>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interfaces::msg::MotorCmds>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interfaces::msg::MotorCmds>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES__MSG__DETAIL__MOTOR_CMDS__TRAITS_HPP_
