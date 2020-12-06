/*
 * Copyright 2017-2020 Stanislav Pidhorskyi. All rights reserved.
 * License: https://raw.githubusercontent.com/podgorskiy/bimpy/master/LICENSE.txt
 */

#include <imgui.h>
#include <imgui_internal.h>
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include "runtime_error.h"
#include <GL/gl3w.h>
#include <GLFW/glfw3.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <backward.hpp>
#include <memory>
#include <mutex>

#ifndef BIMPY_IMGUI_CONFIG
#error("imgui config is not used")
#endif

namespace py = pybind11;

typedef py::array_t<uint8_t, py::array::c_style> ndarray_uint8;

class Context
{
public:
	Context& operator=(const Context&) = delete;
	Context(const Context&) = delete;
	Context() = default;

	void Init(int width, int height, const std::string& name,
			bool resizable,
			bool visible,
			bool decorated,
			bool focused,
			bool auto_iconify,
			bool floating,
			bool maximized,
			bool transperent,
			bool focus_on_show,
			bool scale_to_monitor,
			bool full_screen);

	void Resize(int width, int height);

	void NewFrame();

	void Render();

	bool ShouldClose();

	int GetWidth() const;

	int GetHeight() const;

	~Context();

	std::array<float, 4> clearColor = {0.1f, 0.1f, 0.1f, 1.0f};

	py::function mouse_button_callback;
	py::function mouse_position_callback;
	py::function keyboard_callback;
private:
	GLFWwindow* m_window = nullptr;
	int m_width;
	int m_height;
	struct ImGuiContext* m_imgui = nullptr;
	std::mutex m_imgui_ctx_mutex;
	backward::SignalHandling m_sh;
};


void Context::Init(int width, int height, const std::string& name,
			bool resizable,
			bool visible,
			bool decorated,
			bool focused,
			bool auto_iconify,
			bool floating,
			bool maximized,
			bool transperent,
			bool focus_on_show,
			bool scale_to_monitor,
			bool full_screen)
{
	if (m_window)
	{
		throw runtime_error(
				"bimpy context was already initialized, can not initialize again. Create a new one and dispose the old one instead.");
	}

	if (!glfwInit())
	{
		throw runtime_error(
				"GLFW initialization failed (glfwInit() failed).\nThis may happen if you try to run bimpy on a headless machine ");
	}

	glfwWindowHint(GLFW_RESIZABLE, (int)resizable);
	glfwWindowHint(GLFW_VISIBLE, (int)visible);
	glfwWindowHint(GLFW_DECORATED, (int)decorated);
	glfwWindowHint(GLFW_FOCUSED, (int)focused);
	glfwWindowHint(GLFW_AUTO_ICONIFY, (int)auto_iconify);
	glfwWindowHint(GLFW_FLOATING, (int)floating);
	glfwWindowHint(GLFW_MAXIMIZED, (int)maximized);
	glfwWindowHint(GLFW_TRANSPARENT_FRAMEBUFFER, (int)transperent);
	glfwWindowHint(GLFW_FOCUS_ON_SHOW, (int)focus_on_show);
	glfwWindowHint(GLFW_SCALE_TO_MONITOR, (int)scale_to_monitor);

#if __APPLE__
	// GL 3.2 + GLSL 150
	const char* glsl_version = "#version 150";
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // Required on Mac
#else
	// GL 3.0 + GLSL 130
	const char* glsl_version = "#version 130";
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
	//glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
	//glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // 3.0+ only
#endif

	m_window = glfwCreateWindow(width, height, name.c_str(), full_screen ? glfwGetPrimaryMonitor() : NULL, NULL);
	if (!m_window)
	{
		glfwTerminate();
		throw runtime_error(
				"GLFW failed to create window (glfwCreateWindow() failed).\nThis may happen if you try to run bimpy on a headless machine ");
	}

	glfwMakeContextCurrent(m_window);
	glfwSwapInterval(1); // vsync

	if (gl3wInit() != GL3W_OK)
	{
		glfwDestroyWindow(m_window);
		m_window = nullptr;
		throw runtime_error(
				"GL3W initialization failed.\nThis may happen if you try to run bimpy on a headless machine");
	}

	m_imgui = ImGui::CreateContext();
	ImGui::SetCurrentContext(m_imgui);

	ImGui_ImplGlfw_InitForOpenGL(m_window, false);
	ImGui_ImplOpenGL3_Init(glsl_version);

	m_width = width;
	m_height = height;

	glfwSetWindowUserPointer(m_window, this);

	glfwSetWindowSizeCallback(m_window, [](GLFWwindow* window, int width, int height)
	{
		Context* ctx = static_cast<Context*>(glfwGetWindowUserPointer(window));
		ctx->Resize(width, height);
	});

	glfwSetKeyCallback(m_window, [](GLFWwindow* window, int key, int, int action, int mods)
	{
		Context* ctx = static_cast<Context*>(glfwGetWindowUserPointer(window));

		ImGuiIO& io = ImGui::GetIO();
		if (action == GLFW_PRESS)
		{
			io.KeysDown[key] = true;
		}
		if (action == GLFW_RELEASE)
		{
			io.KeysDown[key] = false;
		}

		io.KeyCtrl = io.KeysDown[GLFW_KEY_LEFT_CONTROL] || io.KeysDown[GLFW_KEY_RIGHT_CONTROL];
		io.KeyShift = io.KeysDown[GLFW_KEY_LEFT_SHIFT] || io.KeysDown[GLFW_KEY_RIGHT_SHIFT];
		io.KeyAlt = io.KeysDown[GLFW_KEY_LEFT_ALT] || io.KeysDown[GLFW_KEY_RIGHT_ALT];
		io.KeySuper = io.KeysDown[GLFW_KEY_LEFT_SUPER] || io.KeysDown[GLFW_KEY_RIGHT_SUPER];
		if (ctx->keyboard_callback)
		{
			ctx->keyboard_callback(key, action, mods);
		}
	});

	glfwSetCharCallback(m_window, [](GLFWwindow*, unsigned int c)
	{
		ImGuiIO& io = ImGui::GetIO();
		io.AddInputCharacter(c);
	});

	glfwSetScrollCallback(m_window, [](GLFWwindow*, double /*xoffset*/, double yoffset)
	{
		ImGuiIO& io = ImGui::GetIO();
		io.MouseWheel += (float) yoffset * 2.0f;
	});

	glfwSetMouseButtonCallback(m_window, [](GLFWwindow* window, int button, int action, int /*mods*/)
	{
		Context* ctx = static_cast<Context*>(glfwGetWindowUserPointer(window));
		ImGuiIO& io = ImGui::GetIO();

		if (button >= 0 && button < 3)
		{
			io.MouseDown[button] = action == GLFW_PRESS;
		}
		if (ctx->mouse_button_callback)
		{
			double x, y;
			glfwGetCursorPos(window, &x, &y);
			ctx->mouse_button_callback(button, action == GLFW_PRESS, (float)x, (float)y);
		}
	});

	glfwSetCursorPosCallback(m_window, [](GLFWwindow* window, double x, double y)
	{
		Context* ctx = static_cast<Context*>(glfwGetWindowUserPointer(window));
		if (ctx->mouse_position_callback)
		{
			ctx->mouse_position_callback((float)x, (float)y);
		}
	});
}

Context::~Context()
{
	if (m_window)
	{
		glfwSetWindowSizeCallback(m_window, nullptr);
		ImGui::SetCurrentContext(m_imgui);

		ImGui_ImplOpenGL3_Shutdown();
		ImGui_ImplGlfw_Shutdown();
		ImGui::DestroyContext(m_imgui);
		m_imgui = nullptr;

		glfwDestroyWindow(m_window);
		m_window = nullptr;
		glfwTerminate();
	}
}

void Context::Render()
{
	if (!m_window)
	{
		return;
	}

	ImGui::Render();
	glfwMakeContextCurrent(m_window);
	glViewport(0, 0, m_width, m_height);
	glClearColor(clearColor[0], clearColor[1], clearColor[2], clearColor[3]);
	glClear(GL_COLOR_BUFFER_BIT);
	ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
	glfwSwapBuffers(m_window);
	glfwPollEvents();
	m_imgui_ctx_mutex.unlock();
}


void Context::NewFrame()
{
	if (!m_window)
	{
		return;
	}

	m_imgui_ctx_mutex.lock();
	ImGui::SetCurrentContext(m_imgui);
	glfwMakeContextCurrent(m_window);
	ImGui_ImplOpenGL3_NewFrame();
	ImGui_ImplGlfw_NewFrame();
	ImGui::NewFrame();

	// Overwrite default window behaviour
	if (GImGui->WithinFrameScopeWithImplicitWindow)
	{
        GImGui->CurrentWindow->Active = false;
		GImGui->WithinFrameScopeWithImplicitWindow = false;
		ImGui::End();
		GImGui->WithinFrameScopeWithImplicitWindow = true;
		ImGui::SetNextWindowPos(ImVec2(0, 0));
		ImGui::SetNextWindowSize(ImGui::GetIO().DisplaySize);
		ImGui::PushStyleVar(ImGuiStyleVar_WindowRounding, 0);
		ImGui::Begin("Debug##Default2", nullptr, ImGuiWindowFlags_NoDecoration | ImGuiWindowFlags_NoMove);
		ImGui::PopStyleVar();
	}
}


void Context::Resize(int width, int height)
{
	m_width = width;
	m_height = height;
}


bool Context::ShouldClose()
{
	// If there is no window return true to exit a dangling loop
	return m_window ? glfwWindowShouldClose(m_window) != 0 : true;
}

int Context::GetWidth() const
{
	return m_width;
}

int Context::GetHeight() const
{
	return m_height;
}

struct Bool
{
	Bool(): value(false) {}
	Bool(bool v): value(v) {}

	bool value;
	bool null = false;
};

struct Float
{
	Float(): value(0.0f) {}
	Float(float v): value(v) {}

	float value;
};

struct Int
{
	Int(): value(0) {}
	Int(int v): value(v) {}

	int value;
};

struct String
{
	String(): value("") {}
	String(const std::string& v): value(v) {}

	std::string value;
};

class Image
{
public:
	Image& operator=(const Context&) = delete;
	Image(const Context&) = delete;

	Image(ndarray_uint8 ndarray): Image(ndarray.request())
	{}

	~Image()
	{
		glDeleteTextures(1, &m_textureHandle);
	}

	GLuint GetHandle() const
	{
		return m_textureHandle;
	}

	void GrayScaleToAlpha()
	{
		GLint swizzleMask[] = { GL_ONE, GL_ONE, GL_ONE, GL_RED };
		glBindTexture(GL_TEXTURE_2D, m_textureHandle);
		glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_SWIZZLE_RGBA, swizzleMask);
		glBindTexture(GL_TEXTURE_2D, 0);
	}

	ssize_t m_width;
	ssize_t m_height;
