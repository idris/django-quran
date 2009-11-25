_unicode_to_buckwalter = {
u"\u0621": "'", # Hamza
u"\u0622": "|", # Alif + MaddahAbove (not used in Tanzil)
u"\u0623": ">", # Alif + HamzaAbove
u"\u0624": "&", # Waw + HamzaAbove
u"\u0625": "<", # Alif + HamzaBelow
u"\u0626": "}", # Ya + HamzaAbove
u"\u0627": "A", # Alif
u"\u0628": "b", # Ba
u"\u0629": "p", # TaMarbuta
u"\u062A": "t", # Ta
u"\u062B": "v", # Tha
u"\u062C": "j", # Jeem
u"\u062D": "H", # HHa
u"\u062E": "x", # Kha
u"\u062F": "d", # Dal
u"\u0630": "*", # Thal
u"\u0631": "r", # Ra
u"\u0632": "z", # Zain
u"\u0633": "s", # Seen
u"\u0634": "$", # Sheen
u"\u0635": "S", # Sad
u"\u0636": "D", # DDad
u"\u0637": "T", # TTa
u"\u0638": "Z", # DTha
u"\u0639": "E", # Ain
u"\u063A": "g", # Ghain
u"\u0640": "_", # Tatweel
u"\u0641": "f", # Fa
u"\u0642": "q", # Qaf
u"\u0643": "k", # Kaf
u"\u0644": "l", # Lam
u"\u0645": "m", # Meem
u"\u0646": "n", # Noon
u"\u0647": "h", # Ha
u"\u0648": "w", # Waw
u"\u0649": "Y", # AlifMaksura
u"\u064A": "y", # Ya
u"\u064B": "F", # Fathatan
u"\u064C": "N", # Dammatan
u"\u064D": "K", # Kasratan
u"\u064E": "a", # Fatha
u"\u064F": "u", # Damma
u"\u0650": "i", # Kasra
u"\u0651": "~", # Shadda
u"\u0652": "o", # Sukun
u"\u0653": "^", # Maddah (extended)
u"\u0654": "#", # HamzaAbove (extended)
u"\u0670": "`", # AlifKhanjareeya
u"\u0671": "{", # Alif + HamzaWasl
u"\u067E": "P", # Peh (not Quranic)
u"\u0686": "J", # Tcheh (not Quranic)
u"\u06A4": "V", # Veh (not Quranic)
u"\u06AF": "G", # Gaf (not Quranic)
u"\u06DC": ":", # SmallHighSeen (extended)
u"\u06DF": "@", # SmallHighRoundedZero (extended)
u"\u06E0": "\"", # SmallHighUprightRectangularZero (extended)
u"\u06E2": "[", # SmallHighMeemIsolatedForm (extended)
u"\u06E3": ";", # SmallLowSeen (extended)
u"\u06E5": ",", # SmallWaw (extended)
u"\u06E6": ".", # SmallYa (extended)
u"\u06E8": "!", # SmallHighNoon (extended)
u"\u06EA": "-", # EmptyCentreLowStop (extended)
u"\u06EB": "+", # EmptyCentreHighStop (extended)
u"\u06EC": "%", # RoundedHighStopWithFilledCentre (extended)
u"\u06ED": "]", # SmallLowMeem (extended)
u" ": " ",
}

_buckwalter_to_unicode = {}
for (u, bw) in _unicode_to_buckwalter.iteritems():
    _buckwalter_to_unicode[bw] = u;


# _unicode = u"\u0621\u0622\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062A\u062B\u062C\u062D\u062E\u062F\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063A\u0640\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u0649\u064A\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0654\u0670\u0671\u067E\u0686\u06A4\u06AF\u06DC\u06DF\u06E0\u06E2\u06E2\u06E2\u06E2\u06E2\u06EA\u06EB\u06EC\u06ED"
# _buckwalter = 'NFKC', u"'>|&<}AbptvjHxd*rzs$SDTZEg_fqklmnhwYyFNKaui~o^#`{PJVG:@\"[;,.!-+%]"


def buckwalter_to_unicode(str):
    """
    >>> buckwalter_to_unicode('yaHoyaY`')
    u'\u064a\u064e\u062d\u0652\u064a\u064e\u0649\u0670'
    """
    ret = u""
    for c in str:
        ret += _buckwalter_to_unicode[c]
    return ret

def unicode_to_buckwalter(str):
    """
    >>> unicode_to_buckwalter(u'\u064a\u064e\u062d\u0652\u064a\u064e\u0649\u0670')
    'yaHoyaY`'
    """
    ret = ""
    for c in str:
        ret += _unicode_to_buckwalter[c]
    return ret