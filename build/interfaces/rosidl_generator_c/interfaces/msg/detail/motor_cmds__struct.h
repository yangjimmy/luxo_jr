// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/motor_cmds.h"


#ifndef INTERFACES__MSG__DETAIL__MOTOR_CMDS__STRUCT_H_
#define INTERFACES__MSG__DETAIL__MOTOR_CMDS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/MotorCmds in the package interfaces.
typedef struct interfaces__msg__MotorCmds
{
  double t0;
  double t1;
  double t2;
  double t3;
  double t4;
  double t5;
  double t6;
} interfaces__msg__MotorCmds;

// Struct for a sequence of interfaces__msg__MotorCmds.
typedef struct interfaces__msg__MotorCmds__Sequence
{
  interfaces__msg__MotorCmds * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__MotorCmds__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__MOTOR_CMDS__STRUCT_H_
