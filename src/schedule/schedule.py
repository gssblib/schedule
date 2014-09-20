import datetime
import os
import pickle
import sys
import optparse
import urllib

import gdata.calendar.service
import atom

SESSION_FILENAME = 'session.data'

class Schedule(object):

    CALENDAR_ID = '8rljkisdsimoemo5r22vv7fou4%40group.calendar.google.com'

    SCOPE = ['http://www.google.com/calendar/feeds/',
             'https://www.google.com/calendar/feeds/']

    def __init__(self, options):
        self.options = options
        self.setup_service()

    def setup_service(self):
        if os.path.exists(SESSION_FILENAME) and not self.options.new_session:
            with open(SESSION_FILENAME, 'r') as file:
                self.srv = pickle.load(file)
        else:
            next = 'http://www.germansaturdayschoolboston.org/bad.html'
            secure = False
            session = True
            self.srv = gdata.calendar.service.CalendarService()
            url = self.srv.GenerateAuthSubURL(next, self.SCOPE, secure, session)
            print 'Please visit this URL to create a token:'
            print url
            token = urllib.unquote(raw_input('Token: '))
            self.srv.SetAuthSubToken(token)
            self.srv.UpgradeToSessionToken()
            with open(SESSION_FILENAME, 'w') as file:
                pickle.dump(self.srv, file)

    def add_event(self, title, content, start_time, end_time, guests):
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=content)
        event.when.append(
            gdata.calendar.When(
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat()))
        event.when[0].reminder.append(
            gdata.calendar.Reminder(days='1', method='email'))
        for guest in guests:
            event.who.append(gdata.calendar.Who(email=guest))

        new_event = self.srv.InsertEvent(
            event, '/calendar/feeds/%s/private/full' % self.CALENDAR_ID)

    def create(self):
        feed = self.srv.GetCalendarListFeed()
        #for i, a_calendar in enumerate(feed.entry):
        #    print '\t%s. %s' % (i, a_calendar.title.text,)
        self.add_event(
            'Test',
            datetime.datetime(2014, 9, 20, 14, 30),
            datetime.datetime(2014, 9, 20, 15, 0),
            ['stephan.richter@gmail.com']
            )

###############################################################################
# Command-line UI

parser = optparse.OptionParser("%prog <google-doc>")

config = optparse.OptionGroup(
    parser, "Configuration", "Options to configure the scheduler.")

config.add_option(
    '-n', '--new-session',
    action="store_true", dest='new_session', default=False,
    help="""When specified forces the script to create a new session.""")

parser.add_option_group(config)

def post_schedule(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    options, args = parser.parse_args(argv)
    Schedule(options).create()

# Command-line UI
###############################################################################
