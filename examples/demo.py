# dear imgui, v1.75
# (demo code)

# This is a translation (not finished though, right now it's quite far from being finished) of imgui_demo.cpp to Python.


# Help:
# - Read FAQ at http:#dearimgui.org/faq

# Index of this file:

# [SECTION] Forward Declarations, Helpers
# [SECTION] Demo Window / ShowDemoWindow()
# [SECTION] About Window / ShowAboutWindow()
# [SECTION] Style Editor / ShowStyleEditor()
# [SECTION] Example App: Main Menu Bar / ShowExampleAppMainMenuBar()
# [SECTION] Example App: Debug Console / ShowExampleAppConsole()
# [SECTION] Example App: Debug Log / ShowExampleAppLog()
# [SECTION] Example App: Simple Layout / ShowExampleAppLayout()
# [SECTION] Example App: Property Editor / ShowExampleAppPropertyEditor()
# [SECTION] Example App: Long Text / ShowExampleAppLongText()
# [SECTION] Example App: Auto Resize / ShowExampleAppAutoResize()
# [SECTION] Example App: Constrained Resize / ShowExampleAppConstrainedResize()
# [SECTION] Example App: Simple Overlay / ShowExampleAppSimpleOverlay()
# [SECTION] Example App: Manipulating Window Titles / ShowExampleAppWindowTitles()
# [SECTION] Example App: Custom Rendering using ImDrawList API / ShowExampleAppCustomRendering()
# [SECTION] Example App: Documents Handling / ShowExampleAppDocuments()

import bimpy as bp
from bimpy.utils import help_marker


# Examples Apps (accessible from the "Examples" menu)
show_app_documents = bp.Bool(False)
show_app_main_menu_bar = bp.Bool(False)
show_app_console = bp.Bool(False)
show_app_log = bp.Bool(False)
show_app_layout = bp.Bool(False)
show_app_property_editor = bp.Bool(False)
show_app_long_text = bp.Bool(False)
show_app_auto_resize = bp.Bool(False)
show_app_constrained_resize = bp.Bool(False)
show_app_simple_overlay = bp.Bool(False)
show_app_window_titles = bp.Bool(False)
show_app_custom_rendering = bp.Bool(False)

#  Dear ImGui Apps (accessible from the "Tools" menu)
show_app_metrics = bp.Bool(False)
show_app_style_editor = bp.Bool(False)
show_app_about = bp.Bool(False)

#  Demonstrate the various window flags. Typically you would just use the default!
no_titlebar = bp.Bool(False)
no_scrollbar = bp.Bool(False)
no_menu = bp.Bool(False)
no_move = bp.Bool(False)
no_resize = bp.Bool(False)
no_collapse = bp.Bool(False)
no_close = bp.Bool(False)
no_nav = bp.Bool(False)
no_background = bp.Bool(False)
no_bring_to_front = bp.Bool(False)

show_config_info = bp.Bool(False)


#  Helper to display basic user controls.
def show_user_guide():
    bp.bullet_text("Double-click on title bar to collapse window.")
    bp.bullet_text("Click and drag on lower corner to resize window\n(double-click to auto fit window to its contents).")
    bp.bullet_text("CTRL+Click on a slider or drag box to input value as text.")
    bp.bullet_text("TAB/SHIFT+TAB to cycle through keyboard editable fields.")
    bp.bullet_text("While inputing text:\n")
    bp.indent()
    bp.bullet_text("CTRL+Left/Right to word jump.")
    bp.bullet_text("CTRL+A or double-click to select all.")
    bp.bullet_text("CTRL+X/C/V to use clipboard cut/copy/paste.")
    bp.bullet_text("CTRL+Z,CTRL+Y to undo/redo.")
    bp.bullet_text("ESCAPE to revert.")
    bp.bullet_text("You can apply arithmetic operators +,*,/ on numerical values.\nUse +- to subtract.")
    bp.unindent()
    bp.bullet_text("With keyboard navigation enabled:")
    bp.indent()
    bp.bullet_text("Arrow keys to navigate.")
    bp.bullet_text("Space to activate a widget.")
    bp.bullet_text("Return to input text into a widget.")
    bp.bullet_text("Escape to deactivate a widget, close popup, exit child window.")
    bp.bullet_text("Alt to jump to the menu layer of a window.")
    bp.bullet_text("CTRL+Tab to select a window.")
    bp.unindent()


#  Demonstrate most Dear ImGui features (this is big function!)
#  You may execute this function to experiment with the UI and understand what it does. You may then search for keywords in the code when you are interested by a specific feature.
def show_demo_window(p_open=bp.Bool(True)):

    # if show_app_documents:
    #     ShowExampleAppDocuments(show_app_documents)
    # if show_app_main_menu_bar:
    #     ShowExampleAppMainMenuBar()
    # if show_app_console:
    #     ShowExampleAppConsole(&show_app_console:
    # if show_app_log:
    #     ShowExampleAppLog(&show_app_log:
    # if show_app_layout:
    #     ShowExampleAppLayout(&show_app_layout:
    # if show_app_property_editor:
    #     ShowExampleAppPropertyEditor(&show_app_property_editor:
    # if show_app_long_text:
    #     ShowExampleAppLongText(&show_app_long_text:
    # if show_app_auto_resize:
    #     ShowExampleAppAutoResize(&show_app_auto_resize:
    # if show_app_constrained_resize:
    #     ShowExampleAppConstrainedResize(&show_app_constrained_resize:
    # if show_app_simple_overlay:
    #     ShowExampleAppSimpleOverlay(&show_app_simple_overlay:
    # if show_app_window_titles:
    #     ShowExampleAppWindowTitles(&show_app_window_titles:
    # if show_app_custom_rendering:
    #     ShowExampleAppCustomRendering(&show_app_custom_rendering:

    # if show_app_metrics)             { bp.show_metrics_window(&show_app_metrics:; }
    # if show_app_style_editor)        { bp.begin("Style Editor", &show_app_style_editor); bp.show_style_editor(); bp.end(:; }
    if show_app_about.value:
        show_about_window(show_app_about)

    window_flags = 0
    if no_titlebar.value:
        window_flags |= bp.WindowFlags.NoTitleBar
    if no_scrollbar.value:
        window_flags |= bp.WindowFlags.NoScrollbar
    if not no_menu.value:
        window_flags |= bp.WindowFlags.MenuBar
    if no_move.value:
        window_flags |= bp.WindowFlags.NoMove
    if no_resize.value:
        window_flags |= bp.WindowFlags.NoResize
    if no_collapse.value:
        window_flags |= bp.WindowFlags.NoCollapse
    if no_nav.value:
        window_flags |= bp.WindowFlags.NoNav
    if no_background.value:
        window_flags |= bp.WindowFlags.NoBackground
    if no_bring_to_front.value:
        window_flags |= bp.WindowFlags.NoBringToFrontOnFocus
    if no_close.value:
        p_open = None #  Don't pass our bool* to Begin

    #  We specify a default position/size in case there's no data in the .ini file. Typically this isn't required! We only do it to make the Demo applications a little more welcoming.
    bp.set_next_window_pos(bp.Vec2(650, 20), bp.Condition.FirstUseEver)
    bp.set_next_window_size(bp.Vec2(550, 680), bp.Condition.FirstUseEver)

    #  Main body of the Demo window starts here.
    if not bp.begin("Dear ImGui Demo", flags=window_flags):
        #  Early out if the window is collapsed, as an optimization.
        bp.end()
        return

    #  Most "big" widgets share a common width settings by default.
    # bp.push_item_width(ImGui::GetWindowWidth() * 0.65f);    #  Use 2/3 of the space for widgets and 1/3 for labels (default)
    bp.push_item_width(bp.get_font_size() * -12)              #  Use fixed width for labels (by passing a negative value), the rest goes to widgets. We choose a width proportional to our font size.

    #  Menu Bar
    if bp.begin_menu_bar():
        if bp.begin_menu("Menu"):
            # ShowExampleMenuFile()
            bp.end_menu()

        if bp.begin_menu("Examples"):
            bp.menu_item("Main menu bar", "", show_app_main_menu_bar)
            bp.menu_item("Console", "", show_app_console)
            bp.menu_item("Log", "", show_app_log)
            bp.menu_item("Simple layout", "", show_app_layout)
            bp.menu_item("Property editor", "", show_app_property_editor)
            bp.menu_item("Long text display", "", show_app_long_text)
            bp.menu_item("Auto-resizing window", "", show_app_auto_resize)
            bp.menu_item("Constrained-resizing window", "", show_app_constrained_resize)
            bp.menu_item("Simple overlay", "", show_app_simple_overlay)
            bp.menu_item("Manipulating window titles", "", show_app_window_titles)
            bp.menu_item("Custom rendering", "", show_app_custom_rendering)
            bp.menu_item("Documents", "", show_app_documents)
            bp.end_menu()

        if bp.begin_menu("Tools"):
            bp.menu_item("Metrics", "", show_app_metrics)
            bp.menu_item("Style Editor", "", show_app_style_editor)
            bp.menu_item("About Dear ImGui", "", show_app_about)
            bp.end_menu()

        bp.end_menu_bar()

    bp.text("dear imgui says hello")
    bp.spacing()

    if bp.collapsing_header("Help"):
        bp.text("ABOUT THIS DEMO:")
        bp.bullet_text("Sections below are demonstrating many aspects of the library.")
        bp.bullet_text("The \"Examples\" menu above leads to more demo contents.")
        bp.bullet_text("The \"Tools\" menu above gives access to: About Box, Style Editor,\nand Metrics (general purpose Dear ImGui debugging tool).")
        bp.separator()

        bp.text("PROGRAMMER GUIDE:")
        bp.bullet_text("See the ShowDemoWindow() code in imgui_demo.cpp. <- you are here!")
        bp.bullet_text("See comments in imgui.cpp.")
        bp.bullet_text("See example applications in the examples/ folder.")
        bp.bullet_text("Read the FAQ at http:# www.dearimgui.org/faq/")
        bp.bullet_text("Set 'io.ConfigFlags |= NavEnableKeyboard' for keyboard controls.")
        bp.bullet_text("Set 'io.ConfigFlags |= NavEnableGamepad' for gamepad controls.")
        bp.separator()

        bp.text("USER GUIDE:")
        bp.show_user_guide()

    if bp.collapsing_header("Configuration"):
        # if bp.tree_node("Configuration##2"):
        #     bp.checkbox_flags("io.ConfigFlags: NavEnableKeyboard", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NavEnableKeyboard)
        #     bp.checkbox_flags("io.ConfigFlags: NavEnableGamepad", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NavEnableGamepad)
        #     bp.same_line(); HelpMarker("Required back-end to feed in gamepad inputs in io.NavInputs[] and set io.BackendFlags |= ImGuiBackendFlags_HasGamepad.\n\nRead instructions in imgui.cpp for details.")
        #     bp.checkbox_flags("io.ConfigFlags: NavEnableSetMousePos", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NavEnableSetMousePos)
        #     bp.same_line(); HelpMarker("Instruct navigation to move the mouse cursor. See comment for ImGuiConfigFlags_NavEnableSetMousePos.")
        #     bp.checkbox_flags("io.ConfigFlags: NoMouse", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NoMouse)
        #     if io.ConfigFlags & ImGuiConfigFlags_NoMouse: #  Create a way to restore this flag otherwise we could be stuck completely!
        #     {
        #         if fmodf((float)bp.get_time(), 0.40f) < 0.20f:
        #         {
        #             bp.same_line()
        #             bp.text("<<PRESS SPACE TO DISABLE>>")
        #         }
        #         if bp.is_key_pressed(ImGui::GetKeyIndex(ImGuiKey_Space)):
        #             io.ConfigFlags &= ~ImGuiConfigFlags_NoMouse
        #     }
        #     bp.checkbox_flags("io.ConfigFlags: NoMouseCursorChange", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NoMouseCursorChange)
        #     bp.same_line(); HelpMarker("Instruct back-end to not alter mouse cursor shape and visibility.")
        #     bp.checkbox("io.ConfigInputTextCursorBlink", &io.ConfigInputTextCursorBlink)
        #     bp.same_line(); HelpMarker("Set to false to disable blinking cursor, for users who consider it distracting")
        #     bp.checkbox("io.ConfigWindowsResizeFromEdges", &io.ConfigWindowsResizeFromEdges)
        #     bp.same_line(); HelpMarker("Enable resizing of windows from their edges and from the lower-left corner.\nThis requires (io.BackendFlags & ImGuiBackendFlags_HasMouseCursors) because it needs mouse cursor feedback.")
        #     bp.checkbox("io.ConfigWindowsMoveFromTitleBarOnly", &io.ConfigWindowsMoveFromTitleBarOnly)
        #     bp.checkbox("io.MouseDrawCursor", &io.MouseDrawCursor)
        #     bp.same_line(); HelpMarker("Instruct Dear ImGui to render a mouse cursor for you. Note that a mouse cursor rendered via your application GPU rendering path will feel more laggy than hardware cursor, but will be more in sync with your other visuals.\n\nSome desktop applications may use both kinds of cursors (e.g. enable software cursor only when resizing/dragging something).")
        #     bp.tree_pop()
        #     bp.separator()

        # if bp.tree_node("Backend Flags"):
        #     help_marker("Those flags are set by the back-ends (imgui_impl_xxx files) to specify their capabilities.\nHere we expose then as read-only fields to avoid breaking interactions with your back-end.")
        #     ImGuiBackendFlags backend_flags = io.BackendFlags; #  Make a local copy to avoid modifying actual back-end flags.
        #     bp.checkbox_flags("io.BackendFlags: HasGamepad", (unsigned int *)&backend_flags, ImGuiBackendFlags_HasGamepad)
        #     bp.checkbox_flags("io.BackendFlags: HasMouseCursors", (unsigned int *)&backend_flags, ImGuiBackendFlags_HasMouseCursors)
        #     bp.checkbox_flags("io.BackendFlags: HasSetMousePos", (unsigned int *)&backend_flags, ImGuiBackendFlags_HasSetMousePos)
        #     bp.checkbox_flags("io.BackendFlags: RendererHasVtxOffset", (unsigned int *)&backend_flags, ImGuiBackendFlags_RendererHasVtxOffset)
        #     bp.tree_pop()
        #     bp.separator()

        if bp.tree_node("Style"):
            help_marker("The same contents can be accessed in 'Tools->Style Editor' or by calling the ShowStyleEditor() function.")
            bp.show_style_editor()
            bp.tree_pop()
            bp.separator()

        if bp.tree_node("Capture/Logging"):
            bp.text_wrapped("The logging API redirects all text output so you can easily capture the content of a window or a block. Tree nodes can be automatically expanded.")
            help_marker("Try opening any of the contents below in this window and then click one of the \"Log To\" button.")
            # bp.log_buttons()
            bp.text_wrapped("You can also call ImGui::LogText() to output directly to the log without a visual output.")
            if bp.button("Copy \"Hello, world!\" to clipboard"):
                pass
                # bp.log_to_clipboard()
                # bp.log_text("Hello, world!")
                # bp.log_finish()
            bp.tree_pop()

    if bp.collapsing_header("Window options"):
        bp.checkbox("No titlebar", no_titlebar); bp.same_line(150)
        bp.checkbox("No scrollbar", no_scrollbar); bp.same_line(300)
        bp.checkbox("No menu", no_menu)
        bp.checkbox("No move", no_move); bp.same_line(150)
        bp.checkbox("No resize", no_resize); bp.same_line(300)
        bp.checkbox("No collapse", no_collapse)
        bp.checkbox("No close", no_close); bp.same_line(150)
        bp.checkbox("No nav", no_nav); bp.same_line(300)
        bp.checkbox("No background", no_background)
        bp.checkbox("No bring to front", no_bring_to_front)


    # #  All demo contents
    show_demo_window_widgets()
    # ShowDemoWindowLayout()
    # ShowDemoWindowPopups()
    # ShowDemoWindowColumns()
    # ShowDemoWindowMisc()

    bp.end()


