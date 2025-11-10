// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice
#include "interfaces/msg/detail/motor_cmds__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
interfaces__msg__MotorCmds__init(interfaces__msg__MotorCmds * msg)
{
  if (!msg) {
    return false;
  }
  // t0
  // t1
  // t2
  // t3
  // t4
  // t5
  // t6
  return true;
}

void
interfaces__msg__MotorCmds__fini(interfaces__msg__MotorCmds * msg)
{
  if (!msg) {
    return;
  }
  // t0
  // t1
  // t2
  // t3
  // t4
  // t5
  // t6
}

bool
interfaces__msg__MotorCmds__are_equal(const interfaces__msg__MotorCmds * lhs, const interfaces__msg__MotorCmds * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // t0
  if (lhs->t0 != rhs->t0) {
    return false;
  }
  // t1
  if (lhs->t1 != rhs->t1) {
    return false;
  }
  // t2
  if (lhs->t2 != rhs->t2) {
    return false;
  }
  // t3
  if (lhs->t3 != rhs->t3) {
    return false;
  }
  // t4
  if (lhs->t4 != rhs->t4) {
    return false;
  }
  // t5
  if (lhs->t5 != rhs->t5) {
    return false;
  }
  // t6
  if (lhs->t6 != rhs->t6) {
    return false;
  }
  return true;
}

bool
interfaces__msg__MotorCmds__copy(
  const interfaces__msg__MotorCmds * input,
  interfaces__msg__MotorCmds * output)
{
  if (!input || !output) {
    return false;
  }
  // t0
  output->t0 = input->t0;
  // t1
  output->t1 = input->t1;
  // t2
  output->t2 = input->t2;
  // t3
  output->t3 = input->t3;
  // t4
  output->t4 = input->t4;
  // t5
  output->t5 = input->t5;
  // t6
  output->t6 = input->t6;
  return true;
}

interfaces__msg__MotorCmds *
interfaces__msg__MotorCmds__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces__msg__MotorCmds * msg = (interfaces__msg__MotorCmds *)allocator.allocate(sizeof(interfaces__msg__MotorCmds), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(interfaces__msg__MotorCmds));
  bool success = interfaces__msg__MotorCmds__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
interfaces__msg__MotorCmds__destroy(interfaces__msg__MotorCmds * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    interfaces__msg__MotorCmds__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
interfaces__msg__MotorCmds__Sequence__init(interfaces__msg__MotorCmds__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces__msg__MotorCmds * data = NULL;

  if (size) {
    data = (interfaces__msg__MotorCmds *)allocator.zero_allocate(size, sizeof(interfaces__msg__MotorCmds), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = interfaces__msg__MotorCmds__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        interfaces__msg__MotorCmds__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
interfaces__msg__MotorCmds__Sequence__fini(interfaces__msg__MotorCmds__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      interfaces__msg__MotorCmds__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

interfaces__msg__MotorCmds__Sequence *
interfaces__msg__MotorCmds__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces__msg__MotorCmds__Sequence * array = (interfaces__msg__MotorCmds__Sequence *)allocator.allocate(sizeof(interfaces__msg__MotorCmds__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = interfaces__msg__MotorCmds__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
interfaces__msg__MotorCmds__Sequence__destroy(interfaces__msg__MotorCmds__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    interfaces__msg__MotorCmds__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
interfaces__msg__MotorCmds__Sequence__are_equal(const interfaces__msg__MotorCmds__Sequence * lhs, const interfaces__msg__MotorCmds__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!interfaces__msg__MotorCmds__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
interfaces__msg__MotorCmds__Sequence__copy(
  const interfaces__msg__MotorCmds__Sequence * input,
  interfaces__msg__MotorCmds__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(interfaces__msg__MotorCmds);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    interfaces__msg__MotorCmds * data =
      (interfaces__msg__MotorCmds *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!interfaces__msg__MotorCmds__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          interfaces__msg__MotorCmds__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!interfaces__msg__MotorCmds__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
