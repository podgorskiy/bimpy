// ImGui GLFW binding with OpenGL3 + shaders
// In this binding, ImTextureID is used to store an OpenGL 'GLuint' texture identifier. Read the FAQ about ImTextureID in imgui.cpp.

// You can copy and use unmodified imgui_impl_* files in your project. See main.cpp for an example of using this.
// If you use this binding you'll need to call 4 functions: ImGui_ImplXXXX_Init(), ImGui_ImplXXXX_NewFrame(), ImGui::Render() and ImGui_ImplXXXX_Shutdown().
// If you are new to ImGui, see examples/README.txt and documentation at the top of imgui.cpp.
// https://github.com/ocornut/imgui
#include <imgui.h>

struct GLFWwindow;

struct imguiBinding
{
	struct GLFWwindow*  g_Window = NULL;
	double       g_Time = 0.0f;
	bool         g_MousePressed[3] = { false, false, false };
	float        g_MouseWheel = 0.0f;
	unsigned int g_FontTexture = 0;
	int          g_ShaderHandle = 0, g_VertHandle = 0, g_FragHandle = 0;
	int          g_AttribLocationTex = 0, g_AttribLocationProjMtx = 0;
	int          g_AttribLocationPosition = 0, g_AttribLocationUV = 0, g_AttribLocationColor = 0;
	unsigned int g_VboHandle = 0, g_VaoHandle = 0, g_ElementsHandle = 0;
};

extern struct imguiBinding* im_current;

IMGUI_API bool        ImGui_ImplGlfwGL3_Init(imguiBinding* im, GLFWwindow* window, bool install_callbacks);
IMGUI_API void        ImGui_ImplGlfwGL3_Shutdown(imguiBinding* im);
IMGUI_API void        ImGui_ImplGlfwGL3_NewFrame(imguiBinding* im);
IMGUI_API void        ImGui_ImplGlfwGL3_Render(imguiBinding* im);

// Use if you want to reset your rendering device without losing ImGui state.
IMGUI_API void        ImGui_ImplGlfwGL3_InvalidateDeviceObjects(imguiBinding* im);
IMGUI_API bool        ImGui_ImplGlfwGL3_CreateDeviceObjects(imguiBinding* im);