check = bp.Bool(True)
e = bp.Int(0)
clicked = 0
counter = 0
item_current = bp.Int(0)
str0 = bp.String("Hello, world!")
buf = bp.String("\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e")


def show_demo_window_widgets():
    if not bp.collapsing_header("Widgets"):
        return
    global clicked
    if bp.tree_node("Basic"):
        if bp.button("Button"):
            clicked += 1
        if clicked & 1:
            bp.same_line()
            bp.text("Thanks for clicking me!")

        bp.checkbox("checkbox", check)

        bp.radio_button("radio a", e, 0); bp.same_line()
        bp.radio_button("radio b", e, 1); bp.same_line()
        bp.radio_button("radio c", e, 2)

        #  Color buttons, demonstrate using PushID() to add unique identifier in the ID stack, and changing style.
        for i in range(7):
            if i > 0:
                bp.same_line()
            bp.push_id_int(i)
            bp.push_style_color(bp.Colors.Button, bp.Vec4(i/7.0, 0.6, 0.6, 1.0))
            bp.push_style_color(bp.Colors.ButtonHovered, bp.Vec4(i/7.0, 0.7, 0.7, 1.0))
            bp.push_style_color(bp.Colors.ButtonActive, bp.Vec4(i/7.0, 0.8, 0.8, 1.0))
            bp.button("Click")
            bp.pop_style_color(3)
            bp.pop_id()

        #  Use AlignTextToFramePadding() to align text baseline to the baseline of framed elements (otherwise a Text+SameLine+Button sequence will have the text a little too high by default)
        bp.align_text_to_frame_padding()
        bp.text("Hold to repeat:")
        bp.same_line()

        #  Arrow buttons with Repeater
        spacing = bp.get_style().item_inner_spacing.x
        bp.push_button_repeat(True)

        global counter
        if bp.arrow_button("##left", bp.Direction.Left):
            counter -=1

        bp.same_line(0.0, spacing)
        if bp.arrow_button("##right", bp.Direction.Right):
            counter += 1

        bp.pop_button_repeat()
        bp.same_line()
        bp.text("%d" % counter)

        bp.text("Hover over me")
        if bp.is_item_hovered():
            bp.set_tooltip("I am a tooltip")

        bp.same_line()
        bp.text("- or me")
        if bp.is_item_hovered():
            bp.begin_tooltip()
            bp.text("I am a fancy tooltip")
            arr = [0.6, 0.1, 1.0, 0.5, 0.92, 0.1, 0.2]
            bp.plot_lines("Curve", arr)
            bp.end_tooltip()

        bp.separator()

        bp.label_text("label", "Value")

        #  Using the _simplified_ one-liner Combo() api here
        #  See "Combo" section for examples of how to use the more complete BeginCombo()/EndCombo() api.
        items = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK", "LLLLLLL", "MMMM", "OOOOOOO"]
        bp.combo("combo", item_current, items)
        bp.same_line(); help_marker("Refer to the \"Combo\" section below for an explanation of the full BeginCombo/EndCombo API, and demonstration of various flags.\n")


        #  To wire InputText() with std::string or any other custom string type,
        #  see the "Text Input > Resize Callback" section of this demo, and the misc/cpp/imgui_stdlib.h file.
        bp.input_text("input text", str0, 128)
        bp.same_line(); help_marker("USER:\nHold SHIFT or use mouse to select text.\n" "CTRL+Left/Right to word jump.\n" "CTRL+A or double-click to select all.\n" "CTRL+X,CTRL+C,CTRL+V clipboard.\n" "CTRL+Z,CTRL+Y undo/redo.\n" "ESCAPE to revert.\n\nPROGRAMMER:\nYou can use the ImGuiInputTextFlags_CallbackResize facility if you need to wire InputText() to a dynamic string type. See misc/cpp/imgui_stdlib.h for an example (this is not demonstrated in imgui_demo.cpp).")

#             char str1[128] = ""
#             bp.input_text_with_hint("input text (w/ hint)", "enter text here", str1, IM_ARRAYSIZE(str1))
#
#             int i0 = 123
#             bp.input_int("input int", &i0)
#             bp.same_line(); HelpMarker("You can apply arithmetic operators +,*,/ on numerical values.\n  e.g. [ 100 ], input \'*2\', result becomes [ 200 ]\nUse +- to subtract.\n")
#
#             float f0 = 0.001f
#             bp.input_float("input float", &f0, 0.01f, 1.0f, "%.3f")
#
#             double d0 = 999999.00000001
#             bp.input_double("input double", &d0, 0.01f, 1.0f, "%.8f")
#
#             float f1 = 1.e10f
#             bp.input_float("input scientific", &f1, 0.0f, 0.0f, "%e")
#             bp.same_line(); HelpMarker("You can input value using the scientific notation,\n  e.g. \"1e+8\" becomes \"100000000\".\n")
#
#             float vec4a[4] = { 0.10f, 0.20f, 0.30f, 0.44f }
#             bp.input_float3("input float3", vec4a)
#         }
#
#         {
#             int i1 = 50, i2 = 42
#             bp.drag_int("drag int", &i1, 1)
#             bp.same_line(); HelpMarker("Click and drag to edit value.\nHold SHIFT/ALT for faster/slower edit.\nDouble-click or CTRL+click to input value.")
#
#             bp.drag_int("drag int 0..100", &i2, 1, 0, 100, "%d%%")
#
#             float f1=1.00f, f2=0.0067f
#             bp.drag_float("drag float", &f1, 0.005f)
#             bp.drag_float("drag small float", &f2, 0.0001f, 0.0f, 0.0f, "%.06f ns")
#         }
#
#         {
#             int i1=0
#             bp.slider_int("slider int", &i1, -1, 3)
#             bp.same_line(); HelpMarker("CTRL+click to input value.")
#
#             float f1=0.123f, f2=0.0f
#             bp.slider_float("slider float", &f1, 0.0f, 1.0f, "ratio = %.3f")
#             bp.slider_float("slider float (curve)", &f2, -10.0f, 10.0f, "%.4f", 2.0f)
#
#             float angle = 0.0f
#             bp.slider_angle("slider angle", &angle)
#
#             #  Using the format string to display a name instead of an integer.
#             #  Here we completely omit '%d' from the format string, so it'll only display a name.
#             #  This technique can also be used with DragInt().
#             enum Element { Element_Fire, Element_Earth, Element_Air, Element_Water, Element_COUNT }
#             const char* element_names[Element_COUNT] = { "Fire", "Earth", "Air", "Water" }
#             int current_element = Element_Fire
#             const char* current_element_name = (current_element >= 0 && current_element < Element_COUNT) ? element_names[current_element] : "Unknown"
#             bp.slider_int("slider enum", &current_element, 0, Element_COUNT - 1, current_element_name)
#             bp.same_line(); HelpMarker("Using the format string parameter to display a name instead of the underlying integer.")
#         }
#
#         {
#             float col1[3] = { 1.0f,0.0f,0.2f }
#             float col2[4] = { 0.4f,0.7f,0.0f,0.5f }
#             bp.color_edit3("color 1", col1)
#             bp.same_line(); HelpMarker("Click on the colored square to open a color picker.\nClick and hold to use drag and drop.\nRight-click on the colored square to show options.\nCTRL+click on individual component to input value.\n")
#
#             bp.color_edit4("color 2", col2)
#         }
#
#         {
#             #  List box
#             const char* listbox_items[] = { "Apple", "Banana", "Cherry", "Kiwi", "Mango", "Orange", "Pineapple", "Strawberry", "Watermelon" }
#             int listbox_item_current = 1
#             bp.list_box("listbox\n(single select)", &listbox_item_current, listbox_items, IM_ARRAYSIZE(listbox_items), 4)
#
#             # int listbox_item_current2 = 2
#             # bp.set_next_item_width(-1)
#             # bp.list_box("##listbox2", &listbox_item_current2, listbox_items, IM_ARRAYSIZE(listbox_items), 4)
#         }

        bp.tree_pop()
