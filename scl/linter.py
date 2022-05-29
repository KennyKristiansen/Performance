from ast import literal_eval
from hashlib import new

import pyperclip
import regex as re

copiedSCL = repr(pyperclip.paste())
testText = """IF #Value_thing > 10 and #boolean  and #boolean  or #boolean OR #Value_thing < 100 THEN #boolean := true; END_IF;
"""
pyperclip.copy(literal_eval(copiedSCL))


class scl_linter:
    def __init__(self, sclCode: str) -> None:
        self.literalString = repr(sclCode)
        newline = re.compile("""(?<newline>\n)|(?<reverse>\r)|(?<space>\s)""")
        split = newline.split(sclCode)

        # remove from list
        res = [i for i in split if i]  # remove None
        res = [i for i in res if i != " "]
        res = [i for i in res if i != "\n"]
        res = [i for i in res if i != "\r"]

        newlineInserts = []
        for i, val in enumerate(res):
            val = val.upper()
            if val == "AND":
                newlineInserts.append(i)
            if val == "THEN":
                newlineInserts.append(i)
            if val == "OR":
                newlineInserts.append(i)
                newlineInserts.append(i + 1)
            if val == "END_REGION":
                newlineInserts.append(i + 1)
            if val == ";":
                newlineInserts.append(i + 1)
        inserts = 0
        print(newlineInserts)
        for i in newlineInserts:
            res.insert(i + inserts, "\n")
            inserts += 1

        print(res)
        self.reformattedString = " ".join(res)

    def paste(self):
        reformattedStr = self.reformattedString
        pyperclip.copy(reformattedStr)
        return


class escapeCharacters:
    def __init__(self) -> None:
        self.newline = "\n"
        self.carriageReturn = "\r"
        self.tab = "\t"


if __name__ == "__main__":
    lint = scl_linter(pyperclip.paste())
    # lint = scl_linter(testText)
    lint.paste()
