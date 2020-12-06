import bimpy as bp
import bimpy.multilingual.unicode_ranges as unicode_ranges
import bimpy.download as download


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

    noto_sans_regular = download.get_font_cached_or_download('https://github.com/googlefonts/noto-fonts/blob/master/hinted/ttf/NotoSans/NotoSans-Regular.ttf?raw=true', 'NotoSans-Regular.ttf')

    bp.add_font_from_file_ttf(noto_sans_regular, size, range=ranges, oversample=2)

    if cjk:
        noto_sans_cjk = download.get_font_cached_or_download('https://github.com/googlefonts/noto-cjk/blob/master/NotoSansCJK-Regular.ttc?raw=true', 'NotoSansCJK-Regular.ttf')
        bp.add_font_from_file_ttf(noto_sans_cjk, size, range=ranges, oversample=1, merge=True)
