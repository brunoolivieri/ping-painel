# relies on https://github.com/alessandromaggio/pythonping

from pythonping import ping
import pandas as pd
import os

targets = {
    'gateway':      '192.168.0.1',
    'webmailpuc':   '139.82.16.3',
    'uol':          '200.147.3.157',
    'dns':          '8.8.8.8'
}

results = pd.DataFrame(columns =  ["hostname", "delay", "packetloss"])


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ping_host(hostname, ip, limit):
    ping_result = ping(target=ip, count=1, timeout=limit)
    return [hostname, ping_result.rtt_min_ms, ping_result.packet_loss]

def print_avgs(dataframein):
    results_null = dataframein[dataframein['packetloss'] > 0.0]
    results_packetloss = results_null.groupby(['hostname'])['hostname'].count()
    print(results_packetloss)

    results_ok = dataframein[dataframein['packetloss'] == 0.0]
    results_avg = results_ok.groupby(['hostname'])['delay'].mean()
    print(results_avg)



def print_status(dataframein):
    last_results = dataframein.tail(len(targets))
    last_results_idx = last_results.reset_index()
    #os.system('clear')

    for index, row in last_results_idx.iterrows():
        if (row['packetloss'] == 0):
            print('\x1b[6;30;42m' + "  ONLINE:   %s" % row['hostname'] )#+ "          " + '\x1b[0m'  )        
            #print(row['hostname'], row['delay'])
        else:
            print('\x1b[1;31;47m' + "  OFFLINE:  %s" % row['hostname'] )#+ "          " +  '\x1b[0m'  )        
    print('\x1b[0m')


if __name__ == '__main__':

    timeout = 0
    n = 0

    while True:
        n += 1
        timeout += 0.09

        for hostname, ip in targets.items():
            results = pd.concat([pd.DataFrame([ping_host(hostname,ip,timeout)], columns=results.columns), results],  ignore_index=True)

        #     os.system('clear')
        print_status(results)
    
        # if not (n % 10):
        #     os.system('clear')
        #     print_avgs(results)

        if (timeout >= 3):
            break





