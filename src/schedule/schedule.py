import sys
import optparse
import urllib

import gdata.calendar.service

def create_schedule(doc_id):
    next = 'http://www.germansaturdayschoolboston.org/bad.html'
    scope = ['http://www.google.com/calendar/feeds/',
             'https://www.google.com/calendar/feeds/']
    secure = False
    session = True
    srv = gdata.calendar.service.CalendarService()
    url = srv.GenerateAuthSubURL(next, scope, secure, session)
    print url
    token = raw_input('Token: ')
    srv.SetAuthSubToken(urllib.unquote(token))
    srv.UpgradeToSessionToken()
    feed = srv.GetCalendarListFeed()
    for i, a_calendar in enumerate(feed.entry):
        print '\t%s. %s' % (i, a_calendar.title.text,)

###############################################################################
# Command-line UI

parser = optparse.OptionParser("%prog <google-doc>")

config = optparse.OptionGroup(
    parser, "Configuration", "Options to configure the scheduler.")

parser.add_option_group(config)

def post_schedule(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    options, args = parser.parse_args(argv)
    create_schedule(args[0])

# Command-line UI
###############################################################################
