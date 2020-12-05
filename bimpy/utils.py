import bimpy as bp


def help_marker(desc, icon='(?)', width=35.):
    """ Helper to display a little help mark which shows a tooltip when hovered.

    Args:
        desc (string): Help string which is displayed when hovered.
        icon (string, optional): Help marker, optional. If not provided, '(?)' is used. Replace it with your icon from an icon font
        width (Float, optional): Width of the tooltip in text height unit.
    """

    bp.text_disabled(icon)
    if bp.is_item_hovered():
        bp.begin_tooltip()
        bp.push_text_wrap_pos(bp.get_font_size() * width)
        bp.text(desc)
        bp.pop_text_wrap_pos()
        bp.end_tooltip()

