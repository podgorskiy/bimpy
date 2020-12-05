import sys
import os

if os.path.exists("../cmake-build-debug/"):
    print('Running Debugging session!')
    sys.path.insert(0, "../cmake-build-debug/")


import bimpy as bp
from bimpy.utils import help_marker


check = bp.Bool(True)
e = bp.Int(0)
clicked = 0
counter = 0
item_current = bp.Int(0)
str0 = bp.String("Hello, world!")
buf = bp.String("\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e")


def show_demo_window():
    bp.begin_root(menu=True)

    #  Menu Bar
    if bp.begin_menu_bar():
        if bp.begin_menu("Menu"):
            bp.end_menu()

        if bp.begin_menu("Examples"):
            bp.end_menu()

        if bp.begin_menu("Tools"):
            bp.end_menu()

        bp.end_menu_bar()

    global clicked
    if bp.button("Button"):
        clicked += 1
    if clicked & 1:
        bp.same_line()
        bp.text("Thanks for clicking me!")

    bp.checkbox("checkbox", check)

    bp.radio_button("radio a", e, 0);
    bp.same_line()
    bp.radio_button("radio b", e, 1);
    bp.same_line()
    bp.radio_button("radio c", e, 2)

    #  Color buttons, demonstrate using PushID() to add unique identifier in the ID stack, and changing style.
    for i in range(7):
        if i > 0:
            bp.same_line()
        bp.push_id_int(i)
        bp.push_style_color(bp.Colors.Button, bp.Vec4(i / 7.0, 0.6, 0.6, 1.0))
        bp.push_style_color(bp.Colors.ButtonHovered, bp.Vec4(i / 7.0, 0.7, 0.7, 1.0))
        bp.push_style_color(bp.Colors.ButtonActive, bp.Vec4(i / 7.0, 0.8, 0.8, 1.0))
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
        counter -= 1

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
    items = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK", "LLLLLLL", "MMMM",
             "OOOOOOO"]
    bp.combo("combo", item_current, items)
    bp.same_line();
    help_marker(
        "Refer to the \"Combo\" section below for an explanation of the full BeginCombo/EndCombo API, and demonstration of various flags.\n")

    #  To wire InputText() with std::string or any other custom string type,
    #  see the "Text Input > Resize Callback" section of this demo, and the misc/cpp/imgui_stdlib.h file.
    bp.input_text("input text", str0, 128)
    bp.same_line();
    help_marker(
        "USER:\nHold SHIFT or use mouse to select text.\n" "CTRL+Left/Right to word jump.\n" "CTRL+A or double-click to select all.\n" "CTRL+X,CTRL+C,CTRL+V clipboard.\n" "CTRL+Z,CTRL+Y undo/redo.\n" "ESCAPE to revert.\n\nPROGRAMMER:\nYou can use the ImGuiInputTextFlags_CallbackResize facility if you need to wire InputText() to a dynamic string type. See misc/cpp/imgui_stdlib.h for an example (this is not demonstrated in imgui_demo.cpp).")

    bp.end()


ctx = bp.Context()

ctx.init(600, 600, "Demo")

while not ctx.should_close():
    with ctx:
        show_demo_window()
