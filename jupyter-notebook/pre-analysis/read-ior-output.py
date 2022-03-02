import re
import numpy as np
import pandas as pd
import sys
import glob

def main():
    parse_ior_output()

def parse_ior_output():
    machines = ['lassen', 'summit', 'cori']
    fss = ['regular', 'bb']
    scalings = ['strong-scaling', 'weak-scaling']
    num_procs = [64, 128, 256, 512, 1024]
    transfer_sizes = ['4k', '64k', '1m']

    data = {
        'transfer_size': [],
        'scaling': [],
        'num_proc': [],
        'io_subsystem': [],
        'iteration': [],
        'read/write': [],
        'time': [],
    }

    for transfer_size in transfer_sizes:
        for scaling in scalings:
            for machine in machines:
                for fs in fss:
                    for num_proc in num_procs:
                        filenames = glob.glob('/Users/henryxu/Desktop/Research/profiles/' + machine + '/ior-t' + transfer_size + '/app-stdio/ior.' + fs + '.' + scaling + '.' + str(num_proc) + '.*.txt')
                        for filename in filenames:
                            if 'darshan' not in filename and 'recorder' not in filename:
                                with open(filename) as f:
                                    lines = f.readlines()
                                    iteration = 1
                                    count = 0
                                    found = False
                                    for line in lines:
                                        if not found:
                                            start = re.search("total\(s\)", line)
                                        if start:
                                            found = True
                                        if count == 3:
                                            time = line[start.start(): start.end()]
                                            data['transfer_size'].append(transfer_size)
                                            data['scaling'].append(scaling)
                                            data['num_proc'].append(num_proc)
                                            data['io_subsystem'].append(machine + ' ' + fs)
                                            data['time'].append(time)
                                            data['read/write'].append('write')
                                            data['iteration'].append(iteration)
                                        if count == 6:
                                            time = line[start.start(): start.end()]
                                            data['transfer_size'].append(transfer_size)
                                            data['scaling'].append(scaling)
                                            data['num_proc'].append(num_proc)
                                            data['io_subsystem'].append(machine + ' ' + fs)
                                            data['time'].append(time)
                                            data['read/write'].append('read')
                                            data['iteration'].append(iteration)
                                            iteration += 1
                                            found = False
                                            count = 0
                                        if found:
                                            count += 1


    data = pd.DataFrame.from_dict(data)
    data.to_csv('/Users/henryxu/Desktop/Research/profiles/app-stdio-csv/ior.csv', index=False)
    return data

if __name__ == '__main__':
    main()