#     }
#
#     #  Testing ImGuiOnceUponAFrame helper.
#     # ImGuiOnceUponAFrame once
#     # for i in range(5):
#     #     if once:
#     #         bp.text("This will be displayed only once.")
#
#     if bp.tree_node("Trees"):
#     {
#         if bp.tree_node("Basic trees"):
#         {
#             for i in range(5):
#             {
#                 #  Use SetNextItemOpen() so set the default state of a node to be open.
#                 #  We could also use TreeNodeEx() with the ImGuiTreeNodeFlags_DefaultOpen flag to achieve the same thing!
#                 if i == 0:
#                     bp.set_next_item_open(true, ImGuiCond_Once)
#
#                 if bp.tree_node((void*)(intptr_t)i, "Child %d", i):
#                 {
#                     bp.text("blah blah")
#                     bp.same_line()
#                     if bp.small_button("button"): {}
#                     bp.tree_pop()
#                 }
#             }
#             bp.tree_pop()
#         }
#
#         if bp.tree_node("Advanced, with Selectable nodes"):
#         {
#             HelpMarker("This is a more typical looking tree with selectable nodes.\nClick to select, CTRL+Click to toggle, click on arrows or double-click to open.")
#             ImGuiTreeNodeFlags base_flags = ImGuiTreeNodeFlags_OpenOnArrow | ImGuiTreeNodeFlags_OpenOnDoubleClick | ImGuiTreeNodeFlags_SpanAvailWidth
#             bool align_label_with_current_x_position = false
#             bp.checkbox_flags("ImGuiTreeNodeFlags_OpenOnArrow", (unsigned int*)&base_flags, ImGuiTreeNodeFlags_OpenOnArrow)
#             bp.checkbox_flags("ImGuiTreeNodeFlags_OpenOnDoubleClick", (unsigned int*)&base_flags, ImGuiTreeNodeFlags_OpenOnDoubleClick)
#             bp.checkbox_flags("ImGuiTreeNodeFlags_SpanAvailWidth", (unsigned int*)&base_flags, ImGuiTreeNodeFlags_SpanAvailWidth)
#             bp.checkbox_flags("ImGuiTreeNodeFlags_SpanFullWidth", (unsigned int*)&base_flags, ImGuiTreeNodeFlags_SpanFullWidth)
#             bp.checkbox("Align label with current X position)", &align_label_with_current_x_position)
#             bp.text("Hello!")
#             if align_label_with_current_x_position:
#                 bp.unindent(ImGui::GetTreeNodeToLabelSpacing())
#
#             int selection_mask = (1 << 2); #  Dumb representation of what may be user-side selection state. You may carry selection state inside or outside your objects in whatever format you see fit.
#             int node_clicked = -1;                #  Temporary storage of what node we have clicked to process selection at the end of the loop. May be a pointer to your own node type, etc.
#             for i in range(6):
#             {
#                 #  Disable the default open on single-click behavior and pass in Selected flag according to our selection state.
#                 ImGuiTreeNodeFlags node_flags = base_flags
#                 const bool is_selected = (selection_mask & (1 << i)) != 0
#                 if is_selected:
#                     node_flags |= ImGuiTreeNodeFlags_Selected
#                 if i < 3:
#                 {
#                     #  Items 0..2 are Tree Node
#                     bool node_open = bp.tree_node_ex((void*)(intptr_t)i, node_flags, "Selectable Node %d", i)
#                     if bp.is_item_clicked():
#                         node_clicked = i
#                     if node_open:
#                     {
#                         bp.bullet_text("Blah blah\nBlah Blah")
#                         bp.tree_pop()
#                     }
#                 }
#                 else
#                 {
#                     #  Items 3..5 are Tree Leaves
#                     #  The only reason we use TreeNode at all is to allow selection of the leaf.
#                     #  Otherwise we can use BulletText() or advance the cursor by GetTreeNodeToLabelSpacing() and call Text().
#                     node_flags |= ImGuiTreeNodeFlags_Leaf | ImGuiTreeNodeFlags_NoTreePushOnOpen; #  ImGuiTreeNodeFlags_Bullet
#                     bp.tree_node_ex((void*)(intptr_t)i, node_flags, "Selectable Leaf %d", i)
#                     if bp.is_item_clicked():
#                         node_clicked = i
#                 }
#             }
#             if node_clicked != -1:
#             {
#                 #  Update selection state. Process outside of tree loop to avoid visual inconsistencies during the clicking-frame.
#                 if bp.get_i_o().KeyCtrl:
#                     selection_mask ^= (1 << node_clicked);          #  CTRL+click to toggle
#                 else # if !(selection_mask & (1 << node_clicked)): #  Depending on selection behavior you want, this commented bit preserve selection when clicking on item that is part of the selection
#                     selection_mask = (1 << node_clicked);           #  Click to single-select
#             }
#             if align_label_with_current_x_position:
#                 bp.indent(ImGui::GetTreeNodeToLabelSpacing())
#             bp.tree_pop()
#         }
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Collapsing Headers"):
#     {
#         bool closable_group = true
#         bp.checkbox("Show 2nd header", &closable_group)
#         if bp.collapsing_header("Header", ImGuiTreeNodeFlags_None):
#         {
#             bp.text("IsItemHovered: %d", ImGui::IsItemHovered())
#             for i in range(5):
#                 bp.text("Some content %d", i)
#         }
#         if bp.collapsing_header("Header with a close button", &closable_group):
#         {
#             bp.text("IsItemHovered: %d", ImGui::IsItemHovered())
#             for i in range(5):
#                 bp.text("More content %d", i)
#         }
#         /*
#         if bp.collapsing_header("Header with a bullet", ImGuiTreeNodeFlags_Bullet):
#             bp.text("IsItemHovered: %d", ImGui::IsItemHovered())
#         */
#         bp.tree_pop()
#     }

    if bp.tree_node("Bullets"):
        bp.bullet_text("Bullet point 1")
        bp.bullet_text("Bullet point 2\nOn multiple lines")
        if bp.tree_node("Tree node"):
            bp.bullet_text("Another bullet point")
            bp.tree_pop()
        bp.bullet(); bp.text("Bullet point 3 (two calls)")
        bp.bullet(); bp.small_button("Button")
        bp.tree_pop()

    if bp.tree_node("Text"):
        if bp.tree_node("Colored Text"):
            #  Using shortcut. You can use PushStyleColor()/PopStyleColor() for more flexibility.
            bp.text_colored(bp.Vec4(1.0,0.0,1.0,1.0), "Pink")
            bp.text_colored(bp.Vec4(1.0,1.0,0.0,1.0), "Yellow")
            bp.text_disabled("Disabled")
            bp.same_line(); help_marker("The TextDisabled color is stored in ImGuiStyle.")
            bp.tree_pop()

#         if bp.tree_node("Word Wrapping"):
#         {
#             #  Using shortcut. You can use PushTextWrapPos()/PopTextWrapPos() for more flexibility.
#             bp.text_wrapped("This text should automatically wrap on the edge of the window. The current implementation for text wrapping follows simple rules suitable for English and possibly other languages.")
#             bp.spacing()
#
#             float wrap_width = 200.0f
#             bp.slider_float("Wrap width", &wrap_width, -20, 600, "%.0f")
#
#             bp.text("Test paragraph 1:")
#             ImVec2 pos = bp.get_cursor_screen_pos()
#             bp.get_window_draw_list()->AddRectFilled(ImVec2(pos.x + wrap_width, pos.y), ImVec2(pos.x + wrap_width + 10, pos.y + bp.get_text_line_height()), IM_COL32(255,0,255,255))
#             bp.push_text_wrap_pos(ImGui::GetCursorPos().x + wrap_width)
#             bp.text("The lazy dog is a good dog. This paragraph is made to fit within %.0f pixels. Testing a 1 character word. The quick brown fox jumps over the lazy dog.", wrap_width)
#             bp.get_window_draw_list()->AddRect(bp.get_item_rect_min(), bp.get_item_rect_max(), IM_COL32(255,255,0,255))
#             bp.pop_text_wrap_pos()
#
#             bp.text("Test paragraph 2:")
#             pos = bp.get_cursor_screen_pos()
#             bp.get_window_draw_list()->AddRectFilled(ImVec2(pos.x + wrap_width, pos.y), ImVec2(pos.x + wrap_width + 10, pos.y + bp.get_text_line_height()), IM_COL32(255,0,255,255))
#             bp.push_text_wrap_pos(ImGui::GetCursorPos().x + wrap_width)
#             bp.text("aaaaaaaa bbbbbbbb, c cccccccc,dddddddd. d eeeeeeee   ffffffff. gggggggg!hhhhhhhh")
#             bp.get_window_draw_list()->AddRect(bp.get_item_rect_min(), bp.get_item_rect_max(), IM_COL32(255,255,0,255))
#             bp.pop_text_wrap_pos()
#
#             bp.tree_pop()
#         }

        if bp.tree_node("UTF-8 Text"):
            #  UTF-8 test with Japanese characters
            #  (Needs a suitable font, try Noto, or Arial Unicode, or M+ fonts. Read docs/FONTS.txt for details.)
            #  - From C++11 you can use the u8"my text" syntax to encode literal strings as UTF-8
            #  - For earlier compiler, you may be able to encode your sources as UTF-8 (e.g. Visual Studio save your file as 'UTF-8 without signature')
            #  - FOR THIS DEMO FILE ONLY, BECAUSE WE WANT TO SUPPORT OLD COMPILERS, WE ARE *NOT* INCLUDING RAW UTF-8 CHARACTERS IN THIS SOURCE FILE.
            #    Instead we are encoding a few strings with hexadecimal constants. Don't do this in your application!
            #    Please use u8"text in any language" in your application!
            #  Note that characters values are preserved even by InputText() if the font cannot be displayed, so you can safely copy & paste garbled characters into another application.
            bp.text_wrapped("CJK text will only appears if the font was loaded with the appropriate CJK character ranges. Call io.Font->AddFontFromFileTTF() manually to load extra character ranges. Read docs/FONTS.txt for details.")
            bp.text("Hiragana: \xe3\x81\x8b\xe3\x81\x8d\xe3\x81\x8f\xe3\x81\x91\xe3\x81\x93 (kakikukeko)"); #  Normally we would use u8"blah blah" with the proper characters directly in the string.
            bp.text("Kanjis: \xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e (nihongo)")
            bp.input_text("UTF-8 input", buf, 128)
            bp.tree_pop()
        bp.tree_pop()

