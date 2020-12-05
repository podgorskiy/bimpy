import sys
import os

if os.path.exists("../cmake-build-debug/"):
    print('Running Debugging session!')
    sys.path.insert(0, "../cmake-build-debug/")

import bimpy as bp
import wget
from tempfile import NamedTemporaryFile


ctx = bp.Context()

ctx.init(600, 600, "Hello")

import bimpy.multilingual.unicode_ranges as unicode_ranges


def load_fonts(size=22,
               latin=True, latin_ext=False, greek=False, cyrillic=False, armenian=False, special=False,
               chinese=False, japanese=False, korean=False,
               simplified_chinese_common=False, japanese_common=False,
               cjk_unified=False, katakana=False, hiragana=False, cjk_ext_a=False, cjk_compatibility=False):
    ranges = []

    cjk = False

    if latin:
        ranges += unicode_ranges.latin
    if latin_ext:
        ranges += unicode_ranges.latin_extension_A + unicode_ranges.latin_extension_B
    if greek:
        ranges += unicode_ranges.greek
    if cyrillic:
        ranges += unicode_ranges.cyrillic
    if armenian:
        ranges += unicode_ranges.armenian
    if special:
        ranges += unicode_ranges.math + unicode_ranges.arrows + unicode_ranges.currency
        ranges += unicode_ranges.general_punctuation + unicode_ranges.letterlike + unicode_ranges.number_forms
    if chinese or japanese or korean or cjk_unified or simplified_chinese_common or japanese_common or katakana or hiragana:
        ranges += unicode_ranges.CJK_punctuations
        cjk = True
    if chinese or japanese or cjk_unified:
        if simplified_chinese_common or japanese_common:
            raise ValueError("Simplified Chinese common or Japanese common sets should not be mixed with the full sets")
        ranges += unicode_ranges.CJK_unified
    if simplified_chinese_common:
        ranges += unicode_ranges.get_simplified_chinese_common()
    if japanese_common:
        ranges += unicode_ranges.get_japanese_common()
    if japanese or japanese_common:
        katakana = True
        hiragana = True
    if katakana:
        ranges += unicode_ranges.katakana
    if hiragana:
        ranges += unicode_ranges.hiragana
    if korean:
        ranges += unicode_ranges.hangul
    if cjk_ext_a:
        ranges += unicode_ranges.CJK_extension_A
    if cjk_compatibility:
        ranges += unicode_ranges.CJK_compatibility + unicode_ranges.Halfwidth_and_Fullwidth

    ranges = list([i for sub in list(set(zip(ranges[::2], ranges[1::2]))) for i in sub])  # keep unique ranges

    if not os.path.exists('NotoSans-Regular.ttf'):
        wget.download('https://github.com/googlefonts/noto-fonts/blob/master/hinted/ttf/NotoSans/NotoSans-Regular.ttf?raw=true')
    bp.add_font_from_file_ttf("NotoSans-Regular.ttf", size, range=ranges, oversample=2)

    if cjk:
        if not os.path.exists('NotoSansCJK-Regular.ttc'):
            wget.download('https://github.com/googlefonts/noto-cjk/blob/master/NotoSansCJK-Regular.ttc?raw=true')
        bp.add_font_from_file_ttf("NotoSansCJK-Regular.ttc", size, range=ranges, oversample=1, merge=True)


def help_marker(desc):
    bp.text_disabled("(?)")
    if bp.is_item_hovered():
        bp.begin_tooltip()
        bp.push_text_wrap_pos(bp.get_font_size() * 35.0)
        bp.text(desc)
        bp.pop_text_wrap_pos()
        bp.end_tooltip()


load_fonts(chinese=True, latin_ext=True, japanese=True, cyrillic=True)


while not ctx.should_close():
    with ctx:
        chinese = u"學而不思則罔，思而不學則殆。"
        japanese = u"二兎を追う者は一兎をも得ず。 "

        bp.text("PROGRAMMER GUIDE:")
        bp.bullet_text("See the ShowDemoWindow() code in imgui_demo.cpp. <- you are here!")
        bp.bullet_text("See comments in imgui.cpp.")
        bp.bullet_text("See example applications in the examples/ folder.")
        bp.bullet_text("Read the FAQ at http:# www.dearimgui.org/faq/")
        bp.bullet_text("Set 'io.ConfigFlags |= NavEnableKeyboard' for keyboard controls.")
        bp.bullet_text("Set 'io.ConfigFlags |= NavEnableGamepad' for gamepad controls.")
        bp.separator()

        bp.text_wrapped(
            "The logging API redirects all text output so you can easily capture the content of a window or a block. Tree nodes can be automatically expanded.")

        bp.text_colored(bp.Vec4(1.0, 1.0, 0.0, 1.0), "Yellow")
        bp.text_disabled("Disabled")
        bp.same_line();
        help_marker("The TextDisabled color is stored in ImGuiStyle.")
        hiragana = u"あ い う え お か き く け こ さ し す せ そ が ぎ ぐ げ ご ぱ ぴ ぷ ぺ ぽ"
        katakana = u"ア イ ウ エ オ カ キ ク ケ コ サ シ ス セ ソ ガ ギ グ ゲ ゴ パ ピ プ ペ ポ"
        kanji = "川 月 木 心 火 左 北 今 名 美 見 外 成 空 明 静 海 雲 新 語 道 聞 強 飛"
        ukr = "Садок вишневий коло хати,\nХрущі над вишнями гудуть,\nПлугатарі з плугами йдуть,\nСпівають ідучи дівчата,\nА матері вечерять ждуть."
        ukr = "Hej, tam gdzieś z nad czarnej wody\nWsiada na koń kozak młody.\nCzule żegna się z dziewczyną,\nJeszcze czulej z Ukrainą."
        bp.text(chinese)
        bp.text(japanese)
        bp.text(hiragana)
        bp.text(katakana)
        bp.text(kanji)
        bp.text(ukr)

        bp.text_colored(bp.Vec4(1.0, 1.0, 0.0, 1.0), japanese)

        bp.text_disabled("Disabled")
        bp.same_line()
        help_marker("The TextDisabled color is stored in ImGuiStyle.")

        bp.show_demo_window()
