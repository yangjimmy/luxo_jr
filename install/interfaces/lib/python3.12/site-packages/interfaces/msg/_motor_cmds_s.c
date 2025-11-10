// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from interfaces:msg/MotorCmds.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "interfaces/msg/detail/motor_cmds__struct.h"
#include "interfaces/msg/detail/motor_cmds__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool interfaces__msg__motor_cmds__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[37];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("interfaces.msg._motor_cmds.MotorCmds", full_classname_dest, 36) == 0);
  }
  interfaces__msg__MotorCmds * ros_message = _ros_message;
  {  // t0
    PyObject * field = PyObject_GetAttrString(_pymsg, "t0");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t0 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // t1
    PyObject * field = PyObject_GetAttrString(_pymsg, "t1");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t1 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // t2
    PyObject * field = PyObject_GetAttrString(_pymsg, "t2");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t2 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // t3
    PyObject * field = PyObject_GetAttrString(_pymsg, "t3");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t3 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // t4
    PyObject * field = PyObject_GetAttrString(_pymsg, "t4");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t4 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // t5
    PyObject * field = PyObject_GetAttrString(_pymsg, "t5");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t5 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // t6
    PyObject * field = PyObject_GetAttrString(_pymsg, "t6");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->t6 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * interfaces__msg__motor_cmds__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of MotorCmds */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("interfaces.msg._motor_cmds");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "MotorCmds");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  interfaces__msg__MotorCmds * ros_message = (interfaces__msg__MotorCmds *)raw_ros_message;
  {  // t0
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t0", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // t1
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t1);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t1", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // t2
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t2);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t2", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // t3
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t3);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t3", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // t4
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t4);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t4", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // t5
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t5);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t5", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // t6
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->t6);
    {
      int rc = PyObject_SetAttrString(_pymessage, "t6", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
