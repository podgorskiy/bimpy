/*
 * Copyright 2017-2018 Stanislav Pidhorskyi. All rights reserved.
 * License: https://raw.githubusercontent.com/podgorskiy/bimpy/master/LICENSE.txt
 */

#include "imgui_glfw.h"
#define IMGUI_DEFINE_MATH_OPERATORS
#include "imgui_internal.h"
#include <GL/gl3w.h>
#include <GLFW/glfw3.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <memory>
#include <mutex>

namespace py = pybind11;

class Context
{
public:
	void Init(int width, int height, const std::string& name);
	
	void Resize(int width, int height);

	void NewFrame();
	
	void Render();
	
	bool ShouldClose();
private:
	struct Imp
	{
		GLFWwindow* m_window = nullptr;	
		int m_width;
		int m_height;
		struct ImGuiContext* imgui;
		imguiBinding imbinding;
		std::mutex imgui_ctx_mutex;
		~Imp();
	};
	
	std::shared_ptr<Imp> m_imp = std::make_shared<Imp>();
};


void Context::Init(int width, int height, const std::string& name)
{
	if (nullptr == m_imp->m_window)
	{
		glfwInit();

		m_imp->m_window = glfwCreateWindow(width, height, name.c_str(), NULL, NULL);

		glfwMakeContextCurrent(m_imp->m_window);
		
		gl3wInit();
		
		m_imp->imgui = new ImGuiContext();
		GImGui = m_imp->imgui;

		ImGui_ImplGlfwGL3_Init(&m_imp->imbinding, m_imp->m_window, false);
		glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
		
		m_imp->m_width = width;
		m_imp->m_height = height;
		
		glfwSetWindowUserPointer(m_imp->m_window, m_imp.get());

		glfwSetWindowSizeCallback(m_imp->m_window, [](GLFWwindow* window, int width, int height)
		{
			Context* ctx = static_cast<Context*>(glfwGetWindowUserPointer(window));
			ctx->Resize(width, height);
		});

		glfwSetKeyCallback(m_imp->m_window, [](GLFWwindow*, int key, int, int action, int mods)
		{
			ImGuiIO& io = ImGui::GetIO();
			if (action == GLFW_PRESS)
				io.KeysDown[key] = true;
			if (action == GLFW_RELEASE)
				io.KeysDown[key] = false;

			io.KeyCtrl = io.KeysDown[GLFW_KEY_LEFT_CONTROL] || io.KeysDown[GLFW_KEY_RIGHT_CONTROL];
			io.KeyShift = io.KeysDown[GLFW_KEY_LEFT_SHIFT] || io.KeysDown[GLFW_KEY_RIGHT_SHIFT];
			io.KeyAlt = io.KeysDown[GLFW_KEY_LEFT_ALT] || io.KeysDown[GLFW_KEY_RIGHT_ALT];
			io.KeySuper = io.KeysDown[GLFW_KEY_LEFT_SUPER] || io.KeysDown[GLFW_KEY_RIGHT_SUPER];
		});

		glfwSetCharCallback(m_imp->m_window, [](GLFWwindow*, unsigned int c)
		{
			ImGuiIO& io = ImGui::GetIO();
			io.AddInputCharacter((unsigned short)c);
		});

		glfwSetScrollCallback(m_imp->m_window, [](GLFWwindow*, double /*xoffset*/, double yoffset)
		{
			ImGuiIO& io = ImGui::GetIO();
			io.MouseWheel += (float)yoffset * 2.0f;
		});

		glfwSetMouseButtonCallback(m_imp->m_window, [](GLFWwindow*, int button, int action, int /*mods*/)
		{
			ImGuiIO& io = ImGui::GetIO();

			if (button >= 0 && button < 3)
			{
				io.MouseDown[button] = action == GLFW_PRESS;
			}
		});
	}
}


Context::Imp::~Imp()
{
	glfwSetWindowSizeCallback(m_window, nullptr);
	GImGui = imgui;
	ImGui_ImplGlfwGL3_Shutdown(&imbinding);
	glfwTerminate();
	delete imgui;
}


