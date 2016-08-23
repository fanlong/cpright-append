#!/usr/bin/env python
import os
from sys import argv
import getopt

def append_header(fname, crlines, comment_token, skip_first_line_comment):
    f = open(fname, "r");
    first_line = f.readline();
    content = f.read();
    f.close();
    f = open(fname, "w");
    skip_first_line = False;
    if skip_first_line_comment and (first_line.find("//") == 0 or first_line.find("#") == 0 or first_line.find("/*") == 0):
        skip_first_line = True;
        f.write(first_line);
        f.flush();
    for crline in crlines:
        print >> f, comment_token + crline.strip("\n");
    f.flush();
    if not skip_first_line:
        f.write(first_line);
    f.write(content);
    f.close();

(opts, args) = getopt.getopt(argv[1:], "");
if (len(args) < 2):
    print "cpright-append.py <header.txt> <directory>"

fheader = args[0];
tdir = args[1];

f = open(fheader, "r");
crlines = f.readlines();
f.close();

for root, dirs, files in os.walk(tdir):
    for fname in files:
        ridx = fname.rfind(".");
        if ridx == -1:
            continue;
        ext = fname[ridx:].lower();
        if ext != ".c" and ext != ".cpp" and ext != ".h" and ext != ".py" and ext != ".java":
            continue;
        print "Append copyright header to " + root + "/" + fname;
        comment_token = "// ";
        skip_first_line_comment = False;
        if ext == ".py":
            comment_token = "# ";
            skip_first_line_comment = True;
        append_header(root + "/" + fname, crlines, comment_token, skip_first_line_comment);
