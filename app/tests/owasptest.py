import time
from pprint import pprint

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

print('Scanning target %s' % target)
# scanid = zap.ascan.scan(target, scanpolicyname="serversecurity")
# scanid = zap.ascan.scan(target, scanpolicyname="injection")
# scanid = zap.ascan.scan(target, scanpolicyname="browsergathering")
scanid = zap.ascan.scan(target, scanpolicyname="misc")
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

risklevels = ["medium","high","critical"]
risks = []
for alert in alerts:
    if alert.get("risk") and alert.get("risk").lower() in risklevels:
        risks.append(alert)

pprint(zap.core.alerts())
