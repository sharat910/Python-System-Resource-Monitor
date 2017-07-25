from datetime import datetime
import time
import psutil

INTERVAL = 10

def get_net_mbps(pnet, nnet):
    received = 8*float(nnet.bytes_recv - pnet.bytes_recv)/1024./1024./INTERVAL
    sent = 8*float(nnet.bytes_sent - pnet.bytes_sent)/1024./1024./INTERVAL
    return [received, sent]


def get_dist_KBps(pdisk, ndisk):
    read_bytes = float(ndisk.read_bytes - pdisk.read_bytes)/1024./INTERVAL
    write_bytes = float(ndisk.write_bytes - pdisk.write_bytes)/1024./INTERVAL
    return [read_bytes, write_bytes]


def log(pdisk, pnet):
    ndisk = psutil.disk_io_counters()
    nnet = psutil.net_io_counters()
    disk_counters = get_dist_KBps(pdisk, ndisk)
    net_counters = get_net_mbps(pnet, nnet)
    cpu_percent = [psutil.cpu_percent()]
    mem_usage = [psutil.virtual_memory().used/1024./1024.]

    dt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    params = [dt]
    params.extend(cpu_percent)
    params.extend(mem_usage)
    params.extend(net_counters)
    params.extend(disk_counters)

    line = ','.join([str(x) for x in params])
    with open('monitor.csv', 'a') as f:
        f.write(line + '\n')
    print line
    return ndisk, nnet


def main():
    print ','.join(['Timestamp', 'CPU usage (percent)', 'Mem usage (MB)', 'net_rx (mbps)', 'net_tx (mbps)', 'disk_read (KBps)', 'disk_write (KBps)'])
    pdisk = psutil.disk_io_counters()
    pnet = psutil.net_io_counters()
    while True:
        pdisk, pnet = log(pdisk, pnet)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()