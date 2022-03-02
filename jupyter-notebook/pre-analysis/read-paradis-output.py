import re
import numpy as np
import pandas as pd
import sys
import glob

def main():
    parse_paradis_output()

def parse_paradis_output():
    machines = ['lassen', 'summit', 'cori']
    fss = ['regular', 'bb']
    scalings = ['weak-scaling']
    num_procs = [64, 128, 256, 512, 1024]

    data = {
        'scaling': [],
        'num_proc': [],
        'io_subsystem': [],
        'iteration': [],
        'time': []
    }

    for scaling in scalings:
        for machine in machines:
            for fs in fss:
                for num_proc in num_procs:
                    filenames = glob.glob('/Users/henryxu/Desktop/Research/profiles/' + machine + '/paradis/app-stdio/paradis.' + fs + '.' + scaling + '.' + str(num_proc) + '.*.txt')
                    for filename in filenames:
                        if 'darshan' not in filename and 'recorder' not in filename:
                            with open(filename) as f:
                                iteration = 1
                                lines = f.readlines()
                                for line in lines:
                                    start = re.search("main computation loop is", line)
                                    if start:
                                        time = line[start.end() + 1: -2]
                                        data['scaling'].append(scaling)
                                        data['num_proc'].append(num_proc)
                                        data['io_subsystem'].append(machine + ' ' + fs)
                                        data['time'].append(time)
                                        data['iteration'].append(iteration)
                                        iteration += 1

    data = pd.DataFrame.from_dict(data)
    data.to_csv('/Users/henryxu/Desktop/Research/profiles/app-stdio-csv/paradis.csv', index=False)
    return data

if __name__ == '__main__':
    main()