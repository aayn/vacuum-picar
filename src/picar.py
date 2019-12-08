import requests
import http.client
from src.config import HOST, PORT, SIMULATION

BASE_URL = 'http://' + HOST + ':' + PORT + '/'


def __request__(url, times=10):
    for x in range(times):
        try:
            requests.get(url)
            return 0
        except:
            print("Connection error, try again")
    print("Abort")
    return -1


def run_action(cmd):
    """Ask server to do sth, use in running mode

    Post requests to server, server will do what client want to do according to the url.
    This function for running mode

    Args:
        # ============== Back wheels =============
        'bwready' | 'forward' | 'backward' | 'stop'

        # ============== Front wheels =============
        'fwready' | 'fwleft' | 'fwright' |  'fwstraight'

        # ================ Camera =================
        'camready' | 'camleft' | 'camright' | 'camup' | 'camdown'
    """
    # set the url include action information
    global BASE_URL

    url = BASE_URL + 'run/?action=' + cmd
    print('url: %s' % url)
    # post request with url
    __request__(url)


def run_speed(speed):
    """Ask server to set speed, use in running mode

    Post requests to server, server will set speed according to the url.
    This function for running mode.

    Args:
        '0'~'100'
    """
    # Set set-speed url
    url = BASE_URL + 'run/?speed=' + str(speed)
    print('url: %s' % url)
    # Set speed
    __request__(url)


class QueryImage:
    """Query Image

    Query images form http. eg: queryImage = QueryImage(HOST)

    Attributes:
        host, port. Port default 8080, post need to set when creat a new object

    """

    def __init__(self, host, port=8080, argv="/?action=snapshot"):
        # default port 8080, the same as mjpg-streamer server
        self.host = host
        self.port = port
        self.argv = argv

    def queryImage(self):
        """Query Image

        Query images form http.eg:data = queryImage.queryImage()

        Args:
            None

        Return:
            returnmsg.read(), http response data
        """
        http_data = http.client.HTTPConnection(self.host, self.port)
        http_data.putrequest('GET', self.argv)
        http_data.putheader('Host', self.host)
        http_data.putheader('User-agent', 'python-http.client')
        http_data.putheader('Content-type', 'image/jpeg')
        http_data.endheaders()
        returnmsg = http_data.getresponse()

        return returnmsg.read()


def reset():
    run_action('stop')
    run_action('fwstraight')


def stopped(f):
    """Wrapper that stops the PiCar before running f."""

    def wrapper(*args, **kwargs):
        if not SIMULATION:
            run_action('stop')
        # run_action('fwstraight')
        return f(*args, **kwargs)

    return wrapper
