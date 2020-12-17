#!/usr/bin/python3

import os
import sys
import re
import webbrowser

from cgi              import escape
from optparse         import OptionParser
from tempfile         import mkstemp
from rsclib.execute   import Exec
from pybrowse.Version import VERSION

class Browse (Exec) :
    """ Feed a file to running web browser -- modelled after the
        "webbrowse" program in Perl
        You probably want to prevent firefox from changing to the
        current workspace on its own by setting
        browser.tabs.loadDivertedInBackground = true 
        either in the user.js or in about:config
        But this is only a workaround, see
        http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=486570
    """
    def __init__ \
        ( self
        , browser   = None
        , is_html   = False
        , do_markup = True
        , url       = None
        , keep      = 10
        , use_at    = True
        , do_raise  = True
        ) :
        self.browser   = webbrowser.get (browser)
        self.is_html   = is_html
        self.do_markup = do_markup
        self.url       = url
        self.keep      = keep
        self.use_at    = use_at
        self.do_raise  = do_raise
        self.filename  = None
        if url :
            # new = 2 is "open new tab"
            self.wb = self.browser.open \
                (self.url, new = 2, autoraise = self.do_raise)
        else :
            suffix = '.txt'
            if self.is_html or self.do_markup :
                suffix = '.html'
            fd, self.filename = mkstemp (suffix)
            self.filename = os.path.abspath (self.filename)
            f = os.fdopen (fd, 'w')
            if self.do_markup :
                self.markup (sys.stdin.buffer, f)
            else :
                for line in sys.stdin.buffer :
                    f.write (line.decode ('utf-8'))
            f.close ()
            self.wb = self.browser.open \
                (self.filename, new = 2, autoraise = self.do_raise)
            self.schedule_rm ()
    # end def __init__

    def schedule_rm (self) :
        """ Schedule removal of temporary file in self.keep minutes.
            We asume a mkstemp filename doesn't need shell-quoting.
        """
        if self.keep == 0 or not self.filename :
            return
        if self.use_at :
            self.exec_pipe \
                ( ( b'at'
                  , b'now'
                  , b'+'
                  , str (self.keep).encode ('ascii')
                  , b'minutes'
                  )
                , b"/bin/rm -f %s\n" % self.filename.encode ('utf-8')
                )
        else :
            os.system \
                ( "(sleep %s ; /bin/rm -f %s)&"
                % (self.keep * 60, self.filename)
                )
    # end def schedule_rm

    host = r'[-\w.]*\w'
    fqdn = host + r'\.\w{2,}'
    addr = r'[-+\w.%!]*\w@' + host
    path = r'[-+\w.]+(/[-+\w.]+)*/?'
    urlp = r'/[^\s,\'"`<>()\[\]{}]*[^\s,\'"`<>()\[\]{}\.]'
    frm  = r'(^|\n)(From|To|Cc):[^\n]*'
    ngrp = r'(^|\n)(Newsgroups):[^\n]*'
    mesg = r'(^|\n)(Message-ID|References):[^\n]*'
    xref = r'(^|\n)(Xref):[^\n]*'

    RR = [(re.compile (i, flags), j, loop) for i, j, flags, loop in
           ( ( r'(&lt;URL:\s*)([^&\s]+)'
             , r'\1<a href="\2">\2</a>'
             , re.I, 0
             )
           , ( r'(^|[^-\w.">/@])(www\.%(fqdn)s)((%(urlp)s)?)' % locals ()
             , r'\1<a href="http://\2\3">\2\3</a>'
             , re.I, 0
             )
           , ( r'(^|[^-\w.">/@])(ftp\\.%(fqdn)s)((%(urlp)s)?)' % locals ()
             , r'\1<a href="ftp://\2\3">\2\3</a>'
             , re.I, 0
             )
           , ( r'(^|[^-\w.">/@])(%(fqdn)s):(/?)(%(path)s)' % locals ()
             , r'\1<a href="ftp://\2/\4">\2:\3\4</a>'
             , 0, 0
             )
           , ( r'(^|[^-\w.">/])(\w+:%(urlp)s)' % locals ()
             , r'\1<a href="\2">\2</a>'
             , 0, 0
             )
           , ( r'(^|\s)(/%(path)s)(\s|$)' % locals ()
             , r'\1<a href="file:\2">\2</a>\4'
             , 0, 0
             )
           , ( r'($from([ \t]|\&lt;))(%(addr)s)' % locals ()
             , r'\1<a href="mailto:\5">\5</a>'
             , re.I, 1
             )
           , ( r'(%(ngrp)s[ \t,])([-+\w]+(\.[-+\w]+)+)' % locals ()
             , r'\1<a href="news:\4">\4</a>'
             , re.I, 1
             )
           , ( r'(%(mesg)s\&lt;)([^\&\s]+@%(host)s)(\&gt;)' % locals ()
             , r'\1<a href="news:\4">\4</a>\5'
             , re.I, 1
             )
           , ( r'(^|[\\s,])(%(addr)s)' % locals ()
             , r'\1<a href="mailto:\2">\2</a>'
             , 0, 0
             )
           , ( r'(\&lt;)([-+\w.]{0,13}\w@%(host)s)(\&gt;)' % locals ()
             , r'\1<a href="mailto:\2">\2</a>\3'
             , re.I, 0
             )
           , ( r'(\&lt;)([^\&\s@<]+@%(host)s)(\&gt;)' % locals ()
             , r'\1<a href="news:\2">\2</a>\3'
             , re.I, 0
             )
           )
         ]

    def markup (self, input, output, encoding = 'utf-8') :
        output.write ('<html>\n')
        for line in input :
            line = line.decode (encoding)
            line = escape (line)
            for n, (regex, replacement, multiple) in enumerate (self.RR) :
                #print n
                if multiple :
                    k = 0
                    while k :
                        line, k = regex.subn (replacement, line)
                else :
                    line = regex.sub (replacement, line)
            line = line.replace ('\n', '<br>\n')
            output.write (line)
        output.write ('</html>\n')
    # end def markup

