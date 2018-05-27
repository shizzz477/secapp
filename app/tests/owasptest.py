"""
    OWASP Top 10 testing module
      This testng module leverages OWASP Zap by running a large
      series of tests through a local proxy configured in the ZAP
      application.  The result will be an html report with all the
      potential security risks that were found, the description, and
      recommendations for remediation

     Also, the OWASP Zap applcation will show the details of each test

    Requirements:
          - OWASP ZAP needs to be running with 'Local Proxy' configured to
          match the 'proxies' parameter for the ZAPv2 object
          - The target application needs to be running and the 'target' variable
          set to reflect where it's running
"""

import time
from zapv2 import ZAPv2

target = 'http://127.0.0.1:5000/'
apikey = None
zap = ZAPv2(apikey=apikey,proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

print('Accessing target {}'.format(target))
zap.urlopen(target)
time.sleep(2)

print('Spidering target %s' % target)
scanid = zap.spider.scan(target)
time.sleep(2)
while int(zap.spider.status(scanid)) < 100:
    print('Spider progress %: ' + zap.spider.status(scanid))
    time.sleep(2)

print('Spider completed')
# Give the passive scanner a chance to finish
time.sleep(10)

# Run the active scan
print('Scanning target %s' % target)
scanid = zap.ascan.scan(target)
while int(zap.ascan.status(scanid)) < 100:
    print('Scan progress %: ' + zap.ascan.status(scanid))
    time.sleep(10)
print('Scan completed')

# Report the results
print('Hosts: ' + ', '.join(zap.core.hosts))
print('Alerts: ')
alerts = zap.core.alerts()
alertsum = zap.core.alerts_summary()

reportfile = open("alertreport.html", "w")
reportfile.write(zap.core.htmlreport())
reportfile.close()
