import bimpy as bp


ctx = bp.Context()

ctx.init(600, 600, "Hello")

bp.load_fonts(chinese=True, latin_ext=True, japanese=True, cyrillic=True)


while not ctx.should_close():
    with ctx:
        chinese = u"學而不思則罔，思而不學則殆。"
        japanese = u"二兎を追う者は一兎をも得ず。 "

        hiragana = u"あ い う え お か き く け こ さ し す せ そ が ぎ ぐ げ ご ぱ ぴ ぷ ぺ ぽ"
        katakana = u"ア イ ウ エ オ カ キ ク ケ コ サ シ ス セ ソ ガ ギ グ ゲ ゴ パ ピ プ ペ ポ"
        kanji = "川 月 木 心 火 左 北 今 名 美 見 外 成 空 明 静 海 雲 新 語 道 聞 強 飛"

        ukrainian = "Садок вишневий коло хати,\nХрущі над вишнями гудуть,\nПлугатарі з плугами йдуть,\nСпівають ідучи дівчата,\nА матері вечерять ждуть."
        polish = "Hej, tam gdzieś z nad czarnej wody\nWsiada na koń kozak młody.\nCzule żegna się z dziewczyną,\nJeszcze czulej z Ukrainą."
        russian = "Ночь, улица, фонарь, аптека,\nБессмысленный и тусклый свет.\nЖиви ещё хоть четверть века -\nВсё будет так. Исхода нет."

        bp.text('Chinese:')
        bp.indent()
        bp.text(chinese)
        bp.unindent()
        bp.text('Japanese:')
        bp.indent()
        bp.text(japanese)
        bp.bullet_text("hiragana: " + hiragana)
        bp.bullet_text("katakana: " + katakana)
        bp.bullet_text("kanji: " + kanji)
        bp.unindent()
        bp.separator()
        bp.text('Ukrainian:')
        bp.indent()
        bp.text(ukrainian)
        bp.unindent()
        bp.separator()
        bp.text('Polish:')
        bp.indent()
        bp.text(polish)
        bp.unindent()
        bp.separator()
        bp.text('Russian:')
        bp.indent()
        bp.text(russian)
        bp.unindent()
        bp.separator()
