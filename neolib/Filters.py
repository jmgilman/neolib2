import logging
from datetime import datetime

# from neolib import LOG_DIR, PAGE_DIR

LOG_DIR = 'neolib_logs'
LOG_FILE = 'neolib.log'
PAGE_DIR = 'pages'


class HTMLFilter(logging.Filter):
    """Allows for proper filtering of HTML logging
    """

    def filter(self, record):
        """ Called when a log entry is made, ensures page content is logged properly

        Attributes
           record (Record) -- The log record

        Returns
           bool - If the log entry should be logged
        """
        # HTML needs special handling
        if 'pg' in record.args:
            self.handleHTML(record)

        return True

    def handleHTML(self, record):
        """ Saves the given record's page content to a .html file

        Attributes
           record (Record) -- The log record
        """
        # Create a unique file name to identify where this HTML source is coming from
        fileName = datetime.today().strftime("Neolib %Y-%m-%d %H-%M-%S ") + record.module + ".html"

        # Sometimes module may encase the text with < > which is an invalid character for a file name
        fileName = fileName.replace("<", "").replace(">", "")

        # Grab the pg
        pg = record.args['pg']

        # Format a log message that details the page
        ret = "Message: " + record.msg + "\nLine Number: " + str(record.lineno) + "\nURL: " + str(pg.url) + "\nPost Data: " + str(pg.post_data) + "\nAdditional Vars: " + str(pg.header_values)
        ret += "\n\n\n" + str(pg.response.request.headers) + "\n\n" + pg.content

        # Write the file
        f = open(LOG_DIR + '/' + PAGE_DIR + '/' + fileName, "w", encoding='utf-8')
        f.write(ret)
        f.close()
