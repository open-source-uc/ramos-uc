from datetime import datetime
import json

def handle(context, err):
    print('ERROR:', err)
    with open('logs/error.log', 'a+') as log:
        log.write(str(datetime.now()) + ' Error: ' + str(err) + '\n')
        log.write('Context: ' + json.dumps(context, indent=4) + '\n')