#     if bp.tree_node("Images"):
#     {
#         ImGuiIO& io = bp.get_i_o()
#         bp.text_wrapped("Below we are displaying the font texture (which is the only texture we have access to in this demo). Use the 'ImTextureID' type as storage to pass pointers or identifier to your own texture data. Hover the texture for a zoomed view!")
#
#         #  Here we are grabbing the font texture because that's the only one we have access to inside the demo code.
#         #  Remember that ImTextureID is just storage for whatever you want it to be, it is essentially a value that will be passed to the render function inside the ImDrawCmd structure.
#         #  If you use one of the default imgui_impl_XXXX.cpp renderer, they all have comments at the top of their file to specify what they expect to be stored in ImTextureID.
#         #  (for example, the imgui_impl_dx11.cpp renderer expect a 'ID3D11ShaderResourceView*' pointer. The imgui_impl_opengl3.cpp renderer expect a GLuint OpenGL texture identifier etc.)
#         #  If you decided that ImTextureID = MyEngineTexture*, then you can pass your MyEngineTexture* pointers to bp.image(), and gather width/height through your own functions, etc.
#         #  Using ShowMetricsWindow() as a "debugger" to inspect the draw data that are being passed to your render will help you debug issues if you are confused about this.
#         #  Consider using the lower-level ImDrawList::AddImage() API, via bp.get_window_draw_list()->AddImage().
#         ImTextureID my_tex_id = io.Fonts->TexID
#         float my_tex_w = (float)io.Fonts->TexWidth
#         float my_tex_h = (float)io.Fonts->TexHeight
#
#         bp.text("%.0fx%.0f", my_tex_w, my_tex_h)
#         ImVec2 pos = bp.get_cursor_screen_pos()
#         bp.image(my_tex_id, ImVec2(my_tex_w, my_tex_h), ImVec2(0,0), ImVec2(1,1), ImVec4(1.0f,1.0f,1.0f,1.0f), ImVec4(1.0f,1.0f,1.0f,0.5f))
#         if bp.is_item_hovered():
#         {
#             bp.begin_tooltip()
#             float region_sz = 32.0f
#             float region_x = io.MousePos.x - pos.x - region_sz * 0.5f; if region_x < 0.0f) region_x = 0.0f; else if (region_x > my_tex_w - region_sz: region_x = my_tex_w - region_sz
#             float region_y = io.MousePos.y - pos.y - region_sz * 0.5f; if region_y < 0.0f) region_y = 0.0f; else if (region_y > my_tex_h - region_sz: region_y = my_tex_h - region_sz
#             float zoom = 4.0f
#             bp.text("Min: (%.2f, %.2f)", region_x, region_y)
#             bp.text("Max: (%.2f, %.2f)", region_x + region_sz, region_y + region_sz)
#             ImVec2 uv0 = ImVec2((region_x) / my_tex_w, (region_y) / my_tex_h)
#             ImVec2 uv1 = ImVec2((region_x + region_sz) / my_tex_w, (region_y + region_sz) / my_tex_h)
#             bp.image(my_tex_id, ImVec2(region_sz * zoom, region_sz * zoom), uv0, uv1, ImVec4(1.0f, 1.0f, 1.0f, 1.0f), ImVec4(1.0f, 1.0f, 1.0f, 0.5f))
#             bp.end_tooltip()
#         }
#         bp.text_wrapped("And now some textured buttons..")
#         int pressed_count = 0
#         for i in range(8):
#         {
#             bp.push_i_d(i)
#             int frame_padding = -1 + i;     #  -1 = uses default padding
#             if bp.image_button(my_tex_id, ImVec2(32,32), ImVec2(0,0), ImVec2(32.0f/my_tex_w,32/my_tex_h), frame_padding, ImVec4(0.0f,0.0f,0.0f,1.0f)):
#                 pressed_count += 1
#             bp.pop_i_d()
#             bp.same_line()
#         }
#         bp.new_line()
#         bp.text("Pressed %d times.", pressed_count)
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Combo"):
#     {
#         #  Expose flags as checkbox for the demo
#         ImGuiComboFlags flags = 0
#         bp.checkbox_flags("ImGuiComboFlags_PopupAlignLeft", (unsigned int*)&flags, ImGuiComboFlags_PopupAlignLeft)
#         bp.same_line(); HelpMarker("Only makes a difference if the popup is larger than the combo")
#         if bp.checkbox_flags("ImGuiComboFlags_NoArrowButton", (unsigned int*)&flags, ImGuiComboFlags_NoArrowButton):
#             flags &= ~ImGuiComboFlags_NoPreview;     #  Clear the other flag, as we cannot combine both
#         if bp.checkbox_flags("ImGuiComboFlags_NoPreview", (unsigned int*)&flags, ImGuiComboFlags_NoPreview):
#             flags &= ~ImGuiComboFlags_NoArrowButton; #  Clear the other flag, as we cannot combine both
#
#         #  General BeginCombo() API, you have full control over your selection data and display type.
#         #  (your selection data could be an index, a pointer to the object, an id for the object, a flag stored in the object itself, etc.)
#         const char* items[] = { "AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK", "LLLLLLL", "MMMM", "OOOOOOO" }
#         const char* item_current = items[0];            #  Here our selection is a single pointer stored outside the object.
#         if bp.begin_combo("combo 1", item_current, flags): #  The second parameter is the label previewed before opening the combo.
#         {
#             for (int n = 0; n < IM_ARRAYSIZE(items); n++)
#             {
#                 bool is_selected = (item_current == items[n])
#                 if bp.selectable(items[n], is_selected):
#                     item_current = items[n]
#                 if is_selected:
#                     bp.set_item_default_focus();   #  Set the initial focus when opening the combo (scrolling + for keyboard navigation support in the upcoming navigation branch)
#             }
#             bp.end_combo()
#         }
#
#         #  Simplified one-liner Combo() API, using values packed in a single constant string
#         int item_current_2 = 0
#         bp.combo("combo 2 (one-liner)", &item_current_2, "aaaa\0bbbb\0cccc\0dddd\0eeee\0\0")
#
#         #  Simplified one-liner Combo() using an array of const char*
#         int item_current_3 = -1; #  If the selection isn't within 0..count, Combo won't display a preview
#         bp.combo("combo 3 (array)", &item_current_3, items, IM_ARRAYSIZE(items))
#
#         #  Simplified one-liner Combo() using an accessor function
#         struct FuncHolder { bool ItemGetter(void* data, int idx, const char** out_str) { *out_str = ((const char**)data)[idx]; return true; } }
#         int item_current_4 = 0
#         bp.combo("combo 4 (function)", &item_current_4, &FuncHolder::ItemGetter, items, IM_ARRAYSIZE(items))
#
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Selectables"):
#     {
#         #  Selectable() has 2 overloads:
#         #  - The one taking "bool selected" as a read-only selection information. When Selectable() has been clicked is returns true and you can alter selection state accordingly.
#         #  - The one taking "bool* p_selected" as a read-write selection information (convenient in some cases)
#         #  The earlier is more flexible, as in real application your selection may be stored in a different manner (in flags within objects, as an external list, etc).
#         if bp.tree_node("Basic"):
#         {
#             bool selection[5] = { false, true, false, false, false }
#             bp.selectable("1. I am selectable", &selection[0])
#             bp.selectable("2. I am selectable", &selection[1])
#             bp.text("3. I am not selectable")
#             bp.selectable("4. I am selectable", &selection[3])
#             if bp.selectable("5. I am double clickable", selection[4], ImGuiSelectableFlags_AllowDoubleClick):
#                 if bp.is_mouse_double_clicked(0):
#                     selection[4] = !selection[4]
#             bp.tree_pop()
#         }
#         if bp.tree_node("Selection State: Single Selection"):
#         {
#             int selected = -1
#             for n in range(5):
#             {
#                 char buf[32]
#                 sprintf(buf, "Object %d", n)
#                 if bp.selectable(buf, selected == n):
#                     selected = n
#             }
#             bp.tree_pop()
#         }
#         if bp.tree_node("Selection State: Multiple Selection"):
#         {
#             HelpMarker("Hold CTRL and click to select multiple items.")
#             bool selection[5] = { false, false, false, false, false }
#             for n in range(5):
#             {
#                 char buf[32]
#                 sprintf(buf, "Object %d", n)
#                 if bp.selectable(buf, selection[n]):
#                 {
#                     if !bp.get_i_o().KeyCtrl:    #  Clear selection when CTRL is not held
#                         memset(selection, 0, sizeof(selection))
#                     selection[n] ^= 1
#                 }
#             }
#             bp.tree_pop()
#         }
#         if bp.tree_node("Rendering more text into the same line"):
#         {
#             #  Using the Selectable() override that takes "bool* p_selected" parameter and toggle your booleans automatically.
#             bool selected[3] = { false, false, false }
#             bp.selectable("main.c",    &selected[0]); bp.same_line(300); bp.text(" 2,345 bytes")
#             bp.selectable("Hello.cpp", &selected[1]); bp.same_line(300); bp.text("12,345 bytes")
#             bp.selectable("Hello.h",   &selected[2]); bp.same_line(300); bp.text(" 2,345 bytes")
#             bp.tree_pop()
#         }
#         if bp.tree_node("In columns"):
#         {
#             bp.columns(3, NULL, false)
#             bool selected[16] = {}
#             for i in range(16):
#             {
#                 char label[32]; sprintf(label, "Item %d", i)
#                 if bp.selectable(label, &selected[i]): {}
#                 bp.next_column()
#             }
#             bp.columns(1)
#             bp.tree_pop()
#         }
#         if bp.tree_node("Grid"):
#         {
#             bool selected[4*4] = { true, false, false, false, false, true, false, false, false, false, true, false, false, false, false, true }
#             for (int i = 0; i < 4*4; i++)
#             {
#                 bp.push_i_d(i)
#                 if bp.selectable("Sailor", &selected[i], 0, ImVec2(50,50)):
#                 {
#                     #  Note: We _unnecessarily_ test for both x/y and i here only to silence some analyzer. The second part of each test is unnecessary.
#                     int x = i % 4
#                     int y = i / 4
#                     if x > 0:           { selected[i - 1] ^= 1; }
#                     if x < 3 && i < 15: { selected[i + 1] ^= 1; }
#                     if y > 0 && i > 3:  { selected[i - 4] ^= 1; }
#                     if y < 3 && i < 12: { selected[i + 4] ^= 1; }
#                 }
#                 if (i % 4) < 3) bp.same_line(:
#                 bp.pop_i_d()
#             }
#             bp.tree_pop()
#         }
#         if bp.tree_node("Alignment"):
#         {
#             HelpMarker("Alignment applies when a selectable is larger than its text content.\nBy default, Selectables uses style.SelectableTextAlign but it can be overriden on a per-item basis using PushStyleVar().")
#             bool selected[3*3] = { true, false, true, false, true, false, true, false, true }
#             for y in range(3):
#             {
#                 for x in range(3):
#                 {
#                     ImVec2 alignment = ImVec2((float)x / 2.0f, (float)y / 2.0f)
#                     char name[32]
#                     sprintf(name, "(%.1f,%.1f)", alignment.x, alignment.y)
#                     if x > 0) bp.same_line(:
#                     bp.push_style_var(ImGuiStyleVar_SelectableTextAlign, alignment)
#                     bp.selectable(name, &selected[3*y+x], ImGuiSelectableFlags_None, ImVec2(80,80))
#                     bp.pop_style_var()
#                 }
#             }
#             bp.tree_pop()
#         }
#         bp.tree_pop()
#     }
#
#     #  To wire InputText() with std::string or any other custom string type,
#     #  see the "Text Input > Resize Callback" section of this demo, and the misc/cpp/imgui_stdlib.h file.
#     if bp.tree_node("Text Input"):
#     {
#         if bp.tree_node("Multi-line Text Input"):
#         {
#             #  Note: we are using a fixed-sized buffer for simplicity here. See ImGuiInputTextFlags_CallbackResize
#             #  and the code in misc/cpp/imgui_stdlib.h for how to setup InputText() for dynamically resizing strings.
#             char text[1024 * 16] =
#                 "/*\n"
#                 " The Pentium F00F bug, shorthand for F0 0F C7 C8,\n"
#                 " the hexadecimal encoding of one offending instruction,\n"
#                 " more formally, the invalid operand with locked CMPXCHG8B\n"
#                 " instruction bug, is a design flaw in the majority of\n"
#                 " Intel Pentium, Pentium MMX, and Pentium OverDrive\n"
#                 " processors (all in the P5 microarchitecture).\n"
#                 "*/\n\n"
#                 "label:\n"
#                 "\tlock cmpxchg8b eax\n"
#
#             ImGuiInputTextFlags flags = ImGuiInputTextFlags_AllowTabInput
#             HelpMarker("You can use the ImGuiInputTextFlags_CallbackResize facility if you need to wire InputTextMultiline() to a dynamic string type. See misc/cpp/imgui_stdlib.h for an example. (This is not demonstrated in imgui_demo.cpp because we don't want to include <string> in here)")
#             bp.checkbox_flags("ImGuiInputTextFlags_ReadOnly", (unsigned int*)&flags, ImGuiInputTextFlags_ReadOnly)
#             bp.checkbox_flags("ImGuiInputTextFlags_AllowTabInput", (unsigned int*)&flags, ImGuiInputTextFlags_AllowTabInput)
#             bp.checkbox_flags("ImGuiInputTextFlags_CtrlEnterForNewLine", (unsigned int*)&flags, ImGuiInputTextFlags_CtrlEnterForNewLine)
#             bp.input_text_multiline("##source", text, IM_ARRAYSIZE(text), ImVec2(-FLT_MIN, bp.get_text_line_height() * 16), flags)
#             bp.tree_pop()
#         }
#
#         if bp.tree_node("Filtered Text Input"):
#         {
#             char buf1[64] = ""; bp.input_text("default", buf1, 64)
#             char buf2[64] = ""; bp.input_text("decimal", buf2, 64, ImGuiInputTextFlags_CharsDecimal)
#             char buf3[64] = ""; bp.input_text("hexadecimal", buf3, 64, ImGuiInputTextFlags_CharsHexadecimal | ImGuiInputTextFlags_CharsUppercase)
#             char buf4[64] = ""; bp.input_text("uppercase", buf4, 64, ImGuiInputTextFlags_CharsUppercase)
#             char buf5[64] = ""; bp.input_text("no blank", buf5, 64, ImGuiInputTextFlags_CharsNoBlank)
#             struct TextFilters { int FilterImGuiLetters(ImGuiInputTextCallbackData* data) { if data->EventChar < 256 && strchr("imgui", (char)data->EventChar): return 0; return 1; } }
#             char buf6[64] = ""; bp.input_text("\"imgui\" letters", buf6, 64, ImGuiInputTextFlags_CallbackCharFilter, TextFilters::FilterImGuiLetters)
#
#             bp.text("Password input")
#             char bufpass[64] = "password123"
#             bp.input_text("password", bufpass, 64, ImGuiInputTextFlags_Password | ImGuiInputTextFlags_CharsNoBlank)
#             bp.same_line(); HelpMarker("Display all characters as '*'.\nDisable clipboard cut and copy.\nDisable logging.\n")
#             bp.input_text_with_hint("password (w/ hint)", "<password>", bufpass, 64, ImGuiInputTextFlags_Password | ImGuiInputTextFlags_CharsNoBlank)
#             bp.input_text("password (clear)", bufpass, 64, ImGuiInputTextFlags_CharsNoBlank)
#             bp.tree_pop()
#         }
#
#         if bp.tree_node("Resize Callback"):
#         {
#             #  To wire InputText() with std::string or any other custom string type,
#             #  you can use the ImGuiInputTextFlags_CallbackResize flag + create a custom bp.input_text() wrapper using your prefered type.
#             #  See misc/cpp/imgui_stdlib.h for an implementation of this using std::string.
#             HelpMarker("Demonstrate using ImGuiInputTextFlags_CallbackResize to wire your resizable string type to InputText().\n\nSee misc/cpp/imgui_stdlib.h for an implementation of this for std::string.")
#             struct Funcs
#             {
#                 int MyResizeCallback(ImGuiInputTextCallbackData* data)
#                 {
#                     if data->EventFlag == ImGuiInputTextFlags_CallbackResize:
#                     {
#                         ImVector<char>* my_str = (ImVector<char>*)data->UserData
#                         IM_ASSERT(my_str->begin() == data->Buf)
#                         my_str->resize(data->BufSize);  #  NB: On resizing calls, generally data->BufSize == data->BufTextLen + 1
#                         data->Buf = my_str->begin()
#                     }
#                     return 0
#                 }
#
#                 #  Tip: Because ImGui:: is a namespace you would typicall add your own function into the namespace in your own source files.
#                 #  For example, you may add a function called bp.input_text(const char* label, MyString* my_str).
#                 bool MyInputTextMultiline(const char* label, ImVector<char>* my_str, const ImVec2& size = ImVec2(0, 0), ImGuiInputTextFlags flags = 0)
#                 {
#                     IM_ASSERT((flags & ImGuiInputTextFlags_CallbackResize) == 0)
#                     return bp.input_text_multiline(label, my_str->begin(), (size_t)my_str->size(), size, flags | ImGuiInputTextFlags_CallbackResize, Funcs::MyResizeCallback, (void*)my_str)
#                 }
#             }
#
#             #  For this demo we are using ImVector as a string container.
#             #  Note that because we need to store a terminating zero character, our size/capacity are 1 more than usually reported by a typical string class.
#             ImVector<char> my_str
#             if my_str.empty():
#                 my_str.push_back(0)
#             Funcs::MyInputTextMultiline("##MyStr", &my_str, ImVec2(-FLT_MIN, bp.get_text_line_height() * 16))
#             bp.text("Data: %p\nSize: %d\nCapacity: %d", (void*)my_str.begin(), my_str.size(), my_str.capacity())
#             bp.tree_pop()
#         }
#
#         bp.tree_pop()
#     }
#
#     #  Plot/Graph widgets are currently fairly limited.
#     #  Consider writing your own plotting widget, or using a third-party one (see "Wiki->Useful Widgets", or github.com/ocornut/imgui/issues/2747)
#     if bp.tree_node("Plots Widgets"):
#     {
#         bool animate = true
#         bp.checkbox("Animate", &animate)
#
#         float arr[] = { 0.6f, 0.1f, 1.0f, 0.5f, 0.92f, 0.1f, 0.2f }
#         bp.plot_lines("Frame Times", arr, IM_ARRAYSIZE(arr))
#
#         #  Create a dummy array of contiguous float values to plot
#         #  Tip: If your float aren't contiguous but part of a structure, you can pass a pointer to your first float and the sizeof() of your structure in the Stride parameter.
#         float values[90] = {}
#         int values_offset = 0
#         double refresh_time = 0.0
#         if !animate || refresh_time == 0.0:
#             refresh_time = bp.get_time()
#         while (refresh_time < bp.get_time()) #  Create dummy data at fixed 60 hz rate for the demo
#         {
#             float phase = 0.0f
#             values[values_offset] = cosf(phase)
#             values_offset = (values_offset+1) % IM_ARRAYSIZE(values)
#             phase += 0.10f*values_offset
#             refresh_time += 1.0f/60.0f
#         }
#
#         #  Plots can display overlay texts
#         #  (in this example, we will display an average value)
#         {
#             float average = 0.0f
#             for (int n = 0; n < IM_ARRAYSIZE(values); n++)
#                 average += values[n]
#             average /= (float)IM_ARRAYSIZE(values)
#             char overlay[32]
#             sprintf(overlay, "avg %f", average)
#             bp.plot_lines("Lines", values, IM_ARRAYSIZE(values), values_offset, overlay, -1.0f, 1.0f, ImVec2(0,80))
#         }
#         bp.plot_histogram("Histogram", arr, IM_ARRAYSIZE(arr), 0, NULL, 0.0f, 1.0f, ImVec2(0,80))
#
#         #  Use functions to generate output
#         #  FIXME: This is rather awkward because current plot API only pass in indices. We probably want an API passing floats and user provide sample rate/count.
#         struct Funcs
#         {
#             float Sin(void*, int i) { return sinf(i * 0.1f); }
#             float Saw(void*, int i) { return (i & 1) ? 1.0f : -1.0f; }
#         }
#         int func_type = 0, display_count = 70
#         bp.separator()
#         bp.set_next_item_width(100)
#         bp.combo("func", &func_type, "Sin\0Saw\0")
#         bp.same_line()
#         bp.slider_int("Sample count", &display_count, 1, 400)
#         float (*func)(void*, int) = (func_type == 0) ? Funcs::Sin : Funcs::Saw
#         bp.plot_lines("Lines", func, NULL, display_count, 0, NULL, -1.0f, 1.0f, ImVec2(0,80))
#         bp.plot_histogram("Histogram", func, NULL, display_count, 0, NULL, -1.0f, 1.0f, ImVec2(0,80))
#         bp.separator()
#
#         #  Animate a simple progress bar
#         float progress = 0.0f, progress_dir = 1.0f
#         if animate:
#         {
#             progress += progress_dir * 0.4f * bp.get_i_o().DeltaTime
#             if progress >= +1.1f: { progress = +1.1f; progress_dir *= -1.0f; }
#             if progress <= -0.1f: { progress = -0.1f; progress_dir *= -1.0f; }
#         }
#
#         #  Typically we would use ImVec2(-1.0f,0.0f) or ImVec2(-FLT_MIN,0.0f) to use all available width,
#         #  or ImVec2(width,0.0f) for a specified width. ImVec2(0.0f,0.0f) uses ItemWidth.
#         bp.progress_bar(progress, ImVec2(0.0f,0.0f))
#         bp.same_line(0.0f, ImGui::GetStyle().ItemInnerSpacing.x)
#         bp.text("Progress Bar")
#
#         float progress_saturated = (progress < 0.0f) ? 0.0f : (progress > 1.0f) ? 1.0f : progress
#         char buf[32]
#         sprintf(buf, "%d/%d", (int)(progress_saturated*1753), 1753)
#         bp.progress_bar(progress, ImVec2(0.f,0.f), buf)
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Color/Picker Widgets"):
#     {
#         ImVec4 color = ImVec4(114.0f/255.0f, 144.0f/255.0f, 154.0f/255.0f, 200.0f/255.0f)
#
#         bool alpha_preview = true
#         bool alpha_half_preview = false
#         bool drag_and_drop = true
#         bool options_menu = true
#         bool hdr = false
#         bp.checkbox("With Alpha Preview", &alpha_preview)
#         bp.checkbox("With Half Alpha Preview", &alpha_half_preview)
#         bp.checkbox("With Drag and Drop", &drag_and_drop)
#         bp.checkbox("With Options Menu", &options_menu); bp.same_line(); HelpMarker("Right-click on the individual color widget to show options.")
#         bp.checkbox("With HDR", &hdr); bp.same_line(); HelpMarker("Currently all this does is to lift the 0..1 limits on dragging widgets.")
#         ImGuiColorEditFlags misc_flags = (hdr ? ImGuiColorEditFlags_HDR : 0) | (drag_and_drop ? 0 : ImGuiColorEditFlags_NoDragDrop) | (alpha_half_preview ? ImGuiColorEditFlags_AlphaPreviewHalf : (alpha_preview ? ImGuiColorEditFlags_AlphaPreview : 0)) | (options_menu ? 0 : ImGuiColorEditFlags_NoOptions)
#
#         bp.text("Color widget:")
#         bp.same_line(); HelpMarker("Click on the colored square to open a color picker.\nCTRL+click on individual component to input value.\n")
#         bp.color_edit3("MyColor##1", (float*)&color, misc_flags)
#
#         bp.text("Color widget HSV with Alpha:")
#         bp.color_edit4("MyColor##2", (float*)&color, ImGuiColorEditFlags_DisplayHSV | misc_flags)
#
#         bp.text("Color widget with Float Display:")
#         bp.color_edit4("MyColor##2f", (float*)&color, ImGuiColorEditFlags_Float | misc_flags)
#
#         bp.text("Color button with Picker:")
#         bp.same_line(); HelpMarker("With the ImGuiColorEditFlags_NoInputs flag you can hide all the slider/text inputs.\nWith the ImGuiColorEditFlags_NoLabel flag you can pass a non-empty label which will only be used for the tooltip and picker popup.")
#         bp.color_edit4("MyColor##3", (float*)&color, ImGuiColorEditFlags_NoInputs | ImGuiColorEditFlags_NoLabel | misc_flags)
#
#         bp.text("Color button with Custom Picker Popup:")
#
#         #  Generate a dummy default palette. The palette will persist and can be edited.
#         bool saved_palette_init = true
#         ImVec4 saved_palette[32] = {}
#         if saved_palette_init:
#         {
#             for (int n = 0; n < IM_ARRAYSIZE(saved_palette); n++)
#             {
#                 bp.color_convert_h_s_vto_r_g_b(n / 31.0f, 0.8f, 0.8f, saved_palette[n].x, saved_palette[n].y, saved_palette[n].z)
#                 saved_palette[n].w = 1.0f; #  Alpha
#             }
#             saved_palette_init = false
#         }
#
#         ImVec4 backup_color
#         bool open_popup = bp.color_button("MyColor##3b", color, misc_flags)
#         bp.same_line(0, ImGui::GetStyle().ItemInnerSpacing.x)
#         open_popup |= bp.button("Palette")
#         if open_popup:
#         {
#             bp.open_popup("mypicker")
#             backup_color = color
#         }
#         if bp.begin_popup("mypicker"):
#         {
#             bp.text("MY CUSTOM COLOR PICKER WITH AN AMAZING PALETTE!")
#             bp.separator()
#             bp.color_picker4("##picker", (float*)&color, misc_flags | ImGuiColorEditFlags_NoSidePreview | ImGuiColorEditFlags_NoSmallPreview)
#             bp.same_line()
#
#             bp.begin_group(); #  Lock X position
#             bp.text("Current")
#             bp.color_button("##current", color, ImGuiColorEditFlags_NoPicker | ImGuiColorEditFlags_AlphaPreviewHalf, ImVec2(60,40))
#             bp.text("Previous")
#             if bp.color_button("##previous", backup_color, ImGuiColorEditFlags_NoPicker | ImGuiColorEditFlags_AlphaPreviewHalf, ImVec2(60,40)):
#                 color = backup_color
#             bp.separator()
#             bp.text("Palette")
#             for (int n = 0; n < IM_ARRAYSIZE(saved_palette); n++)
#             {
#                 bp.push_i_d(n)
#                 if (n % 8) != 0:
#                     bp.same_line(0.0f, ImGui::GetStyle().ItemSpacing.y)
#                 if bp.color_button("##palette", saved_palette[n], ImGuiColorEditFlags_NoAlpha | ImGuiColorEditFlags_NoPicker | ImGuiColorEditFlags_NoTooltip, ImVec2(20,20)):
#                     color = ImVec4(saved_palette[n].x, saved_palette[n].y, saved_palette[n].z, color.w); #  Preserve alpha!
#
#                 #  Allow user to drop colors into each palette entry
#                 #  (Note that ColorButton is already a drag source by default, unless using ImGuiColorEditFlags_NoDragDrop)
#                 if bp.begin_drag_drop_target():
#                 {
#                     if const ImGuiPayload* payload = bp.accept_drag_drop_payload(IMGUI_PAYLOAD_TYPE_COLOR_3F):
#                         memcpy((float*)&saved_palette[n], payload->Data, sizeof(float) * 3)
#                     if const ImGuiPayload* payload = bp.accept_drag_drop_payload(IMGUI_PAYLOAD_TYPE_COLOR_4F):
#                         memcpy((float*)&saved_palette[n], payload->Data, sizeof(float) * 4)
#                     bp.end_drag_drop_target()
#                 }
#
#                 bp.pop_i_d()
#             }
#             bp.end_group()
#             bp.end_popup()
#         }
#
#         bp.text("Color button only:")
#         bp.color_button("MyColor##3c", *(ImVec4*)&color, misc_flags, ImVec2(80,80))
#
#         bp.text("Color picker:")
#         bool alpha = true
#         bool alpha_bar = true
#         bool side_preview = true
#         bool ref_color = false
#         ImVec4 ref_color_v(1.0f,0.0f,1.0f,0.5f)
#         int display_mode = 0
#         int picker_mode = 0
#         bp.checkbox("With Alpha", &alpha)
#         bp.checkbox("With Alpha Bar", &alpha_bar)
#         bp.checkbox("With Side Preview", &side_preview)
#         if side_preview:
#         {
#             bp.same_line()
#             bp.checkbox("With Ref Color", &ref_color)
#             if ref_color:
#             {
#                 bp.same_line()
#                 bp.color_edit4("##RefColor", &ref_color_v.x, ImGuiColorEditFlags_NoInputs | misc_flags)
#             }
#         }
#         bp.combo("Display Mode", &display_mode, "Auto/Current\0None\0RGB Only\0HSV Only\0Hex Only\0")
#         bp.same_line(); HelpMarker("ColorEdit defaults to displaying RGB inputs if you don't specify a display mode, but the user can change it with a right-click.\n\nColorPicker defaults to displaying RGB+HSV+Hex if you don't specify a display mode.\n\nYou can change the defaults using SetColorEditOptions().")
#         bp.combo("Picker Mode", &picker_mode, "Auto/Current\0Hue bar + SV rect\0Hue wheel + SV triangle\0")
#         bp.same_line(); HelpMarker("User can right-click the picker to change mode.")
#         ImGuiColorEditFlags flags = misc_flags
#         if !alpha)            flags |= ImGuiColorEditFlags_NoAlpha;        #  This is by default if you call ColorPicker3() instead of ColorPicker4(:
#         if alpha_bar:         flags |= ImGuiColorEditFlags_AlphaBar
#         if !side_preview:     flags |= ImGuiColorEditFlags_NoSidePreview
#         if picker_mode == 1:  flags |= ImGuiColorEditFlags_PickerHueBar
#         if picker_mode == 2:  flags |= ImGuiColorEditFlags_PickerHueWheel
#         if display_mode == 1: flags |= ImGuiColorEditFlags_NoInputs;       #  Disable all RGB/HSV/Hex displays
#         if display_mode == 2: flags |= ImGuiColorEditFlags_DisplayRGB;     #  Override display mode
#         if display_mode == 3: flags |= ImGuiColorEditFlags_DisplayHSV
#         if display_mode == 4: flags |= ImGuiColorEditFlags_DisplayHex
#         bp.color_picker4("MyColor##4", (float*)&color, flags, ref_color ? &ref_color_v.x : NULL)
#
#         bp.text("Programmatically set defaults:")
#         bp.same_line(); HelpMarker("SetColorEditOptions() is designed to allow you to set boot-time default.\nWe don't have Push/Pop functions because you can force options on a per-widget basis if needed, and the user can change non-forced ones with the options menu.\nWe don't have a getter to avoid encouraging you to persistently save values that aren't forward-compatible.")
#         if bp.button("Default: Uint8 + HSV + Hue Bar"):
#             bp.set_color_edit_options(ImGuiColorEditFlags_Uint8 | ImGuiColorEditFlags_DisplayHSV | ImGuiColorEditFlags_PickerHueBar)
#         if bp.button("Default: Float + HDR + Hue Wheel"):
#             bp.set_color_edit_options(ImGuiColorEditFlags_Float | ImGuiColorEditFlags_HDR | ImGuiColorEditFlags_PickerHueWheel)
#
#         #  HSV encoded support (to avoid RGB<>HSV round trips and singularities when S==0 or V==0)
#         ImVec4 color_stored_as_hsv(0.23f, 1.0f, 1.0f, 1.0f)
#         bp.spacing()
#         bp.text("HSV encoded colors")
#         bp.same_line(); HelpMarker("By default, colors are given to ColorEdit and ColorPicker in RGB, but ImGuiColorEditFlags_InputHSV allows you to store colors as HSV and pass them to ColorEdit and ColorPicker as HSV. This comes with the added benefit that you can manipulate hue values with the picker even when saturation or value are zero.")
#         bp.text("Color widget with InputHSV:")
#         bp.color_edit4("HSV shown as RGB##1", (float*)&color_stored_as_hsv, ImGuiColorEditFlags_DisplayRGB | ImGuiColorEditFlags_InputHSV | ImGuiColorEditFlags_Float)
#         bp.color_edit4("HSV shown as HSV##1", (float*)&color_stored_as_hsv, ImGuiColorEditFlags_DisplayHSV | ImGuiColorEditFlags_InputHSV | ImGuiColorEditFlags_Float)
#         bp.drag_float4("Raw HSV values", (float*)&color_stored_as_hsv, 0.01f, 0.0f, 1.0f)
#
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Range Widgets"):
#     {
#         float begin = 10, end = 90
#         int begin_i = 100, end_i = 1000
#         bp.drag_float_range2("range", &begin, &end, 0.25f, 0.0f, 100.0f, "Min: %.1f %%", "Max: %.1f %%")
#         bp.drag_int_range2("range int (no bounds)", &begin_i, &end_i, 5, 0, 0, "Min: %d units", "Max: %d units")
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Data Types"):
#     {
#         #  The DragScalar/InputScalar/SliderScalar functions allow various data types: signed/unsigned int/long long and float/double
#         #  To avoid polluting the public API with all possible combinations, we use the ImGuiDataType enum to pass the type,
#         #  and passing all arguments by address.
#         #  This is the reason the test code below creates local variables to hold "zero" "one" etc. for each types.
#         #  In practice, if you frequently use a given type that is not covered by the normal API entry points, you can wrap it
#         #  yourself inside a 1 line function which can take typed argument as value instead of void*, and then pass their address
#         #  to the generic function. For example:
#         #    bool MySliderU64(const char *label, u64* value, u64 min = 0, u64 max = 0, const char* format = "%lld")
#         #    {
#         #       return SliderScalar(label, ImGuiDataType_U64, value, &min, &max, format)
#         #    }
#
#         #  Limits (as helper variables that we can take the address of)
#         #  Note that the SliderScalar function has a maximum usable range of half the natural type maximum, hence the /2 below.
#         #ifndef LLONG_MIN
#         ImS64 LLONG_MIN = -9223372036854775807LL - 1
#         ImS64 LLONG_MAX = 9223372036854775807LL
#         ImU64 ULLONG_MAX = (2ULL * 9223372036854775807LL + 1)
#         #endif
#         const char    s8_zero  = 0,   s8_one  = 1,   s8_fifty  = 50, s8_min  = -128,        s8_max = 127
#         const ImU8    u8_zero  = 0,   u8_one  = 1,   u8_fifty  = 50, u8_min  = 0,           u8_max = 255
#         const short   s16_zero = 0,   s16_one = 1,   s16_fifty = 50, s16_min = -32768,      s16_max = 32767
#         const ImU16   u16_zero = 0,   u16_one = 1,   u16_fifty = 50, u16_min = 0,           u16_max = 65535
#         const ImS32   s32_zero = 0,   s32_one = 1,   s32_fifty = 50, s32_min = INT_MIN/2,   s32_max = INT_MAX/2,    s32_hi_a = INT_MAX/2 - 100,    s32_hi_b = INT_MAX/2
#         const ImU32   u32_zero = 0,   u32_one = 1,   u32_fifty = 50, u32_min = 0,           u32_max = UINT_MAX/2,   u32_hi_a = UINT_MAX/2 - 100,   u32_hi_b = UINT_MAX/2
#         const ImS64   s64_zero = 0,   s64_one = 1,   s64_fifty = 50, s64_min = LLONG_MIN/2, s64_max = LLONG_MAX/2,  s64_hi_a = LLONG_MAX/2 - 100,  s64_hi_b = LLONG_MAX/2
#         const ImU64   u64_zero = 0,   u64_one = 1,   u64_fifty = 50, u64_min = 0,           u64_max = ULLONG_MAX/2, u64_hi_a = ULLONG_MAX/2 - 100, u64_hi_b = ULLONG_MAX/2
#         const float   f32_zero = 0.f, f32_one = 1.f, f32_lo_a = -10000000000.0f, f32_hi_a = +10000000000.0f
#         const double  f64_zero = 0.,  f64_one = 1.,  f64_lo_a = -1000000000000000.0, f64_hi_a = +1000000000000000.0
#
#         #  State
#         char   s8_v  = 127
#         ImU8   u8_v  = 255
#         short  s16_v = 32767
#         ImU16  u16_v = 65535
#         ImS32  s32_v = -1
#         ImU32  u32_v = (ImU32)-1
#         ImS64  s64_v = -1
#         ImU64  u64_v = (ImU64)-1
#         float  f32_v = 0.123f
#         double f64_v = 90000.01234567890123456789
#
#         const float drag_speed = 0.2f
#         bool drag_clamp = false
#         bp.text("Drags:")
#         bp.checkbox("Clamp integers to 0..50", &drag_clamp); bp.same_line(); HelpMarker("As with every widgets in dear imgui, we never modify values unless there is a user interaction.\nYou can override the clamping limits by using CTRL+Click to input a value.")
#         bp.drag_scalar("drag s8",        ImGuiDataType_S8,     &s8_v,  drag_speed, drag_clamp ? &s8_zero  : NULL, drag_clamp ? &s8_fifty  : NULL)
#         bp.drag_scalar("drag u8",        ImGuiDataType_U8,     &u8_v,  drag_speed, drag_clamp ? &u8_zero  : NULL, drag_clamp ? &u8_fifty  : NULL, "%u ms")
#         bp.drag_scalar("drag s16",       ImGuiDataType_S16,    &s16_v, drag_speed, drag_clamp ? &s16_zero : NULL, drag_clamp ? &s16_fifty : NULL)
#         bp.drag_scalar("drag u16",       ImGuiDataType_U16,    &u16_v, drag_speed, drag_clamp ? &u16_zero : NULL, drag_clamp ? &u16_fifty : NULL, "%u ms")
#         bp.drag_scalar("drag s32",       ImGuiDataType_S32,    &s32_v, drag_speed, drag_clamp ? &s32_zero : NULL, drag_clamp ? &s32_fifty : NULL)
#         bp.drag_scalar("drag u32",       ImGuiDataType_U32,    &u32_v, drag_speed, drag_clamp ? &u32_zero : NULL, drag_clamp ? &u32_fifty : NULL, "%u ms")
#         bp.drag_scalar("drag s64",       ImGuiDataType_S64,    &s64_v, drag_speed, drag_clamp ? &s64_zero : NULL, drag_clamp ? &s64_fifty : NULL)
#         bp.drag_scalar("drag u64",       ImGuiDataType_U64,    &u64_v, drag_speed, drag_clamp ? &u64_zero : NULL, drag_clamp ? &u64_fifty : NULL)
#         bp.drag_scalar("drag float",     ImGuiDataType_Float,  &f32_v, 0.005f,  &f32_zero, &f32_one, "%f", 1.0f)
#         bp.drag_scalar("drag float ^2",  ImGuiDataType_Float,  &f32_v, 0.005f,  &f32_zero, &f32_one, "%f", 2.0f); bp.same_line(); HelpMarker("You can use the 'power' parameter to increase tweaking precision on one side of the range.")
#         bp.drag_scalar("drag double",    ImGuiDataType_Double, &f64_v, 0.0005f, &f64_zero, NULL,     "%.10f grams", 1.0f)
#         bp.drag_scalar("drag double ^2", ImGuiDataType_Double, &f64_v, 0.0005f, &f64_zero, &f64_one, "0 < %.10f < 1", 2.0f)
#
#         bp.text("Sliders")
#         bp.slider_scalar("slider s8 full",     ImGuiDataType_S8,     &s8_v,  &s8_min,   &s8_max,   "%d")
#         bp.slider_scalar("slider u8 full",     ImGuiDataType_U8,     &u8_v,  &u8_min,   &u8_max,   "%u")
#         bp.slider_scalar("slider s16 full",    ImGuiDataType_S16,    &s16_v, &s16_min,  &s16_max,  "%d")
#         bp.slider_scalar("slider u16 full",    ImGuiDataType_U16,    &u16_v, &u16_min,  &u16_max,  "%u")
#         bp.slider_scalar("slider s32 low",     ImGuiDataType_S32,    &s32_v, &s32_zero, &s32_fifty,"%d")
#         bp.slider_scalar("slider s32 high",    ImGuiDataType_S32,    &s32_v, &s32_hi_a, &s32_hi_b, "%d")
#         bp.slider_scalar("slider s32 full",    ImGuiDataType_S32,    &s32_v, &s32_min,  &s32_max,  "%d")
#         bp.slider_scalar("slider u32 low",     ImGuiDataType_U32,    &u32_v, &u32_zero, &u32_fifty,"%u")
#         bp.slider_scalar("slider u32 high",    ImGuiDataType_U32,    &u32_v, &u32_hi_a, &u32_hi_b, "%u")
#         bp.slider_scalar("slider u32 full",    ImGuiDataType_U32,    &u32_v, &u32_min,  &u32_max,  "%u")
#         bp.slider_scalar("slider s64 low",     ImGuiDataType_S64,    &s64_v, &s64_zero, &s64_fifty,"%I64d")
#         bp.slider_scalar("slider s64 high",    ImGuiDataType_S64,    &s64_v, &s64_hi_a, &s64_hi_b, "%I64d")
#         bp.slider_scalar("slider s64 full",    ImGuiDataType_S64,    &s64_v, &s64_min,  &s64_max,  "%I64d")
#         bp.slider_scalar("slider u64 low",     ImGuiDataType_U64,    &u64_v, &u64_zero, &u64_fifty,"%I64u ms")
#         bp.slider_scalar("slider u64 high",    ImGuiDataType_U64,    &u64_v, &u64_hi_a, &u64_hi_b, "%I64u ms")
#         bp.slider_scalar("slider u64 full",    ImGuiDataType_U64,    &u64_v, &u64_min,  &u64_max,  "%I64u ms")
#         bp.slider_scalar("slider float low",   ImGuiDataType_Float,  &f32_v, &f32_zero, &f32_one)
#         bp.slider_scalar("slider float low^2", ImGuiDataType_Float,  &f32_v, &f32_zero, &f32_one,  "%.10f", 2.0f)
#         bp.slider_scalar("slider float high",  ImGuiDataType_Float,  &f32_v, &f32_lo_a, &f32_hi_a, "%e")
#         bp.slider_scalar("slider double low",  ImGuiDataType_Double, &f64_v, &f64_zero, &f64_one,  "%.10f grams", 1.0f)
#         bp.slider_scalar("slider double low^2",ImGuiDataType_Double, &f64_v, &f64_zero, &f64_one,  "%.10f", 2.0f)
#         bp.slider_scalar("slider double high", ImGuiDataType_Double, &f64_v, &f64_lo_a, &f64_hi_a, "%e grams", 1.0f)
#
#         bool inputs_step = true
#         bp.text("Inputs")
#         bp.checkbox("Show step buttons", &inputs_step)
#         bp.input_scalar("input s8",      ImGuiDataType_S8,     &s8_v,  inputs_step ? &s8_one  : NULL, NULL, "%d")
#         bp.input_scalar("input u8",      ImGuiDataType_U8,     &u8_v,  inputs_step ? &u8_one  : NULL, NULL, "%u")
#         bp.input_scalar("input s16",     ImGuiDataType_S16,    &s16_v, inputs_step ? &s16_one : NULL, NULL, "%d")
#         bp.input_scalar("input u16",     ImGuiDataType_U16,    &u16_v, inputs_step ? &u16_one : NULL, NULL, "%u")
#         bp.input_scalar("input s32",     ImGuiDataType_S32,    &s32_v, inputs_step ? &s32_one : NULL, NULL, "%d")
#         bp.input_scalar("input s32 hex", ImGuiDataType_S32,    &s32_v, inputs_step ? &s32_one : NULL, NULL, "%08X", ImGuiInputTextFlags_CharsHexadecimal)
#         bp.input_scalar("input u32",     ImGuiDataType_U32,    &u32_v, inputs_step ? &u32_one : NULL, NULL, "%u")
#         bp.input_scalar("input u32 hex", ImGuiDataType_U32,    &u32_v, inputs_step ? &u32_one : NULL, NULL, "%08X", ImGuiInputTextFlags_CharsHexadecimal)
#         bp.input_scalar("input s64",     ImGuiDataType_S64,    &s64_v, inputs_step ? &s64_one : NULL)
#         bp.input_scalar("input u64",     ImGuiDataType_U64,    &u64_v, inputs_step ? &u64_one : NULL)
#         bp.input_scalar("input float",   ImGuiDataType_Float,  &f32_v, inputs_step ? &f32_one : NULL)
#         bp.input_scalar("input double",  ImGuiDataType_Double, &f64_v, inputs_step ? &f64_one : NULL)
#
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Multi-component Widgets"):
#     {
#         float vec4f[4] = { 0.10f, 0.20f, 0.30f, 0.44f }
#         int vec4i[4] = { 1, 5, 100, 255 }
#
#         bp.input_float2("input float2", vec4f)
#         bp.drag_float2("drag float2", vec4f, 0.01f, 0.0f, 1.0f)
#         bp.slider_float2("slider float2", vec4f, 0.0f, 1.0f)
#         bp.input_int2("input int2", vec4i)
#         bp.drag_int2("drag int2", vec4i, 1, 0, 255)
#         bp.slider_int2("slider int2", vec4i, 0, 255)
#         bp.spacing()
#
#         bp.input_float3("input float3", vec4f)
#         bp.drag_float3("drag float3", vec4f, 0.01f, 0.0f, 1.0f)
#         bp.slider_float3("slider float3", vec4f, 0.0f, 1.0f)
#         bp.input_int3("input int3", vec4i)
#         bp.drag_int3("drag int3", vec4i, 1, 0, 255)
#         bp.slider_int3("slider int3", vec4i, 0, 255)
#         bp.spacing()
#
#         bp.input_float4("input float4", vec4f)
#         bp.drag_float4("drag float4", vec4f, 0.01f, 0.0f, 1.0f)
#         bp.slider_float4("slider float4", vec4f, 0.0f, 1.0f)
#         bp.input_int4("input int4", vec4i)
#         bp.drag_int4("drag int4", vec4i, 1, 0, 255)
#         bp.slider_int4("slider int4", vec4i, 0, 255)
#
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Vertical Sliders"):
#     {
#         const float spacing = 4
#         bp.push_style_var(ImGuiStyleVar_ItemSpacing, ImVec2(spacing, spacing))
#
#         int int_value = 0
#         bp.v_slider_int("##int", ImVec2(18,160), &int_value, 0, 5)
#         bp.same_line()
#
#         float values[7] = { 0.0f, 0.60f, 0.35f, 0.9f, 0.70f, 0.20f, 0.0f }
#         bp.push_i_d("set1")
#         for i in range(7):
#         {
#             if i > 0) bp.same_line(:
#             bp.push_i_d(i)
#             bp.push_style_color(ImGuiCol_FrameBg, (ImVec4)ImColor::HSV(i/7.0f, 0.5f, 0.5f))
#             bp.push_style_color(ImGuiCol_FrameBgHovered, (ImVec4)ImColor::HSV(i/7.0f, 0.6f, 0.5f))
#             bp.push_style_color(ImGuiCol_FrameBgActive, (ImVec4)ImColor::HSV(i/7.0f, 0.7f, 0.5f))
#             bp.push_style_color(ImGuiCol_SliderGrab, (ImVec4)ImColor::HSV(i/7.0f, 0.9f, 0.9f))
#             bp.v_slider_float("##v", ImVec2(18,160), &values[i], 0.0f, 1.0f, "")
#             if bp.is_item_active() || bp.is_item_hovered():
#                 bp.set_tooltip("%.3f", values[i])
#             bp.pop_style_color(4)
#             bp.pop_i_d()
#         }
#         bp.pop_i_d()
#
#         bp.same_line()
#         bp.push_i_d("set2")
#         float values2[4] = { 0.20f, 0.80f, 0.40f, 0.25f }
#         const int rows = 3
#         const ImVec2 small_slider_size(18, (float)(int)((160.0f - (rows - 1) * spacing) / rows))
#         for nx in range(4):
#         {
#             if nx > 0) bp.same_line(:
#             bp.begin_group()
#             for ny in range(rows):
#             {
#                 bp.push_i_d(nx*rows+ny)
#                 bp.v_slider_float("##v", small_slider_size, &values2[nx], 0.0f, 1.0f, "")
#                 if bp.is_item_active() || bp.is_item_hovered():
#                     bp.set_tooltip("%.3f", values2[nx])
#                 bp.pop_i_d()
#             }
#             bp.end_group()
#         }
#         bp.pop_i_d()
#
#         bp.same_line()
#         bp.push_i_d("set3")
#         for i in range(4):
#         {
#             if i > 0) bp.same_line(:
#             bp.push_i_d(i)
#             bp.push_style_var(ImGuiStyleVar_GrabMinSize, 40)
#             bp.v_slider_float("##v", ImVec2(40,160), &values[i], 0.0f, 1.0f, "%.2f\nsec")
#             bp.pop_style_var()
#             bp.pop_i_d()
#         }
#         bp.pop_i_d()
#         bp.pop_style_var()
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Drag and Drop"):
#     {
#         if bp.tree_node("Drag and drop in standard widgets"):
#         {
#             #  ColorEdit widgets automatically act as drag source and drag target.
#             #  They are using standardized payload strings IMGUI_PAYLOAD_TYPE_COLOR_3F and IMGUI_PAYLOAD_TYPE_COLOR_4F to allow your own widgets
#             #  to use colors in their drag and drop interaction. Also see the demo in Color Picker -> Palette demo.
#             HelpMarker("You can drag from the colored squares.")
#             float col1[3] = { 1.0f, 0.0f, 0.2f }
#             float col2[4] = { 0.4f, 0.7f, 0.0f, 0.5f }
#             bp.color_edit3("color 1", col1)
#             bp.color_edit4("color 2", col2)
#             bp.tree_pop()
#         }
#
#         if bp.tree_node("Drag and drop to copy/swap items"):
#         {
#             enum Mode
#             {
#                 Mode_Copy,
#                 Mode_Move,
#                 Mode_Swap
#             }
#             int mode = 0
#             if bp.radio_button("Copy", mode == Mode_Copy)) { mode = Mode_Copy; } bp.same_line(:
#             if bp.radio_button("Move", mode == Mode_Move)) { mode = Mode_Move; } bp.same_line(:
#             if bp.radio_button("Swap", mode == Mode_Swap): { mode = Mode_Swap; }
#             const char* names[9] = { "Bobby", "Beatrice", "Betty", "Brianna", "Barry", "Bernard", "Bibi", "Blaine", "Bryn" }
#             for (int n = 0; n < IM_ARRAYSIZE(names); n++)
#             {
#                 bp.push_i_d(n)
#                 if (n % 3) != 0:
#                     bp.same_line()
#                 bp.button(names[n], ImVec2(60,60))
#
#                 #  Our buttons are both drag sources and drag targets here!
#                 if bp.begin_drag_drop_source(ImGuiDragDropFlags_None):
#                 {
#                     bp.set_drag_drop_payload("DND_DEMO_CELL", &n, sizeof(int));    #  Set payload to carry the index of our item (could be anything)
#                     if mode == Mode_Copy) { bp.text("Copy %s", names[n]); }    #  Display preview (could be anything, e.g. when dragging an image we could decide to display the filename and a small preview of the image, etc.:
#                     if mode == Mode_Move) { bp.text("Move %s", names[n]:; }
#                     if mode == Mode_Swap) { bp.text("Swap %s", names[n]:; }
#                     bp.end_drag_drop_source()
#                 }
#                 if bp.begin_drag_drop_target():
#                 {
#                     if const ImGuiPayload* payload = bp.accept_drag_drop_payload("DND_DEMO_CELL"):
#                     {
#                         IM_ASSERT(payload->DataSize == sizeof(int))
#                         int payload_n = *(const int*)payload->Data
#                         if mode == Mode_Copy:
#                         {
#                             names[n] = names[payload_n]
#                         }
#                         if mode == Mode_Move:
#                         {
#                             names[n] = names[payload_n]
#                             names[payload_n] = ""
#                         }
#                         if mode == Mode_Swap:
#                         {
#                             const char* tmp = names[n]
#                             names[n] = names[payload_n]
#                             names[payload_n] = tmp
#                         }
#                     }
#                     bp.end_drag_drop_target()
#                 }
#                 bp.pop_i_d()
#             }
#             bp.tree_pop()
#         }
#
#         if bp.tree_node("Drag to reorder items (simple)"):
#         {
#             #  Simple reordering
#             HelpMarker("We don't use the drag and drop api at all here! Instead we query when the item is held but not hovered, and order items accordingly.")
#             const char* item_names[] = { "Item One", "Item Two", "Item Three", "Item Four", "Item Five" }
#             for (int n = 0; n < IM_ARRAYSIZE(item_names); n++)
#             {
#                 const char* item = item_names[n]
#                 bp.selectable(item)
#
#                 if bp.is_item_active() && !bp.is_item_hovered():
#                 {
#                     int n_next = n + (bp.get_mouse_drag_delta(0).y < 0.f ? -1 : 1)
#                     if n_next >= 0 && n_next < IM_ARRAYSIZE(item_names):
#                     {
#                         item_names[n] = item_names[n_next]
#                         item_names[n_next] = item
#                         bp.reset_mouse_drag_delta()
#                     }
#                 }
#             }
#             bp.tree_pop()
#         }
#
#         bp.tree_pop()
#     }
#
#     if bp.tree_node("Querying Status (Active/Focused/Hovered etc.)"):
#     {
#         #  Submit an item (various types available) so we can query their status in the following block.
#         int item_type = 1
#         bp.combo("Item Type", &item_type, "Text\0Button\0Button (w/ repeat)\0Checkbox\0SliderFloat\0InputText\0InputFloat\0InputFloat3\0ColorEdit4\0MenuItem\0TreeNode\0TreeNode (w/ double-click)\0ListBox\0", 20)
#         bp.same_line()
#         HelpMarker("Testing how various types of items are interacting with the IsItemXXX functions.")
#         bool ret = false
#         bool b = false
#         float col4f[4] = { 1.0f, 0.5, 0.0f, 1.0f }
#         char str[16] = {}
#         if item_type == 0) { bp.text("ITEM: Text":; }                                              #  Testing text items with no identifier/interaction
#         if item_type == 1) { ret = bp.button("ITEM: Button":; }                                    #  Testing button
#         if item_type == 2) { bp.push_button_repeat(true); ret = bp.button("ITEM: Button"); bp.pop_button_repeat(); } #  Testing button (with repeater:
#         if item_type == 3) { ret = bp.checkbox("ITEM: Checkbox", &b:; }                            #  Testing checkbox
#         if item_type == 4) { ret = bp.slider_float("ITEM: SliderFloat", &col4f[0], 0.0f, 1.0f:; }   #  Testing basic item
#         if item_type == 5) { ret = bp.input_text("ITEM: InputText", &str[0], IM_ARRAYSIZE(str)); }  #  Testing input text (which handles tabbing:
#         if item_type == 6) { ret = bp.input_float("ITEM: InputFloat", col4f, 1.0f:; }               #  Testing +/- buttons on scalar input
#         if item_type == 7) { ret = bp.input_float3("ITEM: InputFloat3", col4f); }                   #  Testing multi-component items (IsItemXXX flags are reported merged:
#         if item_type == 8) { ret = bp.color_edit4("ITEM: ColorEdit4", col4f); }                     #  Testing multi-component items (IsItemXXX flags are reported merged:
#         if item_type == 9) { ret = bp.menu_item("ITEM: MenuItem"); }                                #  Testing menu item (they use ImGuiButtonFlags_PressedOnRelease button policy:
#         if item_type == 10){ ret = bp.tree_node("ITEM: TreeNode"); if (ret) bp.tree_pop(:; }     #  Testing tree node
#         if item_type == 11){ ret = bp.tree_node_ex("ITEM: TreeNode w/ ImGuiTreeNodeFlags_OpenOnDoubleClick", ImGuiTreeNodeFlags_OpenOnDoubleClick | ImGuiTreeNodeFlags_NoTreePushOnOpen:; } #  Testing tree node with ImGuiButtonFlags_PressedOnDoubleClick button policy.
#         if item_type == 12){ const char* items[] = { "Apple", "Banana", "Cherry", "Kiwi" }; int current = 1; ret = bp.list_box("ITEM: ListBox", &current, items, IM_ARRAYSIZE(items), IM_ARRAYSIZE(items):; }
#
#         #  Display the value of IsItemHovered() and other common item state functions.
#         #  Note that the ImGuiHoveredFlags_XXX flags can be combined.
#         #  Because BulletText is an item itself and that would affect the output of IsItemXXX functions,
#         #  we query every state in a single call to avoid storing them and to simplify the code
#         ImGui::BulletText(
#             "Return value = %d\n"
#             "IsItemFocused() = %d\n"
#             "IsItemHovered() = %d\n"
#             "IsItemHovered(_AllowWhenBlockedByPopup) = %d\n"
#             "IsItemHovered(_AllowWhenBlockedByActiveItem) = %d\n"
#             "IsItemHovered(_AllowWhenOverlapped) = %d\n"
#             "IsItemHovered(_RectOnly) = %d\n"
#             "IsItemActive() = %d\n"
#             "IsItemEdited() = %d\n"
#             "IsItemActivated() = %d\n"
#             "IsItemDeactivated() = %d\n"
#             "IsItemDeactivatedAfterEdit() = %d\n"
#             "IsItemVisible() = %d\n"
#             "IsItemClicked() = %d\n"
#             "IsItemToggledOpen() = %d\n"
#             "GetItemRectMin() = (%.1f, %.1f)\n"
#             "GetItemRectMax() = (%.1f, %.1f)\n"
#             "GetItemRectSize() = (%.1f, %.1f)",
#             ret,
#             bp.is_item_focused(),
#             bp.is_item_hovered(),
#             bp.is_item_hovered(ImGuiHoveredFlags_AllowWhenBlockedByPopup),
#             bp.is_item_hovered(ImGuiHoveredFlags_AllowWhenBlockedByActiveItem),
#             bp.is_item_hovered(ImGuiHoveredFlags_AllowWhenOverlapped),
#             bp.is_item_hovered(ImGuiHoveredFlags_RectOnly),
#             bp.is_item_active(),
#             bp.is_item_edited(),
#             bp.is_item_activated(),
#             bp.is_item_deactivated(),
#             bp.is_item_deactivated_after_edit(),
#             bp.is_item_visible(),
#             bp.is_item_clicked(),
#             bp.is_item_toggled_open(),
#             bp.get_item_rect_min().x, bp.get_item_rect_min().y,
#             bp.get_item_rect_max().x, bp.get_item_rect_max().y,
#             bp.get_item_rect_size().x, bp.get_item_rect_size().y
#         )
#
#         bool embed_all_inside_a_child_window = false
#         bp.checkbox("Embed everything inside a child window (for additional testing)", &embed_all_inside_a_child_window)
#         if embed_all_inside_a_child_window:
#             bp.begin_child("outer_child", ImVec2(0, ImGui::GetFontSize() * 20), true)
#
#         #  Testing IsWindowFocused() function with its various flags.
#         #  Note that the ImGuiFocusedFlags_XXX flags can be combined.
#         ImGui::BulletText(
#             "IsWindowFocused() = %d\n"
#             "IsWindowFocused(_ChildWindows) = %d\n"
#             "IsWindowFocused(_ChildWindows|_RootWindow) = %d\n"
#             "IsWindowFocused(_RootWindow) = %d\n"
#             "IsWindowFocused(_AnyWindow) = %d\n",
#             bp.is_window_focused(),
#             bp.is_window_focused(ImGuiFocusedFlags_ChildWindows),
#             bp.is_window_focused(ImGuiFocusedFlags_ChildWindows | ImGuiFocusedFlags_RootWindow),
#             bp.is_window_focused(ImGuiFocusedFlags_RootWindow),
#             bp.is_window_focused(ImGuiFocusedFlags_AnyWindow))
#
#         #  Testing IsWindowHovered() function with its various flags.
#         #  Note that the ImGuiHoveredFlags_XXX flags can be combined.
#         ImGui::BulletText(
#             "IsWindowHovered() = %d\n"
#             "IsWindowHovered(_AllowWhenBlockedByPopup) = %d\n"
#             "IsWindowHovered(_AllowWhenBlockedByActiveItem) = %d\n"
#             "IsWindowHovered(_ChildWindows) = %d\n"
#             "IsWindowHovered(_ChildWindows|_RootWindow) = %d\n"
#             "IsWindowHovered(_ChildWindows|_AllowWhenBlockedByPopup) = %d\n"
#             "IsWindowHovered(_RootWindow) = %d\n"
#             "IsWindowHovered(_AnyWindow) = %d\n",
#             bp.is_window_hovered(),
#             bp.is_window_hovered(ImGuiHoveredFlags_AllowWhenBlockedByPopup),
#             bp.is_window_hovered(ImGuiHoveredFlags_AllowWhenBlockedByActiveItem),
#             bp.is_window_hovered(ImGuiHoveredFlags_ChildWindows),
#             bp.is_window_hovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_RootWindow),
#             bp.is_window_hovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_AllowWhenBlockedByPopup),
#             bp.is_window_hovered(ImGuiHoveredFlags_RootWindow),
#             bp.is_window_hovered(ImGuiHoveredFlags_AnyWindow))
#
#         bp.begin_child("child", ImVec2(0, 50), true)
#         bp.text("This is another child window for testing the _ChildWindows flag.")
#         bp.end_child()
#         if embed_all_inside_a_child_window:
#             bp.end_child()
#
#         char dummy_str[] = "This is a dummy field to be able to tab-out of the widgets above."
#         bp.input_text("dummy", dummy_str, IM_ARRAYSIZE(dummy_str), ImGuiInputTextFlags_ReadOnly)
#
#         #  Calling IsItemHovered() after begin returns the hovered status of the title bar.
#         #  This is useful in particular if you want to create a context menu (with BeginPopupContextItem) associated to the title bar of a window.
#         bool test_window = false
#         bp.checkbox("Hovered/Active tests after Begin() for title bar testing", &test_window)
#         if test_window:
#         {
#             bp.begin("Title bar Hovered/Active tests", &test_window)
#             if bp.begin_popup_context_item()) #  <-- This is using IsItemHovered(:
#             {
#                 if bp.menu_item("Close"): { test_window = false; }
#                 bp.end_popup()
#             }
#             ImGui::Text(
#                 "IsItemHovered() after begin = %d (== is title bar hovered)\n"
#                 "IsItemActive() after begin = %d (== is window being clicked/moved)\n",
#                 bp.is_item_hovered(), bp.is_item_active())
#             bp.end()
#         }
#
#         bp.tree_pop()

