#!/usr/bin/env python3
"""
Script to help test and debug. It will create a babelfish message
with the code of the files passed as argument and output them
on stdout so you can pipe them to pyparser or the docker image like
this:

$ ./sendmsg.py [source_file.py]|./pyparser.py

Or with the Docker image:

$ ./sendmsg.py [source_file.py]|docker run -it --rm pyparser:latest
"""
import sys
import json
import msgpack
import logging
sys.path.append('../bin')
import pyparser
# logging.basicConfig(filename="sendmsg.log", level=logging.DEBUG)


def main():
    filesidx = 1
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        outformat = 'json'
        filesidx += 1
        outbuffer = sys.stdout
    else:
        outformat = 'msgpack'
        outbuffer = sys.stdout.buffer

    files = sys.argv[filesidx:]

    d = {
        'action': 'ParseAST',
        'filepath': '',
        'content': '',
        'language': 'python',
    }

    for f in files:
        content = ''
        logging.info(f)
        for encoding in ('utf_8', 'iso8859_15', 'iso8859_15', 'gb2313',
                         'cp1251', 'cp1252', 'cp1250', 'shift-jis', 'gbk', 'cp1256',
                         'iso8859-2', 'euc_jp', 'big5', 'cp874', 'euc_kr', 'iso8859_7'
                                                                           'cp1255'):
            with open(f, encoding=encoding) as infile:
                try:
                    content = infile.read()
                    break
                except UnicodeDecodeError:
                    continue

        d.update({
            'filepath': f,
            'content': content,
        })

        if outformat == 'json':
            # msg = (json.dumps(d, ensure_ascii=True) + '\n@@----@@\n').encode()
            json.dump(d, sys.stdout, ensure_ascii=False)
            outbuffer.write('\n%s' % pyparser.RequestProcessorJSON.JSONEndMark)
            # @@----@@\n')
        else:
            msg = msgpack.packb(d)
            outbuffer.write(msg)
    outbuffer.close()


if __name__ == '__main__':
    main()