private:
	Image(const py::buffer_info& ndarray_info)
	{
		glGenTextures(1, &m_textureHandle);
		glBindTexture(GL_TEXTURE_2D, m_textureHandle);

		m_width = -1;
		m_height = -1;

		GLint backup;
		glGetIntegerv(GL_UNPACK_ALIGNMENT, &backup);
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

		GLint swizzleMask_R[] = { GL_RED, GL_RED, GL_RED, GL_ONE };
		GLint swizzleMask_RG[] = { GL_RED, GL_GREEN, GL_ZERO, GL_ONE };
		GLint swizzleMask_RGB[] = { GL_RED, GL_GREEN, GL_BLUE, GL_ONE };
		GLint swizzleMask_RGBA[] = { GL_RED, GL_GREEN, GL_BLUE, GL_ALPHA };

		if (ndarray_info.ndim == 2)
		{
			m_width = ndarray_info.shape[1];
			m_height = ndarray_info.shape[0];

			glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_SWIZZLE_RGBA, swizzleMask_R);
			glTexImage2D(GL_TEXTURE_2D, 0, GL_R8, m_width, m_height, 0, GL_RED, GL_UNSIGNED_BYTE, ndarray_info.ptr);
		}
		else if (ndarray_info.ndim == 3)
		{
			m_width = ndarray_info.shape[1];
			m_height = ndarray_info.shape[0];

			if (ndarray_info.shape[2] == 1)
			{
				glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_SWIZZLE_RGBA, swizzleMask_R);
				glTexImage2D(GL_TEXTURE_2D, 0, GL_R8, m_width, m_height, 0, GL_RGB, GL_UNSIGNED_BYTE, ndarray_info.ptr);
			}
			else if (ndarray_info.shape[2] == 2)
			{
				glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_SWIZZLE_RGBA, swizzleMask_RG);
				glTexImage2D(GL_TEXTURE_2D, 0, GL_RG8, m_width, m_height, 0, GL_RG, GL_UNSIGNED_BYTE, ndarray_info.ptr);
			}
			else if (ndarray_info.shape[2] == 3)
			{
				glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_SWIZZLE_RGBA, swizzleMask_RGB);
				glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, m_width, m_height, 0, GL_RGB, GL_UNSIGNED_BYTE, ndarray_info.ptr);
			}
			else if (ndarray_info.shape[2] == 4)
			{
				glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_SWIZZLE_RGBA, swizzleMask_RGBA);
				glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, m_width, m_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, ndarray_info.ptr);
			}
			else
			{
				glBindTexture(GL_TEXTURE_2D, 0);
				glPixelStorei(GL_UNPACK_ALIGNMENT, backup);
				throw runtime_error("Wrong number of channels. Should be either 1, 2, 3, or 4, but got %d", (int)ndarray_info.shape[2]);
			}
		}
		else
		{
			glBindTexture(GL_TEXTURE_2D, 0);
			glPixelStorei(GL_UNPACK_ALIGNMENT, backup);
			throw runtime_error("Wrong number of dimensions. Should be either 2 or 3, but got %d", (int)ndarray_info.ndim);
		}
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

		glPixelStorei(GL_UNPACK_ALIGNMENT, backup);
		glBindTexture(GL_TEXTURE_2D, 0);
	}

	GLuint m_textureHandle;
};

std::vector<unsigned short> range_to_list(const ImWchar* r) { std::vector<unsigned short> l; while(*r != 0) { l.push_back(*r); ++r; } return l; }


void  AddLine(const ImVec2& a, const ImVec2& b, ImU32 col, float thickness){ ImGui::GetWindowDrawList()->AddLine(a, b, col, thickness); }
void  AddRect(const ImVec2& a, const ImVec2& b, ImU32 col, float rounding, int rounding_corners_flags, float thickness){ ImGui::GetWindowDrawList()->AddRect(a, b, col, rounding, rounding_corners_flags, thickness); }
void  AddRectFilled(const ImVec2& a, const ImVec2& b, ImU32 col, float rounding, int rounding_corners_flags){ ImGui::GetWindowDrawList()->AddRectFilled(a, b, col, rounding, rounding_corners_flags); }
void  AddRectFilledMultiColor(const ImVec2& a, const ImVec2& b, ImU32 col_upr_left, ImU32 col_upr_right, ImU32 col_bot_right, ImU32 col_bot_lefs){ ImGui::GetWindowDrawList()->AddRectFilledMultiColor(a, b, col_upr_left, col_upr_right, col_bot_right, col_bot_lefs); }
void  AddQuad(const ImVec2& a, const ImVec2& b, const ImVec2& c, const ImVec2& d, ImU32 col, float thickness){ ImGui::GetWindowDrawList()->AddQuad(a, b, c, d, col, thickness); }
void  AddQuadFilled(const ImVec2& a, const ImVec2& b, const ImVec2& c, const ImVec2& d, ImU32 col){ ImGui::GetWindowDrawList()->AddQuadFilled(a, b, c, d, col); }
void  AddTriangle(const ImVec2& a, const ImVec2& b, const ImVec2& c, ImU32 col, float thickness){ ImGui::GetWindowDrawList()->AddTriangle(a, b, c, col, thickness); }
void  AddTriangleFilled(const ImVec2& a, const ImVec2& b, const ImVec2& c, ImU32 col){ ImGui::GetWindowDrawList()->AddTriangleFilled(a, b, c, col); }
void  AddCircle(const ImVec2& centre, float radius, ImU32 col, int num_segments, float thickness){ ImGui::GetWindowDrawList()->AddCircle(centre, radius, col, num_segments, thickness); }
void  AddCircleFilled(const ImVec2& centre, float radius, ImU32 col, int num_segments){ ImGui::GetWindowDrawList()->AddCircleFilled(centre, radius, col, num_segments); }
void  AddBezierCurve(const ImVec2& pos0, const ImVec2& cp0, const ImVec2& cp1, const ImVec2& pos1, ImU32 col, float thickness, int num_segments){ ImGui::GetWindowDrawList()->AddBezierCurve(pos0, cp0, cp1, pos1, col, thickness, num_segments); }

void  PathClear(){ ImGui::GetWindowDrawList()->PathClear(); }
void  PathLineTo(const ImVec2& pos){ ImGui::GetWindowDrawList()->PathLineTo(pos); }
void  PathFillConvex(ImU32 col){ ImGui::GetWindowDrawList()->PathFillConvex(col); }
void  PathStroke(ImU32 col, bool closed, float thickness){ ImGui::GetWindowDrawList()->PathStroke(col, closed, thickness); }


