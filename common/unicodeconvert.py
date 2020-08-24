import os, sys
import re
import htmlentitydefs
import cgi

class unicodeconvert(object):
    def __init__(self):
        return

    def convert(self, s):
        """Take an input string s, find all things that look like SGML character
        entities, and replace them with the Unicode equivalent.
        Function is from:
        http://stackoverflow.com/questions/1197981/convert-html-entities-to-ascii-in-python/1582036#1582036
        """
        matches = re.findall("&#\d+;", s)
        if len(matches) > 0:
            hits = set(matches)
            for hit in hits:
                name = hit[2:-1]
                try:
                    entnum = int(name)
                    s = s.replace(hit, unichr(entnum))
                except ValueError:
                    pass
        matches = re.findall("&\w+;", s)
        hits = set(matches)
        amp = "&"
        if amp in hits:
            hits.remove(amp)
        for hit in hits:
            name = hit[1:-1]
            if name in htmlentitydefs.name2codepoint:
                s = s.replace(hit, unichr(htmlentitydefs.name2codepoint[name]))
        s = s.replace(amp, "&")
        return s

    def unicodeToHTMLEntities(self, text):
        """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
        text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
        return text

    def convertNonAsciiToHTMLEntities(self, text):
        new_txt = ""
        for x in text:
            if ord(x) < 128:
                new_txt += x
            else:
                try:
                    elm =  self.unicodeToHTMLEntities(x)
                except:
                    elm = '&#'+str(ord(x))+';'
                new_txt += elm
        return new_txt

    def convert_utf8(self, itext):
        content = itext[:]
        try:
            content = content.decode('utf8')
        except:
            pass 
        content = self.convertNonAsciiToHTMLEntities(content)
        content = content.replace('&#160;', ' ')
        content = content.replace('&#194;', ' ')
        content = content.replace('&#187;', ' ')
        content = content.replace('&#8217;', "'")
        content = content.replace('\n', '')
        content = content.replace('\t', ' ') 

        txtstr = self.convert(content)
        txtstr = txtstr.encode('utf8') # unicode to string
        return txtstr