void Context::Render()
{
	glfwMakeContextCurrent(m_imp->m_window);
	glViewport(0, 0, m_imp->m_width, m_imp->m_height);
	glClear(GL_COLOR_BUFFER_BIT);
	ImGui_ImplGlfwGL3_Render(&m_imp->imbinding);
	glfwSwapInterval(1);
	glfwSwapBuffers(m_imp->m_window);
	glfwPollEvents();
	m_imp->imgui_ctx_mutex.unlock();
}


void Context::NewFrame()
{
	m_imp->imgui_ctx_mutex.lock();
	GImGui = m_imp->imgui;
	ImGui_ImplGlfwGL3_NewFrame(&m_imp->imbinding);
}


void Context::Resize(int width, int height)
{
	m_imp->m_width = width;
	m_imp->m_height = height;
}


bool Context::ShouldClose()
{
	return glfwWindowShouldClose(m_imp->m_window) != 0;
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

PYBIND11_MODULE(_bimpy, m) {
	static Bool null;
	null.null = true;
	
	m.doc() = "bimpy - bundled imgui for python";

	py::enum_<ImGuiCond_>(m, "Condition")
		.value("Always", ImGuiCond_::ImGuiCond_Always)
		.value("Once", ImGuiCond_::ImGuiCond_Once)
		.value("FirstUseEver", ImGuiCond_::ImGuiCond_FirstUseEver)
		.value("Appearing", ImGuiCond_::ImGuiCond_Appearing)
		.export_values();

	py::enum_<ImGuiWindowFlags_>(m, "WindowFlags")
		.value("NoTitleBar", ImGuiWindowFlags_::ImGuiWindowFlags_NoTitleBar)
		.value("NoResize", ImGuiWindowFlags_::ImGuiWindowFlags_NoResize)
		.value("NoMove", ImGuiWindowFlags_::ImGuiWindowFlags_NoMove)
		.value("NoScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollbar)
		.value("NoScrollWithMouse", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollWithMouse)
		.value("NoCollapse", ImGuiWindowFlags_::ImGuiWindowFlags_NoCollapse)
		.value("AlwaysAutoResize", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysAutoResize)
		.value("ShowBorders", ImGuiWindowFlags_::ImGuiWindowFlags_ShowBorders)
		.value("NoSavedSettings", ImGuiWindowFlags_::ImGuiWindowFlags_NoSavedSettings)
		.value("NoInputs", ImGuiWindowFlags_::ImGuiWindowFlags_NoInputs)
		.value("MenuBar", ImGuiWindowFlags_::ImGuiWindowFlags_MenuBar)
		.value("HorizontalScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_HorizontalScrollbar)
		.value("NoFocusOnAppearing", ImGuiWindowFlags_::ImGuiWindowFlags_NoFocusOnAppearing)
		.value("NoBringToFrontOnFocus", ImGuiWindowFlags_::ImGuiWindowFlags_NoBringToFrontOnFocus)
		.value("AlwaysVerticalScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysVerticalScrollbar)
		.value("AlwaysHorizontalScrollbar", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysHorizontalScrollbar)
		.value("AlwaysUseWindowPadding", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysUseWindowPadding)
		.export_values();
		
	py::enum_<ImGuiInputTextFlags_>(m, "InputTextFlags")
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

	py::enum_<ImGuiCol_>(m, "Colors")
		.value("Text", ImGuiCol_::ImGuiCol_Text)
		.value("TextDisabled", ImGuiCol_::ImGuiCol_TextDisabled)
		.value("WindowBg", ImGuiCol_::ImGuiCol_WindowBg)
		.value("ChildWindowBg", ImGuiCol_::ImGuiCol_ChildWindowBg)
		.value("PopupBg", ImGuiCol_::ImGuiCol_PopupBg)
		.value("Border", ImGuiCol_::ImGuiCol_Border)
		.value("BorderShadow", ImGuiCol_::ImGuiCol_BorderShadow)
		.value("FrameBg", ImGuiCol_::ImGuiCol_FrameBg)
		.value("FrameBgHovered", ImGuiCol_::ImGuiCol_FrameBgHovered)
		.value("FrameBgActive", ImGuiCol_::ImGuiCol_FrameBgActive)
		.value("TitleBg", ImGuiCol_::ImGuiCol_TitleBg)
		.value("TitleBgCollapsed", ImGuiCol_::ImGuiCol_TitleBgCollapsed)
		.value("TitleBgActive", ImGuiCol_::ImGuiCol_TitleBgActive)
		.value("MenuBarBg", ImGuiCol_::ImGuiCol_MenuBarBg)
		.value("ScrollbarBg", ImGuiCol_::ImGuiCol_ScrollbarBg)
		.value("ScrollbarGrab", ImGuiCol_::ImGuiCol_ScrollbarGrab)
		.value("ScrollbarGrabHovered", ImGuiCol_::ImGuiCol_ScrollbarGrabHovered)
		.value("ScrollbarGrabActive", ImGuiCol_::ImGuiCol_ScrollbarGrabActive)
		.value("ComboBg", ImGuiCol_::ImGuiCol_ComboBg)
		.value("CheckMark", ImGuiCol_::ImGuiCol_CheckMark)
		.value("SliderGrab", ImGuiCol_::ImGuiCol_SliderGrab)
		.value("SliderGrabActive", ImGuiCol_::ImGuiCol_SliderGrabActive)
		.value("Button", ImGuiCol_::ImGuiCol_Button)
		.value("ButtonHovered", ImGuiCol_::ImGuiCol_ButtonHovered)
		.value("ButtonActive", ImGuiCol_::ImGuiCol_ButtonActive)
		.value("Header", ImGuiCol_::ImGuiCol_Header)
		.value("HeaderHovered", ImGuiCol_::ImGuiCol_HeaderHovered)
		.value("HeaderActive", ImGuiCol_::ImGuiCol_HeaderActive)
		.value("Column", ImGuiCol_::ImGuiCol_Column)
		.value("ColumnHovered", ImGuiCol_::ImGuiCol_ColumnHovered)
		.value("ColumnActive", ImGuiCol_::ImGuiCol_ColumnActive)
		.value("ResizeGrip", ImGuiCol_::ImGuiCol_ResizeGrip)
		.value("ResizeGripActive", ImGuiCol_::ImGuiCol_ResizeGripActive)
		.value("ResizeGripHovered", ImGuiCol_::ImGuiCol_ResizeGripHovered)
		.value("CloseButton", ImGuiCol_::ImGuiCol_CloseButton)
		.value("CloseButtonHovered", ImGuiCol_::ImGuiCol_CloseButtonHovered)
		.value("CloseButtonActive", ImGuiCol_::ImGuiCol_CloseButtonActive)
		.value("PlotLines", ImGuiCol_::ImGuiCol_PlotLines)
		.value("PlotLinesHovered", ImGuiCol_::ImGuiCol_PlotLinesHovered)
		.value("PlotHistogram", ImGuiCol_::ImGuiCol_PlotHistogram)
		.value("PlotHistogramHovered", ImGuiCol_::ImGuiCol_PlotHistogramHovered)
		.value("TextSelectedBg", ImGuiCol_::ImGuiCol_TextSelectedBg)
		.value("ModalWindowDarkening", ImGuiCol_::ImGuiCol_ModalWindowDarkening)
		.export_values();
		
	py::class_<Context>(m, "Context")
		.def(py::init())
		.def("init", &Context::Init, "Initializes context and creates window")
		.def("new_frame", &Context::NewFrame, "Starts a new frame. NewFrame must be called before any imgui functions")
		.def("render", &Context::Render, "Finilizes the frame and draws all UI. Render must be called after all imgui functions")
		.def("should_close", &Context::ShouldClose)
		.def("__enter__", &Context::NewFrame)
		.def("__exit__", [](Context& self, py::object, py::object, py::object)
			{
				self.Render();
			});
	
	py::enum_<ImGuiCorner>(m, "Corner")
		.value("TopLeft", ImGuiCorner::ImGuiCorner_TopLeft)
		.value("TopRight", ImGuiCorner::ImGuiCorner_TopRight)
		.value("BotRight", ImGuiCorner::ImGuiCorner_BotRight)
		.value("BotLeft", ImGuiCorner::ImGuiCorner_BotLeft)
		.value("All", ImGuiCorner::ImGuiCorner_All)
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
		.def_readwrite("w", &ImVec4::w);
	
	py::class_<ImGuiStyle>(m, "GuiStyle")
		.def(py::init())
		.def_readwrite("alpha", &ImGuiStyle::Alpha)
		.def_readwrite("window_padding", &ImGuiStyle::WindowPadding)
		.def_readwrite("window_min_size", &ImGuiStyle::WindowMinSize)
		.def_readwrite("window_rounding", &ImGuiStyle::WindowRounding)
		.def_readwrite("window_title_align", &ImGuiStyle::WindowTitleAlign)
		.def_readwrite("child_window_rounding", &ImGuiStyle::ChildWindowRounding)
		.def_readwrite("frame_padding", &ImGuiStyle::FramePadding)
		.def_readwrite("frame_rounding", &ImGuiStyle::FrameRounding)
		.def_readwrite("item_spacing", &ImGuiStyle::ItemSpacing)
		.def_readwrite("item_inner_spacing", &ImGuiStyle::ItemInnerSpacing)
		.def_readwrite("touch_extra_padding", &ImGuiStyle::TouchExtraPadding)
		//.def_readwrite("window_fill_alpha_default", &ImGuiStyle::WindowFillAlphaDefault)
		.def_readwrite("indent_spacing", &ImGuiStyle::IndentSpacing)
		.def_readwrite("columns_min_spacing", &ImGuiStyle::ColumnsMinSpacing)
		.def_readwrite("scroll_bar_size", &ImGuiStyle::ScrollbarSize)
		.def_readwrite("scroll_bar_rounding", &ImGuiStyle::ScrollbarRounding)
		.def_readwrite("grab_min_size", &ImGuiStyle::GrabMinSize)
		.def_readwrite("grab_rounding", &ImGuiStyle::GrabRounding)
		.def_readwrite("display_window_padding", &ImGuiStyle::DisplayWindowPadding)
		.def_readwrite("display_safe_area_padding", &ImGuiStyle::DisplaySafeAreaPadding)
		.def_readwrite("anti_aliased_lines", &ImGuiStyle::AntiAliasedLines)
		.def_readwrite("anti_aliased_shapes", &ImGuiStyle::AntiAliasedShapes)
		.def_readwrite("curve_tessellation_tol", &ImGuiStyle::CurveTessellationTol)
		.def("get_color",[](ImGuiStyle& self, ImGuiCol_ a)
			{
				return self.Colors[(int)a];
			})
		.def("set_color",[](ImGuiStyle& self, ImGuiCol_ a, ImVec4 c)
			{
				self.Colors[(int)a] = c;
			});

	m.def("get_style", &ImGui::GetStyle);
	m.def("set_style", [](const ImGuiStyle& a) 
		{
			ImGui::GetStyle() = a;
		});
	
	m.def("show_test_window", [](){ ImGui::ShowTestWindow(); });
	
	m.def("begin",[](const std::string& name, Bool& opened, ImGuiWindowFlags flags) -> bool
		{
			return ImGui::Begin(name.c_str(), opened.null ? nullptr : &opened.value, flags);
		},
		"Push a new ImGui window to add widgets to",
		py::arg("name"), py::arg("opened") = null, py::arg("flags") = ImGuiWindowFlags_(0));
	  
	m.def("end", &ImGui::End);
	
	m.def("begin_child",[](const std::string& str_id, const ImVec2& size, bool border, ImGuiWindowFlags extra_flags) -> bool
		{
			return ImGui::BeginChild(str_id.c_str(), size);
		},
		"begin a scrolling region. size==0.0f: use remaining window size, size<0.0f: use remaining window size minus abs(size). size>0.0f: fixed size. each axis can use a different mode, e.g. ImVec2(0,400).",
		py::arg("str_id"), py::arg("size") = ImVec2(0,0), py::arg("border") = false, py::arg("extra_flags") = ImGuiWindowFlags_(0));
		
	m.def("end_child", &ImGui::EndChild);
	
	m.def("get_content_region_max", &ImGui::GetContentRegionMax);
	m.def("get_content_region_avail", &ImGui::GetContentRegionAvail);
	m.def("get_content_region_avail_width", &ImGui::GetContentRegionAvailWidth);
	m.def("get_window_content_region_min", &ImGui::GetWindowContentRegionMin);
	m.def("get_window_content_region_max", &ImGui::GetWindowContentRegionMax);
	m.def("get_window_content_region_width", &ImGui::GetWindowContentRegionWidth);
	m.def("get_window_font_size", &ImGui::GetWindowFontSize);
	m.def("set_window_font_scale", &ImGui::SetWindowFontScale);
	m.def("get_window_pos", &ImGui::GetWindowPos);
	m.def("get_window_size", &ImGui::GetWindowSize);
	m.def("get_window_width", &ImGui::GetWindowWidth);
	m.def("get_window_height", &ImGui::GetWindowHeight);
	m.def("is_window_collapsed", &ImGui::IsWindowCollapsed);
	m.def("is_window_appearing", &ImGui::IsWindowAppearing);
	m.def("set_window_font_scale", &ImGui::SetWindowFontScale); 
	
	m.def("set_next_window_pos", &ImGui::SetNextWindowPos, py::arg("pos"), py::arg("cond") = 0, py::arg("pivot") = ImVec2(0,0));
	m.def("set_next_window_size", &ImGui::SetNextWindowSize, py::arg("size"), py::arg("cond") = 0);
	m.def("set_next_window_size_constraints", [](const ImVec2& size_min, const ImVec2& size_max){ ImGui::SetNextWindowSizeConstraints(size_min, size_max); }, py::arg("size_min"), py::arg("size_max") = 0);
	m.def("set_next_window_content_size", &ImGui::SetNextWindowContentSize, py::arg("size"));
	m.def("set_next_window_content_width", &ImGui::SetNextWindowContentWidth, py::arg("width"));
	m.def("set_next_window_collapsed", &ImGui::SetNextWindowCollapsed, py::arg("collapsed"), py::arg("cond") = 0);
	m.def("set_next_window_focus", &ImGui::SetNextWindowFocus); 
	m.def("set_window_pos", [](const char* name, const ImVec2& pos, ImGuiCond cond){ ImGui::SetWindowPos(name, pos, cond); }, py::arg("name"), py::arg("pos"), py::arg("cond") = 0);
	m.def("set_window_size", [](const char* name, const ImVec2& size, ImGuiCond cond){ ImGui::SetWindowSize(name, size, cond); }, py::arg("name"), py::arg("size"), py::arg("cond") = 0);
	m.def("set_window_collapsed", [](const char* name, bool collapsed, ImGuiCond cond){ ImGui::SetWindowCollapsed(name, collapsed, cond); }, py::arg("name"), py::arg("collapsed"), py::arg("cond") = 0);
	m.def("set_window_focus", [](const char* name){ ImGui::SetWindowFocus(name); }, py::arg("name"));
	
	m.def("get_scroll_x", &ImGui::GetScrollX);
	m.def("get_scroll_y", &ImGui::GetScrollY);
	m.def("get_scroll_max_x", &ImGui::GetScrollMaxX);
	m.def("get_scroll_max_y", &ImGui::GetScrollMaxY);
	m.def("set_scroll_x", &ImGui::SetScrollX);
	m.def("set_scroll_y", &ImGui::SetScrollY);
	m.def("set_scroll_here", &ImGui::SetScrollHere, py::arg("center_y_ratio") = 0.5f);
	m.def("set_scroll_from_pos_y", &ImGui::SetScrollFromPosY, py::arg("pos_y"), py::arg("center_y_ratio") = 0.5f);
	m.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere, py::arg("offset") = 0.0f);
	
	m.def("push_style_color", [](ImGuiCol_ idx, const ImVec4& col){ ImGui::PushStyleColor((ImGuiCol)idx, col); });
	m.def("pop_style_color", &ImGui::PopStyleColor, py::arg("count") = 1);
	
	m.def("push_item_width", &ImGui::PushItemWidth);
	m.def("pop_item_width", &ImGui::PopItemWidth);
	m.def("calc_item_width", &ImGui::CalcItemWidth);
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
	m.def("align_first_text_height_to_widgets", &ImGui::AlignFirstTextHeightToWidgets);
	m.def("get_text_line_height", &ImGui::GetTextLineHeight);
	m.def("get_text_line_height_with_spacing", &ImGui::GetTextLineHeightWithSpacing);
	m.def("get_items_line_height_with_spacing", &ImGui::GetItemsLineHeightWithSpacing);

	m.def("columns", &ImGui::Columns, py::arg("count") = 1, py::arg("id") = nullptr, py::arg("border") = true);
	m.def("next_column", &ImGui::NextColumn);
	m.def("get_column_index", &ImGui::GetColumnIndex);
	m.def("get_column_offset", &ImGui::GetColumnOffset, py::arg("column_index") = -1);
	m.def("set_column_offset", &ImGui::SetColumnOffset, py::arg("column_index"), py::arg("offset_x"));
	m.def("get_column_width", &ImGui::GetColumnWidth, py::arg("column_index") = -1);
	m.def("get_columns_count", &ImGui::GetColumnsCount);
	
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
	m.def("invisible_button", &ImGui::InvisibleButton);
	m.def("collapsing_header", [](const char* label, ImGuiTreeNodeFlags flags){ return ImGui::CollapsingHeader(label, flags); }, py::arg("label"), py::arg("flags") = 0);
	m.def("checkbox", [](const char* label, Bool& v){ return ImGui::Checkbox(label, &v.value); });
	m.def("radio_button", [](const char* label, bool active){ return ImGui::RadioButton(label, active); });
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
		if (buf_size > 256)
		{
			char* buff = new char[buf_size];
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
			strncpy(buff, text.value.c_str(), 256);
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
		if (buf_size > 256)
		{
			char* buff = new char[buf_size];
			strncpy(buff, text.value.c_str(), buf_size);
			result = ImGui::InputTextMultiline(label, &text.value[0], buf_size, size, flags);
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
			result = ImGui::InputTextMultiline(label, &text.value[0], buf_size, size, flags);
			if (result)
			{
				text.value = buff;
			}
		}	
		return result;
	}, py::arg("label"), py::arg("text"), py::arg("buf_size"), py::arg("size") = ImVec2(0,0), py::arg("flags") = 0);
	m.def("input_float", [](const char* label, Float& v, float step, float step_fast, int decimal_precision, ImGuiInputTextFlags flags)
	{
		return ImGui::InputFloat(label, &v.value, step, step_fast, decimal_precision, flags);
	}, py::arg("label"), py::arg("v"), py::arg("step") = 0.0f, py::arg("step_fast") = 0.0f, py::arg("decimal_precision") = -1, py::arg("flags") = 0);
	m.def("input_float2", [](const char* label, Float& v1, Float& v2, int decimal_precision, ImGuiInputTextFlags flags)
	{
		float v[2] = {v1.value, v2.value};
		bool result = ImGui::InputFloat2(label, v, decimal_precision, flags);
		v1.value = v[0];
		v2.value = v[1];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("decimal_precision") = -1, py::arg("flags") = 0);
	m.def("input_float3", [](const char* label, Float& v1, Float& v2, Float& v3, int decimal_precision, ImGuiInputTextFlags flags)
	{
		float v[3] = {v1.value, v2.value, v3.value};
		bool result = ImGui::InputFloat3(label, v, decimal_precision, flags);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("decimal_precision") = -1, py::arg("flags") = 0);
	m.def("input_float4", [](const char* label, Float& v1, Float& v2, Float& v3, Float& v4, int decimal_precision, ImGuiInputTextFlags flags)
	{
		float v[4] = {v1.value, v2.value, v3.value, v4.value};
		bool result = ImGui::InputFloat4(label, v, decimal_precision, flags);
		v1.value = v[0];
		v2.value = v[1];
		v3.value = v[2];
		v4.value = v[3];
		return result;
	}, py::arg("label"), py::arg("v1"), py::arg("v2"), py::arg("v3"), py::arg("v4"), py::arg("decimal_precision") = -1, py::arg("flags") = 0);
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

	m.def("slider_angle", [](const char* label, Float& v_rad, float v_degrees_min, float v_degrees_max)
	{
		return ImGui::SliderAngle(label, &v_rad.value, v_degrees_min, v_degrees_max);
	}, py::arg("label"), py::arg("v_rad"), py::arg("v_degrees_min")=-360.0f, py::arg("v_degrees_max")=+360.0f);
	
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
		return ImGui::VSliderInt(label, size, &v.value, v_min, v_max, display_format);
	}, py::arg("label"), py::arg("size"), py::arg("v"), py::arg("v_min"), py::arg("v_max"), py::arg("display_format") = "%.0f");
	
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
		, py::arg("graph_size")	 = ImVec2(0,0)
		, py::arg("stride") = sizeof(float)
		);
		
	m.def("progress_bar", &ImGui::ProgressBar, py::arg("fraction"), py::arg("size_arg") = ImVec2(-1,0), py::arg("overlay") = nullptr);

	m.def("color_button", &ImGui::ColorButton, py::arg("desc_id"), py::arg("col"), py::arg("flags") = 0, py::arg("size") = ImVec2(0,0));
	
	m.def("add_line", &AddLine, py::arg("a"), py::arg("b"), py::arg("col"), py::arg("thickness") = 1.0f);
	m.def("add_rect", &AddRect, py::arg("a"), py::arg("b"), py::arg("col"), py::arg("rounding") = 0.0f, py::arg("rounding_corners_flags") = ImGuiCorner::ImGuiCorner_All, py::arg("thickness") = 1.0f);
	m.def("add_rect_filled", &AddRectFilled, py::arg("a"), py::arg("b"), py::arg("col"), py::arg("rounding") = 0.0f, py::arg("rounding_corners_flags") = ImGuiCorner::ImGuiCorner_All);
	m.def("add_rect_filled_multicolor", &AddRectFilledMultiColor, py::arg("a"), py::arg("b"), py::arg("col_upr_left"), py::arg("col_upr_right"), py::arg("col_bot_right"), py::arg("col_bot_lefs"));
	m.def("add_quad", &AddQuad, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("d"), py::arg("col"), py::arg("thickness") = 1.0f);
	m.def("add_quad_filled", &AddQuadFilled, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("d"), py::arg("col"));
	m.def("add_triangle", &AddTriangle, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("col"), py::arg("thickness") = 1.0f);
	m.def("add_triangle_filled", &AddTriangleFilled, py::arg("a"), py::arg("b"), py::arg("c"), py::arg("col"));
	m.def("add_circle", &AddCircle, py::arg("centre"), py::arg("radius"), py::arg("col"), py::arg("num_segments") = 12, py::arg("thickness") = 1.0f);
	m.def("add_circle_filled", &AddCircleFilled, py::arg("centre"), py::arg("radius"), py::arg("col"), py::arg("num_segments") = 12);
}
