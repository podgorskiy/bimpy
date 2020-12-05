import bimpy

latin = [
    0x0020, 0x00FF,  # Basic Latin + Latin Supplement
]
latin_extension_A = [
    0x0100, 0x0180,  # Extended_A
]
latin_extension_B = [
    0x0180, 0x0250,  # Extended_B
]
greek = [
    0x0370, 0x0400,
    0x1F00, 0x2000   # extended
]
cyrillic = [
    0x0400, 0x052F,  # Cyrillic + Cyrillic Supplement
    0x2DE0, 0x2DFF,  # Cyrillic Extended-A
    0xA640, 0xA69F,  # Cyrillic Extended-B
]
armenian = [
    0x0530, 0x0590
]

general_punctuation = [
    0x2000, 0x206F,  # General Punctuation
]
currency = [
    0x20A0, 0x20CF,
]
letterlike = [
    0x2100, 0x214F,
]
number_forms = [
    0x2150, 0x218F,
]
arrows = [
    0x2190, 0x21FF,
]
math = [
    0x2200, 0x22FF
]

katakana = [
    0x30A0, 0x30FF,  # Katakana
    0x31F0, 0x31FF,  # Katakana Phonetic Extensions
]
hiragana = [
    0x3040, 0x309F,
]
hangul = [
    0xAC00, 0xD79D,  # Hangul Syllables
    0x1100, 0x11FF,  # Hangul Jamo
    0x3130, 0x318F   # Hangul Compatibility Jamo
]
CJK_punctuations = [
    0x3000, 0x303F
]
CJK_unified = [
    0x4e00, 0x9FFF,  # CJK Unified Ideograms
]
Halfwidth_and_Fullwidth = [
    0xFF00, 0xFFEF,
]
CJK_extension_A = [
    0x3400, 0x4DBF  # CJK Han Ideograms
]
CJK_compatibility = [
    0xF900, 0xFAFF   # CJK Compatibility Ideographs
]


def get_simplified_chinese_common():
    r = bimpy.get_glyph_ranges_chinese_simplified_common()
    for i in range(len(r) // 2):
        if 0xFF00 > r[2 * i] >= 0x4E00:
            return r[2 * i:]


def get_japanese_common():
    r = bimpy.get_glyph_ranges_japanese()
    for i in range(len(r) // 2):
        if 0xFF00 > r[2 * i] >= 0x4E00:
            return r[2 * i:]
