/*
 * Copyright 2019-2020 Stanislav Pidhorskyi. All rights reserved.
 * License: https://raw.githubusercontent.com/podgorskiy/bimpy/master/LICENSE.txt
 */
#pragma once
#include <runtime_error.h>

#define BIMPY_IMGUI_CONFIG
#define IMGUI_DEFINE_MATH_OPERATORS
#define IM_ASSERT(_EXPR)  bimpy_assert(_EXPR, #_EXPR)
#define IM_ASSERT_USER_ERROR(_EXP,_MSG) bimpy_assert(_EXP, _MSG)

inline void bimpy_assert(bool expr, const char* msg)
{
	if (!expr) { throw runtime_error("imgui assert failed: %s", msg); }
}