PYBIND11_MODULE(_bimpy, m) {
	static Bool null;
	null.null = true;

	m.doc() = "bimpy - bundled imgui for python";

	py::enum_<ImGuiCond_>(m, "Condition", py::arithmetic())
		.value("Always", ImGuiCond_::ImGuiCond_Always)
		.value("Once", ImGuiCond_::ImGuiCond_Once)
		.value("FirstUseEver", ImGuiCond_::ImGuiCond_FirstUseEver)
		.value("Appearing", ImGuiCond_::ImGuiCond_Appearing)
		.export_values();

	py::enum_<ImGuiWindowFlags_>(m, "WindowFlags", py::arithmetic())
		.value("NoTitleBar", ImGuiWindowFlags_::ImGuiWindowFlags_NoTitleBar)
		.value("NoResize", ImGuiWindowFlags_::ImGuiWindowFlags_NoResize)
		.value("NoMove", ImGuiWindowFlags_::ImGuiWindowFlags_NoMove)
		.value("NoScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollbar)
		.value("NoScrollWithMouse", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollWithMouse)
		.value("NoCollapse", ImGuiWindowFlags_::ImGuiWindowFlags_NoCollapse)
		.value("AlwaysAutoResize", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysAutoResize)
		.value("NoBackground", ImGuiWindowFlags_::ImGuiWindowFlags_NoBackground)
		.value("NoSavedSettings", ImGuiWindowFlags_::ImGuiWindowFlags_NoSavedSettings)
		.value("NoMouseInputs", ImGuiWindowFlags_::ImGuiWindowFlags_NoMouseInputs)
		.value("MenuBar", ImGuiWindowFlags_::ImGuiWindowFlags_MenuBar)
		.value("HorizontalScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_HorizontalScrollbar)
		.value("NoFocusOnAppearing", ImGuiWindowFlags_::ImGuiWindowFlags_NoFocusOnAppearing)
		.value("NoBringToFrontOnFocus", ImGuiWindowFlags_::ImGuiWindowFlags_NoBringToFrontOnFocus)
		.value("AlwaysVerticalScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysVerticalScrollbar)
		.value("AlwaysHorizontalScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysHorizontalScrollbar)
		.value("AlwaysUseWindowPadding", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysUseWindowPadding)
		.value("NoNavInputs", ImGuiWindowFlags_::ImGuiWindowFlags_NoNavInputs)
		.value("NoNavFocus", ImGuiWindowFlags_::ImGuiWindowFlags_NoNavFocus)
		.value("UnsavedDocument", ImGuiWindowFlags_::ImGuiWindowFlags_UnsavedDocument)
		.value("NoNav", ImGuiWindowFlags_::ImGuiWindowFlags_NoNav )
		.value("NoDecoration", ImGuiWindowFlags_::ImGuiWindowFlags_NoDecoration)
		.value("NoInputs", ImGuiWindowFlags_::ImGuiWindowFlags_NoInputs)
		.export_values();

	py::enum_<ImGuiInputTextFlags_>(m, "InputTextFlags", py::arithmetic())
		.value("CharsDecimal", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsDecimal)
		.value("CharsHexadecimal", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsHexadecimal)
		.value("CharsUppercase", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsUppercase)
		.value("CharsNoBlank", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsNoBlank)
		.value("AutoSelectAll", ImGuiInputTextFlags_::ImGuiInputTextFlags_AutoSelectAll)
		.value("EnterReturnsTrue", ImGuiInputTextFlags_::ImGuiInputTextFlags_EnterReturnsTrue)
		//.value("CallbackCompletion", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackCompletion)
		//.value("CallbackHistory", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackHistory)
		//.value("CallbackAlways", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackAlways)
		//.value("CallbackCharFilter", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackCharFilter)
		.value("AllowTabInput", ImGuiInputTextFlags_::ImGuiInputTextFlags_AllowTabInput)
		.value("CtrlEnterForNewLine", ImGuiInputTextFlags_::ImGuiInputTextFlags_CtrlEnterForNewLine)
		.value("NoHorizontalScroll", ImGuiInputTextFlags_::ImGuiInputTextFlags_NoHorizontalScroll)
		.value("AlwaysInsertMode", ImGuiInputTextFlags_::ImGuiInputTextFlags_AlwaysInsertMode)
		.value("ReadOnly", ImGuiInputTextFlags_::ImGuiInputTextFlags_ReadOnly)
		.value("Password", ImGuiInputTextFlags_::ImGuiInputTextFlags_Password)
		//.value("NoUndoRedo", ImGuiInputTextFlags_::ImGuiInputTextFlags_NoUndoRedo)
		.value("Multiline", ImGuiInputTextFlags_::ImGuiInputTextFlags_Multiline)
		.export_values();

	py::enum_<ImGuiDir_>(m, "Direction")
		.value("None", ImGuiDir_::ImGuiDir_None)
		.value("Left", ImGuiDir_::ImGuiDir_Left)
		.value("Right", ImGuiDir_::ImGuiDir_Right)
		.value("Up", ImGuiDir_::ImGuiDir_Up)
		.value("Down", ImGuiDir_::ImGuiDir_Down);

	py::enum_<ImGuiCol_>(m, "Colors")
		.value("Text", ImGuiCol_::ImGuiCol_Text)
		.value("TextDisabled", ImGuiCol_::ImGuiCol_TextDisabled)
		.value("WindowBg", ImGuiCol_::ImGuiCol_WindowBg)
		.value("ChildBg", ImGuiCol_::ImGuiCol_ChildBg)
		.value("PopupBg", ImGuiCol_::ImGuiCol_PopupBg)
		.value("Border", ImGuiCol_::ImGuiCol_Border)
		.value("BorderShadow", ImGuiCol_::ImGuiCol_BorderShadow)
		.value("FrameBg", ImGuiCol_::ImGuiCol_FrameBg)
		.value("FrameBgHovered", ImGuiCol_::ImGuiCol_FrameBgHovered)
		.value("FrameBgActive", ImGuiCol_::ImGuiCol_FrameBgActive)
		.value("TitleBg", ImGuiCol_::ImGuiCol_TitleBg)
		.value("TitleBgActive", ImGuiCol_::ImGuiCol_TitleBgActive)
		.value("TitleBgCollapsed", ImGuiCol_::ImGuiCol_TitleBgCollapsed)
		.value("MenuBarBg", ImGuiCol_::ImGuiCol_MenuBarBg)
		.value("ScrollbarBg", ImGuiCol_::ImGuiCol_ScrollbarBg)
		.value("ScrollbarGrab", ImGuiCol_::ImGuiCol_ScrollbarGrab)
		.value("ScrollbarGrabHovered", ImGuiCol_::ImGuiCol_ScrollbarGrabHovered)
		.value("ScrollbarGrabActive", ImGuiCol_::ImGuiCol_ScrollbarGrabActive)
		.value("CheckMark", ImGuiCol_::ImGuiCol_CheckMark)
		.value("SliderGrab", ImGuiCol_::ImGuiCol_SliderGrab)
		.value("SliderGrabActive", ImGuiCol_::ImGuiCol_SliderGrabActive)
		.value("Button", ImGuiCol_::ImGuiCol_Button)
		.value("ButtonHovered", ImGuiCol_::ImGuiCol_ButtonHovered)
		.value("ButtonActive", ImGuiCol_::ImGuiCol_ButtonActive)
		.value("Header", ImGuiCol_::ImGuiCol_Header)
		.value("HeaderHovered", ImGuiCol_::ImGuiCol_HeaderHovered)
		.value("HeaderActive", ImGuiCol_::ImGuiCol_HeaderActive)
		.value("Separator", ImGuiCol_::ImGuiCol_Separator)
		.value("SeparatorHovered", ImGuiCol_::ImGuiCol_SeparatorHovered)
		.value("SeparatorActive", ImGuiCol_::ImGuiCol_SeparatorActive)
		.value("ResizeGrip", ImGuiCol_::ImGuiCol_ResizeGrip)
		.value("ResizeGripHovered", ImGuiCol_::ImGuiCol_ResizeGripHovered)
		.value("ResizeGripActive", ImGuiCol_::ImGuiCol_ResizeGripActive)
		.value("Tab", ImGuiCol_::ImGuiCol_Tab)
		.value("TabHovered", ImGuiCol_::ImGuiCol_TabHovered)
		.value("TabActive", ImGuiCol_::ImGuiCol_TabActive)
		.value("TabUnfocused", ImGuiCol_::ImGuiCol_TabUnfocused)
		.value("TabUnfocusedActive", ImGuiCol_::ImGuiCol_TabUnfocusedActive)
		.value("PlotLines", ImGuiCol_::ImGuiCol_PlotLines)
		.value("PlotLinesHovered", ImGuiCol_::ImGuiCol_PlotLinesHovered)
		.value("PlotHistogram", ImGuiCol_::ImGuiCol_PlotHistogram)
		.value("PlotHistogramHovered", ImGuiCol_::ImGuiCol_PlotHistogramHovered)
		.value("TextSelectedBg", ImGuiCol_::ImGuiCol_TextSelectedBg)
		.value("DragDropTarget", ImGuiCol_::ImGuiCol_DragDropTarget)
		.value("NavHighlight", ImGuiCol_::ImGuiCol_NavHighlight)
		.value("NavWindowingHighlight", ImGuiCol_::ImGuiCol_NavWindowingHighlight)
		.value("NavWindowingDimBg", ImGuiCol_::ImGuiCol_NavWindowingDimBg)
		.value("ModalWindowDimBg", ImGuiCol_::ImGuiCol_ModalWindowDimBg)
		// Obsolete names (will be removed)
		.value("ChildWindowBg", ImGuiCol_::ImGuiCol_ChildBg)
		.value("ModalWindowDarkening", ImGuiCol_::ImGuiCol_ModalWindowDimBg)
		.export_values();

	py::enum_<ImGuiStyleVar_>(m, "Style", py::arithmetic())
		.value("Alpha", ImGuiStyleVar_::ImGuiStyleVar_Alpha)
		.value("WindowPadding", ImGuiStyleVar_::ImGuiStyleVar_WindowPadding)
		.value("WindowRounding", ImGuiStyleVar_::ImGuiStyleVar_WindowRounding)
		.value("WindowBorderSize", ImGuiStyleVar_::ImGuiStyleVar_WindowBorderSize)
		.value("WindowMinSize", ImGuiStyleVar_::ImGuiStyleVar_WindowMinSize)
		.value("WindowTitleAlign", ImGuiStyleVar_::ImGuiStyleVar_WindowTitleAlign)
		.value("ChildRounding", ImGuiStyleVar_::ImGuiStyleVar_ChildRounding)
		.value("ChildBorderSize", ImGuiStyleVar_::ImGuiStyleVar_ChildBorderSize)
		.value("PopupRounding", ImGuiStyleVar_::ImGuiStyleVar_PopupRounding)
		.value("PopupBorderSize", ImGuiStyleVar_::ImGuiStyleVar_PopupBorderSize)
		.value("FramePadding", ImGuiStyleVar_::ImGuiStyleVar_FramePadding)
		.value("FrameRounding", ImGuiStyleVar_::ImGuiStyleVar_FrameRounding)
		.value("FrameBorderSize", ImGuiStyleVar_::ImGuiStyleVar_FrameBorderSize)
		.value("ItemSpacing", ImGuiStyleVar_::ImGuiStyleVar_ItemSpacing)
		.value("ItemInnerSpacing", ImGuiStyleVar_::ImGuiStyleVar_ItemInnerSpacing)
		.value("IndentSpacing", ImGuiStyleVar_::ImGuiStyleVar_IndentSpacing)
		.value("ScrollbarSize", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarSize)
		.value("ScrollbarRounding", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarRounding)
		.value("GrabMinSize", ImGuiStyleVar_::ImGuiStyleVar_GrabMinSize)
		.value("GrabRounding", ImGuiStyleVar_::ImGuiStyleVar_GrabRounding)
		.value("TabRounding", ImGuiStyleVar_::ImGuiStyleVar_TabRounding)
		.value("ButtonTextAlign", ImGuiStyleVar_::ImGuiStyleVar_ButtonTextAlign)
		.value("SelectableTextAlign", ImGuiStyleVar_::ImGuiStyleVar_SelectableTextAlign)
		.export_values();

	py::enum_<ImGuiFocusedFlags_>(m, "FocusedFlags", py::arithmetic())
		.value("None", ImGuiFocusedFlags_None)
		.value("ChildWindows", ImGuiFocusedFlags_ChildWindows)
		.value("RootWindow", ImGuiFocusedFlags_RootWindow)
		.value("AnyWindow", ImGuiFocusedFlags_AnyWindow)
		.value("RootAndChildWindows", ImGuiFocusedFlags_RootAndChildWindows)
		.export_values();

	py::enum_<ImGuiHoveredFlags_>(m, "HoveredFlags", py::arithmetic())
		.value("None", ImGuiHoveredFlags_None)
		.value("ChildWindows", ImGuiHoveredFlags_ChildWindows)
		.value("RootWindow", ImGuiHoveredFlags_RootWindow)
		.value("AnyWindow", ImGuiHoveredFlags_AnyWindow)
		.value("AllowWhenBlockedByPopup", ImGuiHoveredFlags_AllowWhenBlockedByPopup)
		.value("AllowWhenBlockedByActiveItem", ImGuiHoveredFlags_AllowWhenBlockedByActiveItem)
		.value("AllowWhenOverlapped", ImGuiHoveredFlags_AllowWhenOverlapped)
		.value("AllowWhenDisabled", ImGuiHoveredFlags_AllowWhenDisabled)
		.value("RectOnly", ImGuiHoveredFlags_RectOnly)
		.export_values();

	py::enum_<ImGuiTreeNodeFlags_>(m, "TreeNodeFlags", py::arithmetic())
		.value("None", ImGuiTreeNodeFlags_None)
		.value("Selected", ImGuiTreeNodeFlags_Selected)
		.value("Framed", ImGuiTreeNodeFlags_Framed)
		.value("AllowItemOverlap", ImGuiTreeNodeFlags_AllowItemOverlap)
		.value("NoTreePushOnOpen", ImGuiTreeNodeFlags_NoTreePushOnOpen)
		.value("NoAutoOpenOnLog", ImGuiTreeNodeFlags_NoAutoOpenOnLog)
		.value("DefaultOpen", ImGuiTreeNodeFlags_DefaultOpen)
		.value("OpenOnDoubleClick", ImGuiTreeNodeFlags_OpenOnDoubleClick)
		.value("OpenOnArrow", ImGuiTreeNodeFlags_OpenOnArrow)
		.value("Leaf", ImGuiTreeNodeFlags_Leaf)
		.value("Bullet", ImGuiTreeNodeFlags_Bullet)
		.value("FramePadding", ImGuiTreeNodeFlags_FramePadding)
		.value("NavLeftJumpsBackHere", ImGuiTreeNodeFlags_NavLeftJumpsBackHere)
		.value("CollapsingHeader", ImGuiTreeNodeFlags_CollapsingHeader)
		.export_values();


	/*
	 * int width, int height, const std::string& name,
			bool resizable,
			bool visible,
			bool decorated,
			bool focused,
			bool auto_iconify,
			bool floating,
			bool maximized,
			bool transperent,
			bool focus_on_show,
			bool scale_to_monitor,
			bool full_screen)
	 */
	py::class_<Context>(m, "Context")
		.def(py::init())
		.def("init", &Context::Init, "Initializes context and creates window",
				py::arg("width"), py::arg("height"), py::arg("name"),
				py::arg("resizable") = true,
				py::arg("visible") = true,
				py::arg("decorated") = true,
				py::arg("focused") = true,
				py::arg("auto_iconify") = true,
				py::arg("floating") = false,
				py::arg("maximized") = false,
				py::arg("transperent") = false,
				py::arg("focus_on_show") = true,
				py::arg("scale_to_monitor") = false,
				py::arg("full_screen") = false
		)
		.def("new_frame", &Context::NewFrame, "Starts a new frame. NewFrame must be called before any imgui functions")
		.def("render", &Context::Render, "Finalizes the frame and draws all UI. Render must be called after all imgui functions")
		.def("should_close", &Context::ShouldClose)

		.def_property_readonly("width", &Context::GetWidth)
		.def_property_readonly("height", &Context::GetHeight)

		.def_readwrite("mouse_button_callback", &Context::mouse_button_callback)
		.def_readwrite("mouse_position_callback", &Context::mouse_position_callback)
		.def_readwrite("keyboard_callback", &Context::keyboard_callback)

		.def_readwrite("clear_color", &Context::clearColor)
		.def("__enter__", &Context::NewFrame)
		.def("__exit__", [](Context& self, py::object, py::object, py::object)
			{
				self.Render();
			});

	py::enum_<ImDrawCornerFlags_>(m, "Corner")
		.value("TopLeft", ImDrawCornerFlags_TopLeft)
		.value("TopRight", ImDrawCornerFlags_TopRight)
		.value("BotRight", ImDrawCornerFlags_BotRight)
		.value("BotLeft", ImDrawCornerFlags_BotLeft)
		.value("All", ImDrawCornerFlags_All)
		.export_values();

	py::class_<Bool>(m, "Bool")
		.def(py::init())
		.def(py::init<bool>())
		.def_readwrite("value", &Bool::value);

	py::class_<Float>(m, "Float")
		.def(py::init())
		.def(py::init<float>())
		.def_readwrite("value", &Float::value);

	py::class_<Int>(m, "Int")
		.def(py::init())
		.def(py::init<int>())
		.def_readwrite("value", &Int::value);

	py::class_<String>(m, "String")
		.def(py::init())
		.def(py::init<std::string>())
		.def_readwrite("value", &String::value);

	py::class_<ImVec2>(m, "Vec2")
		.def(py::init())
		.def(py::init<float, float>())
		.def_readwrite("x", &ImVec2::x)
		.def_readwrite("y", &ImVec2::y)
		.def(py::self * float())
		.def(py::self / float())
		.def(py::self + py::self)
		.def(py::self - py::self)
		.def(py::self * py::self)
		.def(py::self / py::self)
		.def(py::self += py::self)
		.def(py::self -= py::self)
		.def(py::self *= float())
		.def(py::self /= float())
		.def("__mul__", [](float b, const ImVec2 &a) {
			return a * b;
		}, py::is_operator());

	py::class_<ImVec4>(m, "Vec4")
		.def(py::init())
		.def(py::init<float, float, float, float>())
		.def_readwrite("x", &ImVec4::x)
		.def_readwrite("y", &ImVec4::y)
		.def_readwrite("z", &ImVec4::z)
		.def_readwrite("w", &ImVec4::w)
		.def(py::self + py::self)
		.def(py::self - py::self)
		.def("__mul__", [](const ImVec4 &a, float b) {
			return ImVec4(a.x * b, a.y * b, a.z * b, a.w * b);
		}, py::is_operator())
		.def("__rmul__", [](const ImVec4 &a, float b) {
			return ImVec4(a.x * b, a.y * b, a.z * b, a.w * b);
		}, py::is_operator());

	py::class_<Image>(m, "Image")
			.def(py::init<ndarray_uint8>(), "Constructs Image object from ndarray, PIL Image, numpy array, etc.")
			.def("grayscale_to_alpha", &Image::GrayScaleToAlpha, "For grayscale images, uses values as alpha")
			.def_readonly("width", &Image::m_width)
			.def_readonly("height", &Image::m_height);

	py::class_<ImGuiStyle>(m, "GuiStyle")
		.def(py::init())
			.def_readwrite("alpha", &ImGuiStyle::Alpha)
			.def_readwrite("window_padding", &ImGuiStyle::WindowPadding)
			.def_readwrite("window_rounding", &ImGuiStyle::WindowRounding)
			.def_readwrite("window_border_size", &ImGuiStyle::WindowBorderSize)
			.def_readwrite("window_min_size", &ImGuiStyle::WindowMinSize)
			.def_readwrite("window_title_align", &ImGuiStyle::WindowTitleAlign)
			.def_readwrite("window_menu_button_position", &ImGuiStyle::WindowMenuButtonPosition)
			.def_readwrite("child_rounding", &ImGuiStyle::ChildRounding)
			.def_readwrite("child_border_size", &ImGuiStyle::ChildBorderSize)
			.def_readwrite("popup_rounding", &ImGuiStyle::PopupRounding)
			.def_readwrite("popup_border_size", &ImGuiStyle::PopupBorderSize)
			.def_readwrite("frame_padding", &ImGuiStyle::FramePadding)
			.def_readwrite("frame_rounding", &ImGuiStyle::FrameRounding)
			.def_readwrite("frame_border_size", &ImGuiStyle::FrameBorderSize)
			.def_readwrite("item_spacing", &ImGuiStyle::ItemSpacing)
			.def_readwrite("item_inner_spacing", &ImGuiStyle::ItemInnerSpacing)
			.def_readwrite("touch_extra_spacing", &ImGuiStyle::TouchExtraPadding)
			.def_readwrite("indent_spacing", &ImGuiStyle::IndentSpacing)
			.def_readwrite("columns_min_spacing", &ImGuiStyle::ColumnsMinSpacing)
			.def_readwrite("scroll_bar_size", &ImGuiStyle::ScrollbarSize)
			.def_readwrite("scroll_bar_rounding", &ImGuiStyle::ScrollbarRounding)
			.def_readwrite("grab_min_size", &ImGuiStyle::GrabMinSize)
			.def_readwrite("grab_rounding", &ImGuiStyle::GrabRounding)
			.def_readwrite("tab_rounding", &ImGuiStyle::TabRounding)
			.def_readwrite("tab_border_size", &ImGuiStyle::TabBorderSize)
			.def_readwrite("color_button_position", &ImGuiStyle::ColorButtonPosition)
			.def_readwrite("button_text_align", &ImGuiStyle::ButtonTextAlign)
			.def_readwrite("selectable_text_align", &ImGuiStyle::SelectableTextAlign)
			.def_readwrite("display_window_padding", &ImGuiStyle::DisplayWindowPadding)
			.def_readwrite("display_safe_area_padding", &ImGuiStyle::DisplaySafeAreaPadding)
			.def_readwrite("mouse_cursor_scale", &ImGuiStyle::MouseCursorScale)
			.def_readwrite("anti_aliased_lines", &ImGuiStyle::AntiAliasedLines)
			.def_readwrite("anti_aliased_fill", &ImGuiStyle::AntiAliasedFill)
			.def_readwrite("curve_tessellation_tol", &ImGuiStyle::CurveTessellationTol)
		.def("get_color",[](ImGuiStyle& self, ImGuiCol_ a)
			{
				return self.Colors[(int)a];
			})
		.def("set_color",[](ImGuiStyle& self, ImGuiCol_ a, ImVec4 c)
			{
				self.Colors[(int)a] = c;
			});

	py::class_<ImGuiIO>(m, "IO")
		.def(py::init())
			.def_readonly("display_size", &ImGuiIO::DisplaySize)
			.def_readonly("delta_time", &ImGuiIO::DeltaTime)
			.def_readwrite("font_global_scale", &ImGuiIO::FontGlobalScale)
			.def_readonly("backend_platform_name", &ImGuiIO::BackendPlatformName)
			.def_readonly("backend_render_name", &ImGuiIO::BackendRendererName)
			.def_readonly("mouse_pos", &ImGuiIO::MousePos)
			.def_readonly("mouse_down", &ImGuiIO::MouseDown)
			.def_readonly("mouse_wheel", &ImGuiIO::MouseWheel)
			.def_readonly("mouse_wheel", &ImGuiIO::MouseWheel)
			;

	m.def("getio", [](){ return &ImGui::GetIO(); }, py::return_value_policy::reference);

	m.def("get_style", &ImGui::GetStyle);
	m.def("set_style", [](const ImGuiStyle& a)
		{
			ImGui::GetStyle() = a;
		});

	m.def("style_colors_classic", []()
		{
			ImGui::StyleColorsClassic();
		});
	m.def("style_colors_dark", []()
		{
			ImGui::StyleColorsDark();
		});
	m.def("style_colors_light", []()
		{
			ImGui::StyleColorsLight();
		});

	m.def("show_demo_window", [](){ ImGui::ShowDemoWindow(); }, "create demo/test window (previously called ShowTestWindow). demonstrate most ImGui features.");
	m.def("show_about_window", [](){ ImGui::ShowAboutWindow(); }, "create About window. display Dear ImGui version, credits and build/system information.");
	m.def("show_metrics_window", [](){ ImGui::ShowMetricsWindow(); }, "create metrics window. display ImGui internals: draw commands (with individual draw calls and vertices), window list, basic internal state, etc.");
	m.def("show_style_editor", [](){ ImGui::ShowStyleEditor(); }, "add style editor block (not a window). you can pass in a reference ImGuiStyle structure to compare to, revert to and save to (else it uses the default style)");
	m.def("show_style_selector", [](const char* label){ ImGui::ShowStyleSelector(label); }, "add style selector block (not a window), essentially a combo listing the default styles.");
	m.def("show_font_selector", [](const char* label){ ImGui::ShowFontSelector(label); }, "add font selector block (not a window), essentially a combo listing the loaded fonts.");
	m.def("show_user_guide", [](){ ImGui::ShowUserGuide(); }, "add basic help/info block (not a window): how to manipulate ImGui as a end-user (mouse/keyboard controls).");


	m.def("begin",[](const std::string& name, Bool& opened, ImGuiWindowFlags flags) -> bool
		{
			return ImGui::Begin(name.c_str(), opened.null ? nullptr : &opened.value, flags);
		},
		"Push a new ImGui window to add widgets to",
		py::arg("name"), py::arg("opened") = null, py::arg("flags") = ImGuiWindowFlags_(0));

	m.def("end", &ImGui::End);

	m.def("begin_child",[](const std::string& str_id, const ImVec2& size, bool border, ImGuiWindowFlags extra_flags) -> bool
		{
			return ImGui::BeginChild(str_id.c_str(), size, border);
		},
		"begin a scrolling region. size==0.0f: use remaining window size, size<0.0f: use remaining window size minus abs(size). size>0.0f: fixed size. each axis can use a different mode, e.g. ImVec2(0,400).",
		py::arg("str_id"), py::arg("size") = ImVec2(0,0), py::arg("border") = false, py::arg("extra_flags") = ImGuiWindowFlags_(0));

	m.def("end_child", &ImGui::EndChild);

	m.def("begin_main_menu_bar", &ImGui::BeginMainMenuBar, "create and append to a full screen menu-bar. only call EndMainMenuBar() if this returns true!");
	m.def("end_main_menu_bar", &ImGui::EndMainMenuBar);
	m.def("begin_menu_bar", &ImGui::BeginMenuBar, "append to menu-bar of current window (requires ImGuiWindowFlags_MenuBar flag set on parent window). only call EndMenuBar() if this returns true!");
	m.def("end_menu_bar", &ImGui::EndMenuBar);
	m.def("begin_menu",[](const std::string& name, Bool& enabled) -> bool
		{
			return ImGui::BeginMenu(name.c_str(), (bool *) (enabled.null ? nullptr : &enabled.value));
		},
		"create a sub-menu entry. only call EndMenu() if this returns true!",
		py::arg("name"), py::arg("enabled") = Bool(true));
	m.def("menu_item",[](const std::string& label, const std::string& shortcut, Bool& selected, bool enabled) -> bool
		{
			return ImGui::MenuItem(label.c_str(), shortcut.c_str(), selected.null ? nullptr : &selected.value, enabled);
		},
		"return true when activated + toggle (*p_selected) if p_selected != NULL",
		py::arg("name"), py::arg("shortcut"), py::arg("selected") = Bool(false), py::arg("enabled") = true);
	m.def("end_menu", &ImGui::EndMenu);

	m.def("begin_tooltip", &ImGui::BeginTooltip);
	m.def("end_tooltip", &ImGui::EndTooltip);
	m.def("set_tooltip", [](const char* text){ ImGui::SetTooltip("%s", text); });


	m.def("open_popup", [](std::string str_id)
		{
			ImGui::OpenPopup(str_id.c_str());
		},
		"call to mark popup as open (don't call every frame!). popups are closed when user click outside, or if CloseCurrentPopup() is called within a BeginPopup()/EndPopup() block. By default, Selectable()/MenuItem() are calling CloseCurrentPopup(). Popup identifiers are relative to the current ID-stack (so OpenPopup and BeginPopup needs to be at the same level)."
	);
	m.def("open_popup_on_item_click", [](std::string str_id = "", int mouse_button = 1)
		{
			ImGui::OpenPopupOnItemClick(str_id.c_str(), mouse_button);
		},
		"helper to open popup when clicked on last item. return true when just opened."
	);
	m.def("begin_popup", [](std::string str_id, ImGuiWindowFlags flags)->bool
		{
			return ImGui::BeginPopup(str_id.c_str(), flags);
		},
		"",
          py::arg("name"), py::arg("flags") = ImGuiWindowFlags_(0)
	);
	m.def("begin_popup_modal", [](std::string name = "")->bool
		{
			return ImGui::BeginPopupModal(name.c_str());
		},
		""
	);

	// add more arguments later:
	m.def("begin_popup_context_item", []()
		{
			ImGui::BeginPopupContextItem();
		},
		"helper to open and begin popup when clicked on last item. if you can pass a NULL str_id only if the previous item had an id. If you want to use that on a non-interactive item such as Text() you need to pass in an explicit ID here."
	);
	m.def("begin_popup_context_window", []()
		{
			ImGui::BeginPopupContextWindow();
		},
		"helper to open and begin popup when clicked on current window."
	);
	m.def("begin_popup_context_void", []()
		{
			ImGui::BeginPopupContextVoid();
		},
		"helper to open and begin popup when clicked in void (where there are no imgui windows)."
	);

	m.def("end_popup", &ImGui::EndPopup);
	m.def("is_popup_open", [](std::string str_id = "")->bool
		{
			return ImGui::IsPopupOpen(str_id.c_str());
		},
		""
	);
	m.def("close_current_popup", &ImGui::CloseCurrentPopup);

	m.def("get_content_region_max", &ImGui::GetContentRegionMax);
	m.def("get_content_region_avail", &ImGui::GetContentRegionAvail);
    // OBSOLETED in 1.70 (from May 2019)
	m.def("get_content_region_avail_width", &ImGui::GetContentRegionAvailWidth);
	m.def("get_window_content_region_min", &ImGui::GetWindowContentRegionMin);
	m.def("get_window_content_region_max", &ImGui::GetWindowContentRegionMax);
	m.def("get_window_content_region_width", &ImGui::GetWindowContentRegionWidth);
	m.def("get_font_size", &ImGui::GetFontSize);
	m.def("set_window_font_scale", &ImGui::SetWindowFontScale);
	m.def("get_window_pos", &ImGui::GetWindowPos);
	m.def("get_window_size", &ImGui::GetWindowSize);
	m.def("get_window_width", &ImGui::GetWindowWidth);
	m.def("get_window_height", &ImGui::GetWindowHeight);
	m.def("is_window_collapsed", &ImGui::IsWindowCollapsed);
	m.def("is_window_appearing", &ImGui::IsWindowAppearing);
	m.def("is_window_focused", &ImGui::IsWindowFocused);
	m.def("is_window_hovered", &ImGui::IsWindowHovered);

	m.def("set_window_font_scale", &ImGui::SetWindowFontScale);

	m.def("set_next_window_pos", &ImGui::SetNextWindowPos, py::arg("pos"), py::arg("cond") = 0, py::arg("pivot") = ImVec2(0,0));
	m.def("set_next_window_size", &ImGui::SetNextWindowSize, py::arg("size"), py::arg("cond") = 0);
	m.def("set_next_window_size_constraints", [](const ImVec2& size_min, const ImVec2& size_max){ ImGui::SetNextWindowSizeConstraints(size_min, size_max); }, py::arg("size_min"), py::arg("size_max") = 0);
	m.def("set_next_window_content_size", &ImGui::SetNextWindowContentSize, py::arg("size"));
	m.def("set_next_window_collapsed", &ImGui::SetNextWindowCollapsed, py::arg("collapsed"), py::arg("cond") = 0);
	m.def("set_next_window_focus", &ImGui::SetNextWindowFocus);
	m.def("set_next_window_bg_alpha", &ImGui::SetNextWindowBgAlpha, py::arg("alpha"));
	m.def("set_window_pos", [](const char* name, const ImVec2& pos, ImGuiCond cond){ ImGui::SetWindowPos(name, pos, cond); }, py::arg("name"), py::arg("pos"), py::arg("cond") = 0);
	m.def("set_window_size", [](const char* name, const ImVec2& size, ImGuiCond cond){ ImGui::SetWindowSize(name, size, cond); }, py::arg("name"), py::arg("size"), py::arg("cond") = 0);
	m.def("set_window_collapsed", [](const char* name, bool collapsed, ImGuiCond cond){ ImGui::SetWindowCollapsed(name, collapsed, cond); }, py::arg("name"), py::arg("collapsed"), py::arg("cond") = 0);
	m.def("set_window_focus", [](const char* name){ ImGui::SetWindowFocus(name); }, py::arg("name"));

	m.def("get_scroll_x", &ImGui::GetScrollX);
	m.def("get_scroll_y", &ImGui::GetScrollY);
	m.def("get_scroll_max_x", &ImGui::GetScrollMaxX);
	m.def("get_scroll_max_y", &ImGui::GetScrollMaxY);
	m.def("set_scroll_x", [](float scroll_x) { ImGui::SetScrollX(scroll_x); }, py::arg("scroll_x"));
	m.def("set_scroll_y", [](float scroll_y) { ImGui::SetScrollY(scroll_y); }, py::arg("scroll_y"));
    // OBSOLETED in 1.66 (from Sep 2018)
	m.def("set_scroll_here", &ImGui::SetScrollHere, py::arg("center_y_ratio") = 0.5f);
	m.def("set_scroll_here_x", &ImGui::SetScrollHereX, py::arg("center_x_ratio") = 0.5f);
	m.def("set_scroll_here_y", &ImGui::SetScrollHereY, py::arg("center_y_ratio") = 0.5f);
	m.def("set_scroll_from_pos_x", [](float pos_x, float center_x_ratio) { ImGui::SetScrollFromPosX(pos_x, center_x_ratio); }, py::arg("pos_x"), py::arg("center_x_ratio") = 0.5f);
	m.def("set_scroll_from_pos_y", [](float pos_y, float center_y_ratio) { ImGui::SetScrollFromPosY(pos_y, center_y_ratio); }, py::arg("pos_y"), py::arg("center_y_ratio") = 0.5f);
	m.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere, py::arg("offset") = 0.0f);

	m.def("push_style_color", [](ImGuiCol_ idx, const ImVec4& col){ ImGui::PushStyleColor((ImGuiCol)idx, col); });
	m.def("pop_style_color", &ImGui::PopStyleColor, py::arg("count") = 1);

	m.def("push_style_var", [](ImGuiStyleVar_ idx, float val){ ImGui::PushStyleVar((ImGuiStyleVar)idx, val); });
	m.def("push_style_var", [](ImGuiStyleVar_ idx, ImVec2 val){ ImGui::PushStyleVar((ImGuiStyleVar)idx, val); });
	m.def("pop_style_var", &ImGui::PopStyleVar, py::arg("count") = 1);

	m.def("push_item_width", &ImGui::PushItemWidth);
	m.def("pop_item_width", &ImGui::PopItemWidth);
	m.def("set_next_item_width", &ImGui::SetNextItemWidth);
	m.def("calc_item_width", &ImGui::CalcItemWidth);
	m.def("calc_text_size", &ImGui::CalcTextSize, py::arg("text"), py::arg("text_end") = nullptr, py::arg("hide_text_after_double_hash") = false, py::arg("wrap_width") = 0.0f);
	m.def("push_text_wrap_pos", &ImGui::PushTextWrapPos, py::arg("wrap_pos_x") = 0.0f);
	m.def("pop_text_wrap_pos", &ImGui::PopTextWrapPos);
	m.def("push_allow_keyboard_focus", &ImGui::PushAllowKeyboardFocus);
	m.def("pop_allow_keyboard_focus", &ImGui::PopAllowKeyboardFocus);
	m.def("push_button_repeat", &ImGui::PushButtonRepeat);
	m.def("pop_button_repeat", &ImGui::PopButtonRepeat);


	m.def("separator", &ImGui::Separator);
	m.def("same_line", &ImGui::SameLine, py::arg("local_pos_x") = 0.0f, py::arg("spacing_w") = -1.0f);
	m.def("new_line", &ImGui::NewLine);
	m.def("spacing", &ImGui::Spacing);
	m.def("dummy", &ImGui::Dummy);
	m.def("indent", &ImGui::Indent, py::arg("indent_w") = 0.0f);
	m.def("unindent", &ImGui::Unindent, py::arg("indent_w") = 0.0f);
	m.def("begin_group", &ImGui::BeginGroup);
	m.def("end_group", &ImGui::EndGroup);
	m.def("get_cursor_pos", &ImGui::GetCursorPos);
	m.def("get_cursor_pos_x", &ImGui::GetCursorPosX);
	m.def("get_cursor_pos_y", &ImGui::GetCursorPosY);
	m.def("set_cursor_pos", &ImGui::SetCursorPos);
	m.def("set_cursor_pos_x", &ImGui::SetCursorPosX);
	m.def("set_cursor_pos_y", &ImGui::SetCursorPosY);
	m.def("get_cursor_start_pos", &ImGui::GetCursorStartPos);
	m.def("get_cursor_screen_pos", &ImGui::GetCursorScreenPos);
	m.def("set_cursor_screen_pos", &ImGui::SetCursorScreenPos);
	m.def("align_text_to_frame_padding", &ImGui::AlignTextToFramePadding);
	m.def("get_text_line_height", &ImGui::GetTextLineHeight);
	m.def("get_text_line_height_with_spacing", &ImGui::GetTextLineHeightWithSpacing);
	m.def("get_frame_height", &ImGui::GetFrameHeight);
	m.def("get_frame_height_with_spacing", &ImGui::GetFrameHeightWithSpacing);

	m.def("columns", &ImGui::Columns, py::arg("count") = 1, py::arg("id") = nullptr, py::arg("border") = true);
	m.def("next_column", &ImGui::NextColumn);
	m.def("get_column_index", &ImGui::GetColumnIndex);
	m.def("get_column_offset", &ImGui::GetColumnOffset, py::arg("column_index") = -1);
	m.def("set_column_offset", &ImGui::SetColumnOffset, py::arg("column_index"), py::arg("offset_x"));
	m.def("get_column_width", &ImGui::GetColumnWidth, py::arg("column_index") = -1);
    m.def("set_column_width", &ImGui::SetColumnWidth, py::arg("column_index"), py::arg("column_width"));
	m.def("get_columns_count", &ImGui::GetColumnsCount);

	m.def("begin_tab_bar", &ImGui::BeginTabBar, py::arg("str_id"), py::arg("flags") = 0);
	m.def("end_tab_bar", &ImGui::EndTabBar);
	m.def("begin_tab_item",[](const std::string& label, Bool& opened, ImGuiTabItemFlags flags) -> bool
		{
			return ImGui::BeginTabItem(label.c_str(), opened.null ? nullptr : &opened.value, flags);
		},
		"create a Tab. Returns true if the Tab is selected.",
		py::arg("label"), py::arg("opened") = null, py::arg("flags") = 0);
	m.def("end_tab_item", &ImGui::EndTabItem);
	m.def("set_tab_item_closed", &ImGui::SetTabItemClosed, py::arg("tab_or_docked_window_label"));

	m.def("push_id_str", [](const char* str_id_begin, const char* str_id_end){ ImGui::PushID(str_id_begin, str_id_end); }, py::arg("str_id_begin"), py::arg("str_id_end") = nullptr);
	m.def("push_id_int", [](int int_id){ ImGui::PushID(int_id); } );
	m.def("pop_id", &ImGui::PopID);
	m.def("get_id_str", [](const char* str_id_begin, const char* str_id_end){ ImGui::GetID(str_id_begin, str_id_end); }, py::arg("str_id_begin"), py::arg("str_id_end") = nullptr);

	m.def("text", [](const char* text){ ImGui::Text("%s", text); });
	m.def("text_colored", [](const ImVec4& col, const char* text){ ImGui::TextColored(col, "%s", text); });
	m.def("text_disabled", [](const char* text){ ImGui::TextDisabled("%s", text); });
	m.def("text_wrapped", [](const char* text){ ImGui::TextWrapped("%s", text); });
	m.def("label_text", [](const char* label, const char* text){ ImGui::LabelText(label, "%s", text); });
	m.def("bullet_text", [](const char* text){ ImGui::BulletText("%s", text); });
	m.def("bullet", &ImGui::Bullet);

	m.def("button", &ImGui::Button, py::arg("label"), py::arg("size") = ImVec2(0,0));
	m.def("small_button", &ImGui::SmallButton);
	m.def("invisible_button", &ImGui::InvisibleButton, "button behavior without the visuals, frequently useful to build custom behaviors using the public api (along with IsItemActive, IsItemHovered, etc.)");
	m.def("arrow_button", &ImGui::ArrowButton, "square button with an arrow shape");

	m.def("tree_node", [](const char* label){ return ImGui::TreeNode(label); }, py::arg("label"));
	m.def("tree_node_ex", [](int id, ImGuiTreeNodeFlags flags, const char* label){ return ImGui::TreeNodeEx((void*)(intptr_t)id, flags, "%s", label); }, py::arg("id"), py::arg("flags") = 0, py::arg("label")="");
	m.def("tree_pop", &ImGui::TreePop);
    // OBSOLETED in 1.71 (from June 2019)
	m.def("set_next_tree_node_open", &ImGui::SetNextTreeNodeOpen, py::arg("is_open"), py::arg("cond") = 0);
	m.def("set_next_item_open", &ImGui::SetNextItemOpen, py::arg("is_open"), py::arg("cond") = 0);
	m.def("collapsing_header", [](const char* label, ImGuiTreeNodeFlags flags){ return ImGui::CollapsingHeader(label, flags); }, py::arg("label"), py::arg("flags") = 0);
	m.def("checkbox", [](const char* label, Bool& v){ return ImGui::Checkbox(label, &v.value); });
	m.def("radio_button", [](const char* label, bool active){ return ImGui::RadioButton(label, active); });
	m.def("radio_button", [](const char* label, Int& v, int v_button){ return ImGui::RadioButton(label, &v.value, v_button); });

	m.def("begin_combo", &ImGui::BeginCombo, py::arg("label"), py::arg("preview_value"), py::arg("flags") = 0);
	m.def("end_combo", &ImGui::EndCombo, "only call EndCombo() if BeginCombo() returns true!");
	m.def("combo", [](const char* label, Int& current_item, const std::vector<std::string>& items)
	{
		if (items.size() < 10)
		{
			const char* items_[10];
			for (int i = 0; i < (int)items.size(); ++i)
			{
				items_[i] = items[i].c_str();
			}
			return ImGui::Combo(label, &current_item.value, items_, (int)items.size());
		}
		else
		{
			const char** items_= new const char*[items.size()];
			for (int i = 0; i < (int)items.size(); ++i)
			{
				items_[i] = items[i].c_str();
			}
			bool result = ImGui::Combo(label, &current_item.value, items_, (int)items.size());
			delete[] items_;
			return result;
		}
	});

	m.def("input_text", [](const char* label, String& text, size_t buf_size, ImGuiInputTextFlags flags)
	{
		bool result = false;
		if (buf_size > 255)
		{
			char* buff = new char[buf_size + 1];
			strncpy(buff, text.value.c_str(), buf_size);
			result = ImGui::InputText(label, buff, buf_size, flags);
			if (result)
			{
				text.value = buff;
			}
			delete[] buff;
		}
		else
		{
			char buff[256];
			strncpy(buff, text.value.c_str(), 255);
			result = ImGui::InputText(label, buff, buf_size, flags);
			if (result)
			{
				text.value = buff;
			}
		}
		return result;
	}, py::arg("label"), py::arg("text"), py::arg("buf_size"), py::arg("flags") = 0);
	m.def("input_text_multiline", [](const char* label, String& text, size_t buf_size, const ImVec2& size, ImGuiInputTextFlags flags)
	{
		bool result = false;
		if (buf_size > 255)
		{
			char* buff = new char[buf_size + 1];
			strncpy(buff, text.value.c_str(), buf_size);
			result = ImGui::InputTextMultiline(label, buff, buf_size, size, flags);
			if (result)
			{
				text.value = buff;
			}
			delete[] buff;
		}
		else
		{
			char buff[256];
			strncpy(buff, text.value.c_str(), 255);
			result = ImGui::InputTextMultiline(label, buff, buf_size, size, flags);
			if (result)
			{
				text.value = buff;
			}
		}
		return result;
	}, py::arg("label"), py::arg("text"), py::arg("buf_size"), py::arg("size") = ImVec2(0,0), py::arg("flags") = 0);
	m.def("input_text_with_hint", [](const char* label, const char* hint, String& text, size_t buf_size, ImGuiInputTextFlags flags)
	{
		bool result = false;
		if (buf_size > 255)
		{
			char* buff = new char[buf_size];
			strncpy(buff, text.value.c_str(), buf_size);
			result = ImGui::InputTextWithHint(label, hint, buff, buf_size, flags);
			if (result)
			{
				text.value = buff;
			}
			delete[] buff;
		}
		else
		{
			char buff[256];
			strncpy(buff, text.value.c_str(), 256);
			result = ImGui::InputTextWithHint(label, hint, buff, buf_size, flags);
			if (result)
			{
				text.value = buff;
			}
		}
		return result;
	}, py::arg("label"), py::arg("hint"), py::arg("text"), py::arg("buf_size"), py::arg("flags") = 0);
	m.def("input_float", [](const char* label, Float& v, float step, float step_fast, const char* display_format, ImGuiInputTextFlags flags)
	{
		return ImGui::InputFloat(label, &v.value, step, step_fast, display_format, flags);
	}, py::arg("label"), py::arg("v"), py::arg("step") = 0.0f, py::arg("step_fast") = 0.0f, py::arg("display_format") = "%.3f", py::arg("flags") = 0);
	m.def("input_float2", [](const char* label, Float& v1, Float& v2, const char* display_format, ImGuiInputTextFlags flags)
	{
		float v[2] = {v1.value, v2.value};
		bool result = ImGui::InputFloat2(label, v, display_format, flags);
		v1.value = v[0];
		v2.value = v[1];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("display_format") = "%.3f", py::arg("flags") = 0);
	m.def("input_float3", [](const char* label, Float& v1, Float& v2, Float& v3, const char* display_format, ImGuiInputTextFlags flags)
	{
		float v[3] = {v1.value, v2.value, v3.value};
		bool result = ImGui::InputFloat3(label, v, display_format, flags);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("display_format") = "%.3f", py::arg("flags") = 0);
	m.def("input_float4", [](const char* label, Float& v1, Float& v2, Float& v3, Float& v4, const char* display_format, ImGuiInputTextFlags flags)
	{
		float v[4] = {v1.value, v2.value, v3.value, v4.value};
		bool result = ImGui::InputFloat4(label, v, display_format, flags);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		v4.value = v[3];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("display_format") = "%.3f", py::arg("flags") = 0);
	m.def("input_int", [](const char* label, Int& v, int step, int step_fast, ImGuiInputTextFlags flags)
	{
		return ImGui::InputInt(label, &v.value, step, step_fast, flags);
	}, py::arg("label"), py::arg("v"), py::arg("step") = 1, py::arg("step_fast") = 100, py::arg("flags") = 0);
	m.def("input_int2", [](const char* label, Int& v1, Int& v2, ImGuiInputTextFlags flags)
	{
		int v[2] = {v1.value, v2.value};
		bool result = ImGui::InputInt2(label, v, flags);
		v1.value = v[0];
		v2.value = v[1];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("flags") = 0);
	m.def("input_int3", [](const char* label, Int& v1, Int& v2, Int& v3, ImGuiInputTextFlags flags)
	{
		int v[3] = {v1.value, v2.value, v3.value};
		bool result = ImGui::InputInt3(label, v, flags);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("flags") = 0);
	m.def("input_int4", [](const char* label, Int& v1, Int& v2, Int& v3, Int& v4, ImGuiInputTextFlags flags)
	{
		int v[4] = {v1.value, v2.value, v3.value, v4.value};
		bool result = ImGui::InputInt4(label, v, flags);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		v4.value = v[3];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("flags") = 0);


	m.def("color_edit", [](const char* label, ImVec4& col)->bool
	{
		return ImGui::ColorEdit4(label, &col.x);
	});
	m.def("color_picker", [](const char* label, ImVec4& col)->bool
	{
		return ImGui::ColorPicker4(label, &col.x);
	});


	m.def("slider_float", [](const char* label, Float& v, float v_min, float v_max, const char* display_format, float power)
	{
		return ImGui::SliderFloat(label, &v.value, v_min, v_max, display_format, power);
	}, py::arg("label"), py::arg("v"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);
	m.def("slider_float2", [](const char* label, Float& v1, Float& v2, float v_min, float v_max, const char* display_format, float power)
	{
		float v[2] = {v1.value, v2.value};
		bool result = ImGui::SliderFloat2(label, v, v_min, v_max, display_format, power);
		v1.value = v[0];
		v2.value = v[1];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);
	m.def("slider_float3", [](const char* label, Float& v1, Float& v2, Float& v3, float v_min, float v_max, const char* display_format, float power)
	{
		float v[3] = {v1.value, v2.value, v3.value};
		bool result = ImGui::SliderFloat3(label, v, v_min, v_max, display_format, power);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);
	m.def("slider_float4", [](const char* label, Float& v1, Float& v2, Float& v3, Float& v4, float v_min, float v_max, const char* display_format, float power)
	{
		float v[4] = {v1.value, v2.value, v3.value, v4.value};
		bool result = ImGui::SliderFloat4(label, v, v_min, v_max, display_format, power);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		v4.value = v[3];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);

	m.def("v_slider_float", [](const char* label, const ImVec2& size, Float& v, float v_min, float v_max, const char* display_format, float power)
	{
		return ImGui::VSliderFloat(label, size, &v.value, v_min, v_max, display_format, power);
	}, py::arg("label"), py::arg("size"), py::arg("v"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);

	m.def("slider_angle", [](const char* label, Float& v_rad, float v_degrees_min, float v_degrees_max, const char* display_format)
	{
		return ImGui::SliderAngle(label, &v_rad.value, v_degrees_min, v_degrees_max, display_format);
	}, py::arg("label"), py::arg("v_rad"), py::arg("v_degrees_min")=-360.0f, py::arg("v_degrees_max")=+360.0f, py::arg("display_format") = "%.0f deg");

	m.def("slider_int", [](const char* label, Int& v, int v_min, int v_max, const char* display_format)
	{
		return ImGui::SliderInt(label, &v.value, v_min, v_max, display_format);
	}, py::arg("label"), py::arg("v"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	m.def("slider_int2", [](const char* label, Int& v1, Int& v2, int v_min, int v_max, const char* display_format)
	{
		int v[2] = {v1.value, v2.value};
		bool result = ImGui::SliderInt2(label, v, v_min, v_max, display_format);
		v1.value = v[0];
		v2.value = v[1];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	m.def("slider_int3", [](const char* label, Int& v1, Int& v2, Int& v3, int v_min, int v_max, const char* display_format)
	{
		int v[3] = {v1.value, v2.value, v3.value};
		bool result = ImGui::SliderInt3(label, v, v_min, v_max, display_format);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	m.def("slider_int4", [](const char* label, Int& v1, Int& v2, Int& v3, Int& v4, int v_min, int v_max, const char* display_format)
	{
		int v[4] = {v1.value, v2.value, v3.value, v4.value};
		bool result = ImGui::SliderInt4(label, v, v_min, v_max, display_format);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		v4.value = v[3];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");


	m.def("v_slider_int", [](const char* label, const ImVec2& size, Int& v, int v_min, int v_max, const char* display_format)
	{
		return ImGui::VSliderInt(label, size, &v.value,  v_min, v_max, display_format);
	}, py::arg("label"), py::arg("size"), py::arg("v"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");

	//
	m.def("drag_float", [](const char* label, Float& v, float v_speed, float v_min, float v_max, const char* display_format, float power)
		{
			return ImGui::DragFloat(label, &v.value, v_speed, v_min, v_max, display_format, power);
		}, py::arg("label"), py::arg("v"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);
	m.def("drag_float2", [](const char* label, Float& v1, Float& v2, float v_speed, float v_min, float v_max, const char* display_format, float power)
		{
			float v[2] = {v1.value, v2.value};
			bool result = ImGui::DragFloat2(label, v, v_speed, v_min, v_max, display_format, power);
			v1.value = v[0];
			v2.value = v[1];
			return result;
		}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);
	m.def("drag_float3", [](const char* label, Float& v1, Float& v2, Float& v3, float v_speed, float v_min, float v_max, const char* display_format, float power)
		{
			float v[3] = {v1.value, v2.value, v3.value};
			bool result = ImGui::DragFloat3(label, v, v_speed, v_min, v_max, display_format, power);
			v1.value = v[0];
			v2.value = v[1];
			v3.value = v[2];
			return result;
		}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);
	m.def("drag_float4", [](const char* label, Float& v1, Float& v2, Float& v3, Float& v4, float v_speed, float v_min, float v_max, const char* display_format, float power)
		{
			float v[4] = {v1.value, v2.value, v3.value, v4.value};
			bool result = ImGui::DragFloat4(label, v, v_speed, v_min, v_max, display_format, power);
			v1.value = v[0];
			v2.value = v[1];
			v3.value = v[2];
			v4.value = v[3];
			return result;
		}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.3f", py::arg("power") = 1.0f);

	m.def("drag_int", [](const char* label, Int& v, float v_speed, int v_min, int v_max, const char* display_format)
		{
			return ImGui::DragInt(label, &v.value, v_speed, v_min, v_max, display_format);
		}, py::arg("label"), py::arg("v"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	m.def("drag_int2", [](const char* label, Int& v1, Int& v2, float v_speed, int v_min, int v_max, const char* display_format)
		{
			int v[2] = {v1.value, v2.value};
			bool result = ImGui::DragInt2(label, v, v_speed, v_min, v_max, display_format);
			v1.value = v[0];
			v2.value = v[1];
			return result;
		}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	m.def("drag_int3", [](const char* label, Int& v1, Int& v2, Int& v3, float v_speed, int v_min, int v_max, const char* display_format)
		{
			int v[3] = {v1.value, v2.value, v3.value};
			bool result = ImGui::DragInt3(label, v, v_speed, v_min, v_max, display_format);
			v1.value = v[0];
			v2.value = v[1];
			v3.value = v[2];
			return result;
		}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	m.def("drag_int4", [](const char* label, Int& v1, Int& v2, Int& v3, Int& v4, float v_speed, int v_min, int v_max, const char* display_format)
		{
			int v[4] = {v1.value, v2.value, v3.value, v4.value};
			bool result = ImGui::DragInt4(label, v, v_speed, v_min, v_max, display_format);
			v1.value = v[0];
			v2.value = v[1];
			v3.value = v[2];
			v4.value = v[3];
			return result;
		}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("v_speed") = 1.0f, py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");

	m.def("plot_lines", [](
		const char* label,
		const std::vector<float>& values,
		int values_offset = 0,
		const char* overlay_text = NULL,
		float scale_min = FLT_MAX,
		float scale_max = FLT_MAX,
		ImVec2 graph_size = ImVec2(0,0),
		int stride = sizeof(float))
		{
			ImGui::PlotLines(label, values.data(), (int)values.size(), values_offset, overlay_text, scale_min, scale_max, graph_size, stride);
		}
		, py::arg("label")
		, py::arg("values")
		, py::arg("values_offset") = 0
		, py::arg("overlay_text") = nullptr
		, py::arg("scale_min") = FLT_MAX
		, py::arg("scale_max") = FLT_MAX
		, py::arg("graph_size") = ImVec2(0,0)
		, py::arg("stride") = sizeof(float)
		);

	m.def("progress_bar", &ImGui::ProgressBar, py::arg("fraction"), py::arg("size_arg") = ImVec2(-1,0), py::arg("overlay") = nullptr);

	m.def("color_button", &ImGui::ColorButton, py::arg("desc_id"), py::arg("col"), py::arg("flags") = 0, py::arg("size") = ImVec2(0,0), "display a colored square/button, hover for details, return true when pressed.");

	m.def("selectable", [](
		std::string label,
		bool selected = false,
		ImGuiSelectableFlags flags = 0,
		ImVec2 size = ImVec2(0,0))->bool
		{
			return ImGui::Selectable(label.c_str(), selected, flags, size);
		}
		, py::arg("label")
		, py::arg("selected") = false
		, py::arg("flags") = 0
		, py::arg("size") = ImVec2(0,0)
		);

	m.def("selectable", [](
		std::string label,
		Bool& selected,
		ImGuiSelectableFlags flags = 0,
		ImVec2 size = ImVec2(0,0))->bool
		{
			return ImGui::Selectable(label.c_str(), &selected.value, flags, size);
		}
		, py::arg("label")
		, py::arg("selected")
		, py::arg("flags") = 0
		, py::arg("size") = ImVec2(0,0)
		);

	m.def("list_box_header", [](
			std::string label,
			ImVec2 size = ImVec2(0,0))
			{
				ImGui::ListBoxHeader(label.c_str(), size);
			}
			, py::arg("label")
			, py::arg("size")
			);

	m.def("list_box_footer", &ImGui::ListBoxFooter);

	m.def("set_item_default_focus", &ImGui::SetItemDefaultFocus);
	m.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere);

	m.def("is_item_hovered", &ImGui::IsItemHovered, py::arg("flags") = 0);
	m.def("is_item_active", &ImGui::IsItemActive);
	m.def("is_item_focused", &ImGui::IsItemFocused);
	m.def("is_item_clicked", &ImGui::IsItemClicked, py::arg("mouse_button") = 0);
	m.def("is_item_visible", &ImGui::IsItemVisible);
	m.def("is_item_edited", &ImGui::IsItemEdited);
	m.def("is_item_activated", &ImGui::IsItemActivated);
	m.def("is_item_deactivated", &ImGui::IsItemDeactivated);
	m.def("is_item_deactivated_after_edit", &ImGui::IsItemDeactivatedAfterEdit);
	m.def("is_item_toggled_open", &ImGui::IsItemToggledOpen);
	m.def("is_any_item_hovered", &ImGui::IsAnyItemHovered);
	m.def("is_any_item_active", &ImGui::IsAnyItemActive);
	m.def("is_any_item_focused", &ImGui::IsAnyItemFocused);

	m.def("get_item_rect_min", &ImGui::GetItemRectMin);
	m.def("get_item_rect_max", &ImGui::GetItemRectMax);
	m.def("get_item_rect_size", &ImGui::GetItemRectSize);

	m.def("set_item_allow_overlap", &ImGui::SetItemAllowOverlap);

	m.def("get_time", &ImGui::GetTime);
	m.def("get_frame_count", &ImGui::GetFrameCount);

	m.def("get_key_index", &ImGui::GetKeyIndex);
	m.def("is_key_down", &ImGui::IsKeyDown);
	m.def("is_key_pressed", &ImGui::IsKeyPressed);
	m.def("is_key_released", &ImGui::IsKeyReleased);
	m.def("get_key_pressed_amount", &ImGui::GetKeyPressedAmount);
	m.def("is_mouse_down", &ImGui::IsMouseDown);
	m.def("is_any_mouse_down", &ImGui::IsAnyMouseDown);
	m.def("is_mouse_clicked", &ImGui::IsMouseClicked);
	m.def("is_mouse_double_clicked", &ImGui::IsMouseDoubleClicked);
	m.def("is_mouse_released", &ImGui::IsMouseReleased);
	m.def("is_mouse_dragging", &ImGui::IsMouseDragging);
	m.def("is_mouse_hovering_rect", &ImGui::IsMouseHoveringRect);
	m.def("is_mouse_pos_valid", &ImGui::IsMousePosValid);
	m.def("get_mouse_pos", &ImGui::GetMousePos);
	m.def("get_mouse_pos_on_opening_current_popup", &ImGui::GetMousePosOnOpeningCurrentPopup);
	m.def("get_mouse_drag_delta", &ImGui::GetMouseDragDelta);
	m.def("reset_mouse_drag_delta", &ImGui::ResetMouseDragDelta);

	m.def("capture_keyboard_from_app", &ImGui::CaptureKeyboardFromApp);
	m.def("capture_mouse_from_app", &ImGui::CaptureMouseFromApp);

	py::enum_<ImGuiDragDropFlags_>(m, "DragDropFlags")
		.value("SourceNoPreviewTooltip", ImGuiDragDropFlags_SourceNoPreviewTooltip)
		.value("SourceNoDisableHover", ImGuiDragDropFlags_SourceNoDisableHover)
		.value("SourceNoHoldToOpenOthers", ImGuiDragDropFlags_SourceNoHoldToOpenOthers)
		.value("SourceAllowNullID", ImGuiDragDropFlags_SourceAllowNullID)
		.value("SourceExtern", ImGuiDragDropFlags_SourceExtern)
		.value("SourceAutoExpirePayload", ImGuiDragDropFlags_SourceAutoExpirePayload)

		.value("AcceptBeforeDelivery", ImGuiDragDropFlags_AcceptBeforeDelivery)
		.value("AcceptNoDrawDefaultRect", ImGuiDragDropFlags_AcceptNoDrawDefaultRect)
		.value("AcceptNoPreviewTooltip", ImGuiDragDropFlags_AcceptNoPreviewTooltip)
		.value("AcceptPeekOnly", ImGuiDragDropFlags_AcceptPeekOnly)

		.export_values();

	m.def("begin_drag_drop_source", &ImGui::BeginDragDropSource);
	// todo:
	//m.def("set_drag_drop_payload", &ImGui::SetDragDropPayload);
	m.def("set_drag_drop_payload_string", [](std::string data){ImGui::SetDragDropPayload("string",data.c_str(), data.size());});
	m.def("end_drag_drop_source", &ImGui::EndDragDropSource);
	m.def("begin_drag_drop_target", &ImGui::BeginDragDropTarget);
	// todo:
	//m.def("accept_drag_drop_payload", &ImGui::AcceptDragDropPayload);
	m.def("accept_drag_drop_payload_string_preview", [](ImGuiDragDropFlags flags = 0)->std::string{
		auto payload = ImGui::AcceptDragDropPayload("string", flags);
		if (!payload->IsDataType("string") || !payload->Data)
			return "";
		if (payload->IsPreview())
			return std::string(static_cast<char*>(payload->Data), payload->DataSize);
		else
			return "";
	});
	m.def("accept_drag_drop_payload_string", [](ImGuiDragDropFlags flags = 0)->std::string{
		auto payload = ImGui::AcceptDragDropPayload("string", flags);
		if (!payload->IsDataType("string") || !payload->Data)
			return "";
		if (payload->IsDelivery())
			return std::string(static_cast<char*>(payload->Data), payload->DataSize);
		else
			return "";
	});

	m.def("end_drag_drop_target", &ImGui::EndDragDropTarget);
	m.def("get_drag_drop_payload", []()->std::string{
		auto payload = ImGui::GetDragDropPayload();
		if (!payload->IsDataType("string") || !payload->Data)
			return "";
		if (payload->IsDelivery())
			return std::string(static_cast<char*>(payload->Data), payload->DataSize);
		else
			return "";
	});

	m.def("push_clip_rect", &ImGui::PushClipRect);
	m.def("pop_clip_rect", &ImGui::PopClipRect);

	m.def("add_line", &AddLine, py::arg("a"), py::arg("b"), py::arg("col"), py::arg("thickness") = 1.0f);
	m.def("add_rect", &AddRect, py::arg("a"), py::arg("b"), py::arg("col"), py::arg("rounding") = 0.0f, py::arg("rounding_corners_flags") = ImDrawCornerFlags_All, py::arg("thickness") = 1.0f);
	m.def("add_rect_filled", &AddRectFilled, py::arg("a"), py::arg("b"), py::arg("col"), py::arg("rounding") = 0.0f, py::arg("rounding_corners_flags") = ImDrawCornerFlags_All);
	m.def("add_rect_filled_multicolor", &AddRectFilledMultiColor, py::arg("a"), py::arg("b"), py::arg("col_upr_left"), py::arg("col_upr_right"), py::arg("col_bot_right"), py::arg("col_bot_lefs"));
	m.def("add_quad", &AddQuad, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("d"), py::arg("col"), py::arg("thickness") = 1.0f);
	m.def("add_quad_filled", &AddQuadFilled, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("d"), py::arg("col"));
	m.def("add_triangle", &AddTriangle, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("col"), py::arg("thickness") = 1.0f);
	m.def("add_triangle_filled", &AddTriangleFilled, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("col"));
	m.def("add_circle", &AddCircle, py::arg("centre"), py::arg("radius"), py::arg("col"), py::arg("num_segments") = 12, py::arg("thickness") = 1.0f);
	m.def("add_circle_filled", &AddCircleFilled, py::arg("centre"), py::arg("radius"), py::arg("col"), py::arg("num_segments") = 12);
	m.def("add_bezier_curve", &AddBezierCurve, py::arg("pos0"), py::arg("cp0"), py::arg("cp1"), py::arg("pos1"), py::arg("col"), py::arg("thickness"), py::arg("num_segments") = 0);

	m.def("path_clear", &PathClear);
	m.def("path_line_to", &PathLineTo, py::arg("pos"));
	m.def("path_fill_convex", &PathFillConvex, py::arg("col"));
	m.def("path_stroke", &PathStroke, py::arg("col"), py::arg("closed"), py::arg("thickness"));

	m.def("get_glyph_ranges_default", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesDefault()); });
	m.def("get_glyph_ranges_korean", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesKorean()); });
	m.def("get_glyph_ranges_japanese", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesJapanese()); });
	m.def("get_glyph_ranges_chinese_full", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesChineseFull()); });
	m.def("get_glyph_ranges_chinese_simplified_common", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesChineseSimplifiedCommon()); });
	m.def("get_glyph_ranges_cyrillic", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesCyrillic()); });
	m.def("get_glyph_ranges_thai", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesThai()); });
	m.def("get_glyph_ranges_vietnamese", [](){ return range_to_list(ImGui::GetIO().Fonts->GetGlyphRangesVietnamese()); });

	auto get_persistent_storage = []()->std::vector<std::shared_ptr<std::vector<unsigned short> > >&
			{ static std::vector<std::shared_ptr<std::vector<unsigned short> > > x; return x;};

	m.def("add_font_from_file_ttf", [get_persistent_storage](
		std::string filename,
		float size_pixels = 32.0f, int oversample=2, bool merge=false, std::vector<unsigned short> range={})
		{
            ImFontConfig font_cfg = ImFontConfig();
            font_cfg.OversampleH = oversample;
            font_cfg.MergeMode = merge;
			if (range.size() > 0)
			{
				// Data needs to be persistent in memory until the atlas is built
				auto prange = std::make_shared<std::vector<unsigned short> >(range);
				prange->push_back(0);
				get_persistent_storage().push_back(prange);
				return ImGui::GetIO().Fonts->AddFontFromFileTTF(filename.c_str(), size_pixels, &font_cfg, prange->data());
			}
			else
				return ImGui::GetIO().Fonts->AddFontFromFileTTF(filename.c_str(), size_pixels, &font_cfg);
		}
		, py::arg("filename")
		, py::arg("size_pixels"), py::arg("oversample") = 2
		, py::arg("merge") = false, py::arg("range") = std::vector<int>(), py::return_value_policy::reference);

	m.def("add_font_default", [get_persistent_storage](int oversample=2, bool merge=false)
		{
            ImFontConfig font_cfg = ImFontConfig();
            font_cfg.OversampleH = oversample;
            font_cfg.MergeMode = merge;
			return ImGui::GetIO().Fonts->AddFontDefault(&font_cfg);
		}
		,py::arg("oversample") = 2
		, py::arg("merge") = false, py::return_value_policy::reference);

	m.def("build_font", [get_persistent_storage]()
		{
			ImGui::GetIO().Fonts->Build();
			get_persistent_storage().clear();
		});

	m.def("push_font", &ImGui::PushFont);
	m.def("pop_font", &ImGui::PopFont);
	m.def("get_font", &ImGui::GetFont);

	py::class_<ImFont>(m, "Font")
		.def(py::init())
	;

	m.def("set_display_framebuffer_scale",[](float scale){
		ImGui::GetIO().DisplayFramebufferScale = ImVec2(scale,scale);
	}, py::arg("scale"));
	m.def("get_display_framebuffer_scale",[](){
		return ImGui::GetIO().DisplayFramebufferScale;
	});

	m.def("set_font_global_scale",[](float scale){
		ImGui::GetIO().FontGlobalScale = scale;
	}, py::arg("scale"));
	m.def("get_font_global_scale",[](){
		return ImGui::GetIO().FontGlobalScale;
	});
	typedef void (*FImage_texId_wSize)(GLuint, ImVec2&);
	m.def("image", (FImage_texId_wSize)([](GLuint textureId, ImVec2& size)
	{
		ImGui::Image(reinterpret_cast<ImTextureID>(textureId), size);
	}));
	typedef void (*FImage_wSize)(Image*, ImVec2&);
	m.def("image", (FImage_wSize)([](Image* im, ImVec2& size)
	{
		ImGui::Image(reinterpret_cast<ImTextureID>(im->GetHandle()), size);
	}));
	typedef void (*FImage)(Image*);
	m.def("image", (FImage)([](Image* im)
	{
		ImGui::Image(reinterpret_cast<ImTextureID>(im->GetHandle()), ImVec2(im->m_width, im->m_height));
	}));

	m.def("image_button", &ImGui::ImageButton);

	m.attr("key_left_shift") = py::int_(GLFW_KEY_LEFT_SHIFT);
	m.attr("key_left_control") = py::int_(GLFW_KEY_LEFT_CONTROL);
	m.attr("key_left_alt") = py::int_(GLFW_KEY_LEFT_ALT);
	m.attr("key_left_super") = py::int_(GLFW_KEY_LEFT_SUPER);
	m.attr("key_right_shift") = py::int_(GLFW_KEY_RIGHT_SHIFT);
	m.attr("key_right_control") = py::int_(GLFW_KEY_RIGHT_CONTROL);
	m.attr("key_right_alt") = py::int_(GLFW_KEY_RIGHT_ALT);
	m.attr("key_right_super") = py::int_(GLFW_KEY_RIGHT_SUPER);

	m.def("inject_imgui_context", [](void* other) { GImGui = (ImGuiContext*)other; } );
}