# end class Browse

def main () :
    parser = OptionParser (version = "%%prog %s" % VERSION)
    parser.add_option \
        ( "-b", "--browser"
        , dest    = "browser"
        , help    = "What browser to use, use default if unspecified"
        )
    parser.add_option \
        ( "-s", "--html"
        , dest    = "is_html"
        , action  = "store_true"
        , help    = "tag the standard input as HTML (default TEXT)"
        , default = False
        )
    parser.add_option \
        ( "-m", "--markup"
        , dest    = "do_markup"
        , action  = "store_true"
        , help    = "markup a TEXT copy of the input for browsing (heuristic)"
        , default = False
        )
    parser.add_option \
        ( "-u", "--url"
        , dest    = "url"
        , help    = "take the argument as a URL to browse"
        )
    parser.add_option \
        ( "-k", "--keep"
        , dest    = "keep"
        , help    = "minutes to keep any temporary input"
        , type    = "int"
        , default = 10
        )
    parser.add_option \
        ( "-p", "--sleep"
        , dest    = "use_at"
        , help    = "use a sleeping process to delete temporary input"
        , action  = "store_false"
        , default = True
        )
    parser.add_option \
        ( "-a", "--at-job"
        , dest    = "use_at"
        , help    = "use an at job to delete temporary input"
        , action  = "store_true"
        , default = True
        )
    parser.add_option \
        ( "-r", "--noraise"
        , dest    = "do_raise"
        , action  = "store_false"
        , help    = "don't raise the browser window"
        , default = True
        )
    (opt, args) = parser.parse_args ()
    if len (args) :
        parser.error ("No arguments please")
    b = Browse (** opt.__dict__)
# end def main

if __name__ == '__main__' :
    main ()
