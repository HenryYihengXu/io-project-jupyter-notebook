import re
import numpy as np
import pandas as pd
import sys
import glob

def main():
    parse_haccio_output()

def parse_haccio_output():
    machines = ['lassen', 'summit', 'cori']
    fss = ['regular', 'bb']
    scalings = ['strong-scaling', 'weak-scaling']
    num_procs = [64, 128, 256, 512, 1024]
    num_bb_servers = [1, 2, 4, 8]

    data = {
        'scaling': [],
        'num_proc': [],
        'io_subsystem': [],
        'iteration': [],
        'read/write': [],
        'time': []
    }
    is_write = True
    for scaling in scalings:
        for machine in machines:
            for fs in fss:
                if machine == 'cori' and fs == 'bb':
                    for num_bb_server in num_bb_servers:
                        for num_proc in num_procs:
                            if num_bb_server != 1:
                                filenames = glob.glob('/Users/henryxu/Desktop/Research/profiles/' + machine + '/haccio/app-stdio/hacc_io.' + fs + '.strip-' + str(num_bb_server) + 'server.' + scaling + '.' + str(num_proc) + '.*.txt')
                            else:
                                filenames = glob.glob('/Users/henryxu/Desktop/Research/profiles/' + machine + '/haccio/app-stdio/hacc_io.' + fs + '.' + scaling + '.' + str(num_proc) + '.*.txt')
                            for filename in filenames:
                                if 'darshan' not in filename and 'recorder' not in filename:
                                    with open(filename) as f:
                                        lines = f.readlines()
                                        iteration = 1
                                        for line in lines:
                                            start = re.search("Bytes", line)
                                            end = re.search("MaxTime", line)
                                            if start and end:
                                                time = line[start.end() + 1: end.start() -1]
                                                data['scaling'].append(scaling)
                                                data['num_proc'].append(num_proc)
                                                data['io_subsystem'].append(machine + ' ' + fs + ' strip ' + str(num_bb_server))
                                                data['time'].append(time)
                                                data['iteration'].append(iteration)
                                                if is_write:
                                                    data['read/write'].append('write')
                                                else:
                                                    data['read/write'].append('read')
                                                    iteration += 1
                                                is_write = not is_write
                else:
                    for num_proc in num_procs:
                        filenames = glob.glob('/Users/henryxu/Desktop/Research/profiles/' + machine + '/haccio/app-stdio/hacc_io.' + fs + '.' + scaling + '.' + str(num_proc) + '.*.txt')
                        for filename in filenames:
                            if 'darshan' not in filename and 'recorder' not in filename:
                                with open(filename) as f:
                                    lines = f.readlines()
                                    iteration = 1
                                    for line in lines:
                                        start = re.search("Bytes", line)
                                        end = re.search("MaxTime", line)
                                        if start and end:
                                            time = line[start.end() + 1: end.start() -1]
                                            data['scaling'].append(scaling)
                                            data['num_proc'].append(num_proc)
                                            data['io_subsystem'].append(machine + ' ' + fs)
                                            data['time'].append(time)
                                            data['iteration'].append(iteration)
                                            if is_write:
                                                data['read/write'].append('write')
                                            else:
                                                data['read/write'].append('read')
                                                iteration += 1
                                            is_write = not is_write
    data = pd.DataFrame.from_dict(data)
    data.to_csv('/Users/henryxu/Desktop/Research/profiles/app-stdio-csv/haccio.csv', index=False)
    return data

if __name__ == '__main__':
    main()