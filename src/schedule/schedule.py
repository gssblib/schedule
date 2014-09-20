import sys
import optparse

import gdata.spreadsheet.service

def create_schedule(doc_id, username, password):
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.debug = True # feel free to toggle this
    client.email = username
    client.password = password
    client.source = 'GSSBLib Scheduler'
    client.ProgrammaticLogin()
    import pdb; pdb.set_trace()

###############################################################################
# Command-line UI

parser = optparse.OptionParser("%prog <google-doc>")

config = optparse.OptionGroup(
    parser, "Configuration", "Options to configure the scheduler.")

config.add_option(
    '--username', '--user', action="store", dest='username',
    help="""Username to access the Google account.""")

config.add_option(
    '--password', '--pwd', action="store", dest='password',
    help="""Password to access the Google account.""")

parser.add_option_group(config)

def post_schedule(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    options, args = parser.parse_args(args)
    create_schedule(args[0], options.username, options.password)

# Command-line UI
###############################################################################
