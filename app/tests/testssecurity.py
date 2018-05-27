import unittest
from pprint import pprint

from app import app
from zapv2 import ZAPv2

class TestApplicationSecurity(unittest.TestCase):

    def setUp(self):
        self.target = "http://127.0.0.1:5000"
        self.zapproxy = ZAPv2(proxies={'http': "http://127.0.0.1:5000"})

    def teststaticscan(self):
        self.zapproxy.urlopen(self.target)
        self.zapproxy.spider.scan(self.target)
        self.zapproxy.spider.static()
        self.zapproxy.ascan.scan(self.target)
        self.zapproxy.ascan.status()
        # when status is >= 100, the scan has completed and we can fetch results
        alerts = self.zapproxy.core.alerts()
        pprint(alerts)