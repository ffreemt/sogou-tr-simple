"""Sogou translate."""
#

from time import sleep
from random import random, randint
from httpx import Client
import hashlib
from uuid import uuid4
from langid import classify
from fuzzywuzzy import fuzz, process
import logzero
from logzero import logger


SOGOUTR_CODES = [
    "auto",
    "ar",
    "et",
    "bg",
    "pl",
    "ko",
    "bs-Latn",
    "fa",
    "mww",
    "da",
    "de",
    "ru",
    "fr",
    "fi",
    "tlh-Qaak",
    "tlh",
    "hr",
    "otq",
    "ca",
    "cs",
    "ro",
    "lv",
    "ht",
    "lt",
    "nl",
    "ms",
    "mt",
    "pt",
    "ja",
    "sl",
    "th",
    "tr",
    "sr-Latn",
    "sr-Cyrl",
    "sk",
    "sw",
    "af",
    "no",
    "en",
    "es",
    "uk",
    "ur",
    "el",
    "hu",
    "cy",
    "yua",
    "he",
    "zh-CHS",
    "it",
    "hi",
    "id",
    "zh-CHT",
    "vi",
    "sv",
    "yue",
    "fj",
    "fil",
    "sm",
    "to",
    "ty",
    "mg",
    "bn",
]  # pylint: disable=C0301  # NOQA

# https://github.com/imWildCat/sogou-translate/blob/master/sogou_translate.py
ERROR_DICT = {
    "1001": "Translate API: Unsupported language type",
    "1002": "Translate API: Text too long",
    "1003": "Translate API: Invalid PID",
    "1004": "Translate API: Trial PID limit reached",
    "1005": "Translate API: PID traffic too high",
    "1006": "Translate API: Insufficient balance",
    "1007": "Translate API: Random number does not exist",
    "1008": "Translate API: Signature does not exist",
    "1009": "Translate API: The signature is incorrect",
    "10010": "Translate API: Text does not exist",
    "1050": "Translate API: Internal server error",
}

HEADERS = {'Origin': 'https://fanyi.sogou.com',
 'Referer': 'https://fanyi.sogou.com',
 'X-Requested-With': 'XMLHttpRequest',
 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
URL0 = "https://fanyi.sogou.com"
URL = "https://fanyi.sogou.com/reventondc/translateV2"
URL = "https://fanyi.sogou.com/api/transpc/text/result"

SESS = Client()
# SESS.get("https://fanyi.sogou.com/#auto/zh-CHS/test%201111")
SESS.get(URL0, headers=HEADERS)

SECCODE = "8511813095152"  # V 20190929 obsolete
SECCODE = '109984457'


def sogou_tr(text: str, from_lang: str = "auto", to_lang: str = "zh", wait: float = 0.67, verbose=False) -> str:
    """Translate via sogou.

    >>> from random import randint
    >>> from_lang = "auto"; to_lang = "zh"
    >>> text='my people my country'; from_lang='auto'; to_lang='zh'
    >>> trtext = sogou_tr('test ' + str(randint(1, 1000)))
    >>> trtext[:2] in '测试试验'
    True
    """
    #
    if wait < 0.67:
        wait = 0.67
    wait = wait - 0.5  # for mean of random

    if verbose:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    try:
        sogou_tr.runs += 1
        sogou_tr.runs %= 600  # to prevent unlikely overflow
    except Exception:
        sogou_tr.runs = 0
    if sogou_tr.runs > 500:
        sleep(wait + random())  # ava .67s, 3 calls in 2 secs

    try:
        text = text.__str__().strip()
    except Exception as exc:
        logger.error(exc)
        raise

    if not text:
        sogou_tr.text = "nothing to do"
        return ""

    from_lang = from_lang.lower()
    to_lang = to_lang.lower()

    if from_lang == "auto" and to_lang == "auto":
        to_lang = "zh"

    if from_lang in ["zh", "chinese"]:
        from_lang = "zh-CHS"
    if to_lang in ["zh", "chinese"]:
        to_lang = "zh-CHS"

    if from_lang not in SOGOUTR_CODES:
        try:
            _ = process.extractOne(from_lang, SOGOUTR_CODES, scorer=fuzz.UWRatio)
            from_lang = from_lang[0]
        except Exception as exc:
            logger.warning("%s, from_lang setting to auto", exc)
            from_lang = "auto"
    if to_lang not in SOGOUTR_CODES:
        try:
            _ = process.extractOne(
                to_lang, SOGOUTR_CODES, scorer=fuzz.UWRatio
            )
            to_lang = _[0]
        except Exception as exc:
            logger.warning("%, to_lang setting to zh-CHS", exc)
            to_lang = "zh-CHS"

    if from_lang == to_lang:
        sogou_tr.text = "nothing to do"
        return text

    _ = from_lang + to_lang + text + SECCODE
    md5 = hashlib.md5(_.encode("utf-8"))
    sign = md5.hexdigest()
    uuid = uuid4()

    data = {
        "client": "pc",
        # "dict": "true",
        "fr": "browser_pc",
        "from": from_lang,
        "needQc": "1",
        # "pid": "sogou-dict-vr",
        "s": sign,
        # "second_query": "true",
        "text": text,
        "to": to_lang,
        'uuid': str(uuid),
        # "word_group": "true",
    }

    try:
        # resp = SESS.post(URL, headers=self.api_headers, data=self.form_data)
        resp = SESS.post(URL, headers=HEADERS, data=data)
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        logger.debug(resp.json())
    except Exception as exc:
        logger.error(exc)

    try:
        jdata = resp.json()
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        res = jdata.get("data").get("translate").get("dit")
    except Exception as exc:
        logger.error(exc)
        res = str(exc)

    return res


if __name__ == "__main__":
    text = "An employee at Spataro's No Frills, located at 8990 Chinguacousy Rd, has tested positive for the virus."

    print()
    print(text, "\n")

    print("to zh:", sogou_tr(text), "\n")
    print("to de:", sogou_tr(text, to_lang="de"), "\n")
