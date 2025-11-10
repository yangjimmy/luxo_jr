// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice

#include "interfaces/msg/detail/motor_cmds__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_interfaces
const rosidl_type_hash_t *
interfaces__msg__MotorCmds__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x48, 0xb7, 0x84, 0xda, 0x52, 0x80, 0xa4, 0x67,
      0x2c, 0x17, 0x35, 0xb6, 0x7c, 0x9c, 0xa4, 0xb6,
      0xa0, 0xf3, 0xa0, 0x57, 0x23, 0xdf, 0x75, 0x2a,
      0x6b, 0xbf, 0x3c, 0x86, 0xd0, 0xd4, 0xa8, 0x9b,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char interfaces__msg__MotorCmds__TYPE_NAME[] = "interfaces/msg/MotorCmds";

// Define type names, field names, and default values
static char interfaces__msg__MotorCmds__FIELD_NAME__t0[] = "t0";
static char interfaces__msg__MotorCmds__FIELD_NAME__t1[] = "t1";
static char interfaces__msg__MotorCmds__FIELD_NAME__t2[] = "t2";
static char interfaces__msg__MotorCmds__FIELD_NAME__t3[] = "t3";
static char interfaces__msg__MotorCmds__FIELD_NAME__t4[] = "t4";
static char interfaces__msg__MotorCmds__FIELD_NAME__t5[] = "t5";
static char interfaces__msg__MotorCmds__FIELD_NAME__t6[] = "t6";

static rosidl_runtime_c__type_description__Field interfaces__msg__MotorCmds__FIELDS[] = {
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t0, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t1, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t2, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t3, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t4, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t5, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__MotorCmds__FIELD_NAME__t6, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
interfaces__msg__MotorCmds__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {interfaces__msg__MotorCmds__TYPE_NAME, 24, 24},
      {interfaces__msg__MotorCmds__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float64 t0\n"
  "float64 t1\n"
  "float64 t2\n"
  "float64 t3\n"
  "float64 t4\n"
  "float64 t5\n"
  "float64 t6";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
interfaces__msg__MotorCmds__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {interfaces__msg__MotorCmds__TYPE_NAME, 24, 24},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 77, 77},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
interfaces__msg__MotorCmds__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *interfaces__msg__MotorCmds__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
