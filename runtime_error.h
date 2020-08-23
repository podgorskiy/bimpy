/*
 * Copyright 2019-2020 Stanislav Pidhorskyi. All rights reserved.
 * License: https://raw.githubusercontent.com/podgorskiy/bimpy/master/LICENSE.txt
 */
#pragma once
#include <stdarg.h>
#include <memory>
#include <string>
#include <exception>
#include <stdexcept>
#include <string.h>


inline std::string string_format(const std::string& fmt_str, va_list ap)
{
	int n = (int)fmt_str.size() * 2;
	std::unique_ptr<char[]> formatted;

	while(true)
	{
		va_list ap_copy;
		va_copy(ap_copy, ap);
		formatted.reset(new char[n]);
		strcpy(&formatted[0], fmt_str.c_str());
		int final_n = vsnprintf(&formatted[0], n, fmt_str.c_str(), ap_copy);
		if (final_n < 0 || final_n >= n)
			n += abs(final_n - n + 1);
		else
			break;
	}
	return std::string(formatted.get());
}

inline std::string string_format(const std::string fmt_str, ...)
{
	va_list ap;
	va_start(ap, fmt_str);
	std::string result = string_format(fmt_str, ap);
	va_end(ap);
	return result;
}

class runtime_error: public std::runtime_error
{
public:
	explicit runtime_error(const std::string fmt_str, ...):
			std::runtime_error(string_format(fmt_str, (va_start(ap, fmt_str), ap)))
	{
		va_end(ap);
	}

	runtime_error(const runtime_error &) = default;
	runtime_error(runtime_error &&) = default;
	~runtime_error() override = default;

private:
	va_list ap;
};
