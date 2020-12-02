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


# Helper to display a little (?) mark which shows a tooltip when hovered.
# In your own code you may want to display an actual icon if you are using a merged icon fonts (see docs/FONTS.txt)
def help_marker(desc):
    bp.text_disabled("(?)")
    if bp.is_item_hovered():
        bp.begin_tooltip()
        bp.push_text_wrap_pos(bp.get_font_size() * 35.0)
        bp.text(desc)
        bp.pop_text_wrap_pos()
        bp.end_tooltip()


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

    # if bp.collapsing_header("Configuration"):
    # {
    #     ImGuiIO& io = bp.get_i_o()
    #
    #     if bp.tree_node("Configuration##2"):
    #     {
    #         bp.checkbox_flags("io.ConfigFlags: NavEnableKeyboard", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NavEnableKeyboard)
    #         bp.checkbox_flags("io.ConfigFlags: NavEnableGamepad", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NavEnableGamepad)
    #         bp.same_line(); HelpMarker("Required back-end to feed in gamepad inputs in io.NavInputs[] and set io.BackendFlags |= ImGuiBackendFlags_HasGamepad.\n\nRead instructions in imgui.cpp for details.")
    #         bp.checkbox_flags("io.ConfigFlags: NavEnableSetMousePos", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NavEnableSetMousePos)
    #         bp.same_line(); HelpMarker("Instruct navigation to move the mouse cursor. See comment for ImGuiConfigFlags_NavEnableSetMousePos.")
    #         bp.checkbox_flags("io.ConfigFlags: NoMouse", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NoMouse)
    #         if io.ConfigFlags & ImGuiConfigFlags_NoMouse: #  Create a way to restore this flag otherwise we could be stuck completely!
    #         {
    #             if fmodf((float)bp.get_time(), 0.40f) < 0.20f:
    #             {
    #                 bp.same_line()
    #                 bp.text("<<PRESS SPACE TO DISABLE>>")
    #             }
    #             if bp.is_key_pressed(ImGui::GetKeyIndex(ImGuiKey_Space)):
    #                 io.ConfigFlags &= ~ImGuiConfigFlags_NoMouse
    #         }
    #         bp.checkbox_flags("io.ConfigFlags: NoMouseCursorChange", (unsigned int *)&io.ConfigFlags, ImGuiConfigFlags_NoMouseCursorChange)
    #         bp.same_line(); HelpMarker("Instruct back-end to not alter mouse cursor shape and visibility.")
    #         bp.checkbox("io.ConfigInputTextCursorBlink", &io.ConfigInputTextCursorBlink)
    #         bp.same_line(); HelpMarker("Set to false to disable blinking cursor, for users who consider it distracting")
    #         bp.checkbox("io.ConfigWindowsResizeFromEdges", &io.ConfigWindowsResizeFromEdges)
    #         bp.same_line(); HelpMarker("Enable resizing of windows from their edges and from the lower-left corner.\nThis requires (io.BackendFlags & ImGuiBackendFlags_HasMouseCursors) because it needs mouse cursor feedback.")
    #         bp.checkbox("io.ConfigWindowsMoveFromTitleBarOnly", &io.ConfigWindowsMoveFromTitleBarOnly)
    #         bp.checkbox("io.MouseDrawCursor", &io.MouseDrawCursor)
    #         bp.same_line(); HelpMarker("Instruct Dear ImGui to render a mouse cursor for you. Note that a mouse cursor rendered via your application GPU rendering path will feel more laggy than hardware cursor, but will be more in sync with your other visuals.\n\nSome desktop applications may use both kinds of cursors (e.g. enable software cursor only when resizing/dragging something).")
    #         bp.tree_pop()
    #         bp.separator()
    #     }
    #
    #     if bp.tree_node("Backend Flags"):
    #     {
    #         HelpMarker("Those flags are set by the back-ends (imgui_impl_xxx files) to specify their capabilities.\nHere we expose then as read-only fields to avoid breaking interactions with your back-end.")
    #         ImGuiBackendFlags backend_flags = io.BackendFlags; #  Make a local copy to avoid modifying actual back-end flags.
    #         bp.checkbox_flags("io.BackendFlags: HasGamepad", (unsigned int *)&backend_flags, ImGuiBackendFlags_HasGamepad)
    #         bp.checkbox_flags("io.BackendFlags: HasMouseCursors", (unsigned int *)&backend_flags, ImGuiBackendFlags_HasMouseCursors)
    #         bp.checkbox_flags("io.BackendFlags: HasSetMousePos", (unsigned int *)&backend_flags, ImGuiBackendFlags_HasSetMousePos)
    #         bp.checkbox_flags("io.BackendFlags: RendererHasVtxOffset", (unsigned int *)&backend_flags, ImGuiBackendFlags_RendererHasVtxOffset)
    #         bp.tree_pop()
    #         bp.separator()
    #     }
    #
    #     if bp.tree_node("Style"):
    #     {
    #         HelpMarker("The same contents can be accessed in 'Tools->Style Editor' or by calling the ShowStyleEditor() function.")
    #         bp.show_style_editor()
    #         bp.tree_pop()
    #         bp.separator()
    #     }
    #
    #     if bp.tree_node("Capture/Logging"):
    #     {
    #         bp.text_wrapped("The logging API redirects all text output so you can easily capture the content of a window or a block. Tree nodes can be automatically expanded.")
    #         HelpMarker("Try opening any of the contents below in this window and then click one of the \"Log To\" button.")
    #         bp.log_buttons()
    #         bp.text_wrapped("You can also call ImGui::LogText() to output directly to the log without a visual output.")
    #         if bp.button("Copy \"Hello, world!\" to clipboard"):
    #         {
    #             bp.log_to_clipboard()
    #             bp.log_text("Hello, world!")
    #             bp.log_finish()
    #         }
    #         bp.tree_pop()
    #     }
    # }
    #
    # if bp.collapsing_header("Window options"):
    # {
    #     bp.checkbox("No titlebar", &no_titlebar); bp.same_line(150)
    #     bp.checkbox("No scrollbar", &no_scrollbar); bp.same_line(300)
    #     bp.checkbox("No menu", &no_menu)
    #     bp.checkbox("No move", &no_move); bp.same_line(150)
    #     bp.checkbox("No resize", &no_resize); bp.same_line(300)
    #     bp.checkbox("No collapse", &no_collapse)
    #     bp.checkbox("No close", &no_close); bp.same_line(150)
    #     bp.checkbox("No nav", &no_nav); bp.same_line(300)
    #     bp.checkbox("No background", &no_background)
    #     bp.checkbox("No bring to front", &no_bring_to_front)
    # }
    #
    # #  All demo contents
    # ShowDemoWindowWidgets()
    # ShowDemoWindowLayout()
    # ShowDemoWindowPopups()
    # ShowDemoWindowColumns()
    # ShowDemoWindowMisc()

    #  End of ShowDemoWindow()
    bp.end()


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