# -----------------------------------------------------------------------------
#  [SECTION] About Window / ShowAboutWindow()
#  Access from Dear ImGui Demo -> Tools -> About
# -----------------------------------------------------------------------------
def show_about_window(p_open):
    if not bp.begin("About Dear ImGui", p_open, bp.WindowFlags.AlwaysAutoResize):
        bp.end()
        return

    # bp.text("Dear ImGui %s", bp.get_version())
    # bp.separator()
    bp.text("By Omar Cornut and all Dear ImGui contributors.")
    bp.text("Dear ImGui is licensed under the MIT License, see LICENSE for more information.")

    bp.checkbox("Config/Build Information", show_config_info)
    if show_config_info.value:
        style = bp.get_style()

        copy_to_clipboard = bp.button("Copy to clipboard")
        # bp.begin_child_frame(ImGui::GetID("cfginfos"), ImVec2(0, bp.get_text_line_height_with_spacing() * 18), ImGuiWindowFlags_NoMove)
        # if copy_to_clipboard:
        #     bp.log_to_clipboard()
        #     bp.log_text("```\n"); #  Back quotes will make the text appears without formatting when pasting to GitHub

        bp.text("Dear ImGui")
        bp.separator()
        bp.separator()
        bp.text("style.WindowPadding: %.2f,%.2f" % (style.window_padding.x, style.window_padding.y))
        bp.text("style.WindowBorderSize: %.2f" % style.window_border_size)
        bp.text("style.FramePadding: %.2f,%.2f" % (style.frame_padding.x, style.frame_padding.y))
        bp.text("style.FrameRounding: %.2f" % style.frame_rounding)
        bp.text("style.FrameBorderSize: %.2f" % style.frame_border_size)
        bp.text("style.ItemSpacing: %.2f,%.2f" % (style.item_spacing.x, style.item_spacing.y))
        bp.text("style.ItemInnerSpacing: %.2f,%.2f" % (style.item_inner_spacing.x, style.item_inner_spacing.y))

        # if copy_to_clipboard:
        #     bp.log_text("\n```\n")
        #     bp.log_finish()
        # bp.end_child_frame()
    bp.end()


ctx = bp.Context()

ctx.init(600, 600, "Hello")

while not ctx.should_close():
    with ctx:
        show_demo_window()
