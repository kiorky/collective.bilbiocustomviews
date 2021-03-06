#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
import chardet
import datetime


def magicstring(thestr):
    """
    Convert any string to UTF-8 ENCODED one
    """
    seek = False
    if (
        isinstance(thestr, (int, float, long,
                            datetime.date,
                            datetime.time,
                            datetime.datetime))
    ):
        thestr = "{0}".format(thestr)
    if isinstance(thestr, unicode):
        try:
            thestr = thestr.encode('utf-8')
        except Exception:
            seek = True
    if seek:
        try:
            detectedenc = chardet.detect(thestr).get('encoding')
        except Exception:
            detectedenc = None
        if detectedenc:
            sdetectedenc = detectedenc.lower()
        else:
            sdetectedenc = ''
        if sdetectedenc.startswith('iso-8859'):
            detectedenc = 'ISO-8859-15'

        found_encodings = [
            'ISO-8859-15', 'TIS-620', 'EUC-KR',
            'EUC-JP', 'SHIFT_JIS', 'GB2312', 'utf-8', 'ascii',
        ]
        if sdetectedenc not in ('utf-8', 'ascii'):
            try:
                if not isinstance(thestr, unicode):
                    thestr = thestr.decode(detectedenc)
                thestr = thestr.encode(detectedenc)
            except Exception:
                for idx, i in enumerate(found_encodings):
                    try:
                        if not isinstance(thestr, unicode) and detectedenc:
                            thestr = thestr.decode(detectedenc)
                        thestr = thestr.encode(i)
                        break
                    except Exception:
                        if idx == (len(found_encodings) - 1):
                            raise
    if isinstance(thestr, unicode):
        thestr = thestr.encode('utf-8')
    thestr = thestr.decode('utf-8').encode('utf-8')
    return thestr
# vim:set et sts=4 ts=4 tw=80:
