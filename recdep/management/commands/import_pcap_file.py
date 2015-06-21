import sys

from django.core.management.base import BaseCommand, CommandError

from packetparser.pcap import PcapFile

from ...models import (
    Sensor, ServiceSet, Node,
    ProbeReq
)


class Command(BaseCommand):
    help = 'Import a PCAP file into the recdep.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pcap_file_name', nargs='+', type=unicode)

    def handle(self, *args, **options):
        self.stdout.write('Reading PCAP file.')
        self.stdout.write(', '.join(options['pcap_file_name']))

        pcap_file_name_list = options['pcap_file_name']

        for pcap_file_name in pcap_file_name_list:
            if pcap_file_name == '-':
                pcap_file_handle = sys.stdin
                seekable = False
            else:
                pcap_file_handle = open(pcap_file_name, 'rb')
                seekable = True

            pcap_file = PcapFile.parse_header(pcap_file_handle, seekable)
            for pcap_frame in pcap_file.frames():
                print pcap_frame.time_recorded
