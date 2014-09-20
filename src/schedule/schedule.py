import datetime
import os
import pickle
import sys
import optparse
import urllib

import gdata.calendar.service
import gdata.spreadsheet.service
import atom

CAL_SESSION_FILENAME = 'cal_session.data'
DOCS_SESSION_FILENAME = 'doc_session.data'

class Schedule(object):

    DOC_ID = '1s9mfuxESgiXIxzGHVysGg64hH4bVlpT3JkaTdGWDJwA'
    CALENDAR_ID = '8rljkisdsimoemo5r22vv7fou4%40group.calendar.google.com'

    CAL_SCOPE = ['http://www.google.com/calendar/feeds/',
                 'https://www.google.com/calendar/feeds/']
    DOCS_SCOPE = ['http://spreadsheets.google.com/feeds/',
                  'https://spreadsheets.google.com/feeds/']

    def __init__(self, options):
        self.options = options
        self.setup_cal_service()
        self.setup_docs_service()

    def setup_docs_service(self):
        if os.path.exists(DOCS_SESSION_FILENAME) and \
          not self.options.new_session:
            with open(DOCS_SESSION_FILENAME, 'r') as file:
                self.docs_srv = pickle.load(file)
        else:
            next = 'http://www.germansaturdayschoolboston.org/bad.html'
            secure = False
            session = True
            self.docs_srv = gdata.spreadsheet.service.SpreadsheetsService()
            url = self.docs_srv.GenerateAuthSubURL(
                next, self.DOCS_SCOPE, secure, session)
            print 'Please visit this URL to create a token:'
            print url
            token = urllib.unquote(raw_input('Token: '))
            self.docs_srv.SetAuthSubToken(token)
            self.docs_srv.UpgradeToSessionToken()
            with open(DOCS_SESSION_FILENAME, 'w') as file:
                pickle.dump(self.docs_srv, file)

    def setup_cal_service(self):
        if os.path.exists(CAL_SESSION_FILENAME) and \
          not self.options.new_session:
            with open(CAL_SESSION_FILENAME, 'r') as file:
                self.cal_srv = pickle.load(file)
        else:
            next = 'http://www.germansaturdayschoolboston.org/bad.html'
            secure = False
            session = True
            self.cal_srv = gdata.calendar.service.CalendarService()
            url = self.cal_srv.GenerateAuthSubURL(
                next, self.CAL_SCOPE, secure, session)
            print 'Please visit this URL to create a token:'
            print url
            token = urllib.unquote(raw_input('Token: '))
            self.cal_srv.SetAuthSubToken(token)
            self.cal_srv.UpgradeToSessionToken()
            with open(CAL_SESSION_FILENAME, 'w') as file:
                pickle.dump(self.srv, file)

    def create_name_email_map(self):
        self.name_email_map = {}
        query = gdata.spreadsheet.service.CellQuery()
        query.min_row = '2'

        rows = self.docs_srv.GetListFeed(
            self.DOC_ID, self.sheets['E-mails'], query=query)

        for row in rows.entry:
            data = row.custom
            self.name_email_map[data['name'].text] = data['e-mail'].text

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

        new_event = self.cal_srv.InsertEvent(
            event, '/calendar/feeds/%s/private/full' % self.CALENDAR_ID)

    def create(self):
        wss = self.docs_srv.GetWorksheetsFeed(key=self.DOC_ID)
        self.sheets = {
            ws.title.text: ws.id.text.split('/')[-1]
            for ws in wss.entry}
        self.create_name_email_map()

        query = gdata.spreadsheet.service.CellQuery()
        query.min_row = '3'

        rows = self.docs_srv.GetListFeed(
            self.DOC_ID, self.sheets['Schedule'], query=query)

        for row in rows.entry[1:]:
            data = row.custom
            date = datetime.datetime.strptime(
                data['date'].text, '%B %d, %Y').date()

            for task, start, end in [
                    ('setup', datetime.time(8, 30), datetime.time(9, 0)),
                    ('computer', datetime.time(9, 0), datetime.time(12, 30)),
                    ('shelving', datetime.time(9, 0), datetime.time(12, 30))]:
                start_dt = datetime.datetime.combine(date, start)
                end_dt = datetime.datetime.combine(date, end)
                guests = filter(None,
                    [self.name_email_map.get(name.split(' ')[0].strip())
                     for name in (data[task].text or '').split(', ')]
                    )
                print task.title()
                print start_dt, end_dt
                print guests
                print
                self.add_event(
                   task.title(), data[task].text or '',
                   start_dt, end_dt, guests)

###############################################################################
# Command-line UI

parser = optparse.OptionParser("%prog [options]")

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
