import datetime

from django.test import TestCase
from django.utils import timezone

from .models import (
    ProbeReq, Node, ServiceSet,
    Sensor
)

import logging
logger = logging.getLogger(__name__)


class StoreTests(TestCase):
    def test_create(self):

        current_time = timezone.now()

        ProbeReq.add_list('sensor1', [
            {
                'ssid': 'abc',
                'addr': 'aa:bb:cc:dd:ee:ff',
                'datetime': current_time,
            }
        ])


        probe_req_qset = ProbeReq.objects.all()

        self.assertEquals(probe_req_qset.count(), 1)
        self.assertEquals(
            probe_req_qset.values('datetime')[0],
            { 'datetime': current_time }
        )

        service_set_qset = ServiceSet.objects.all()
        self.assertEquals(
            service_set_qset.values('ssid')[0],
            { 'ssid': u'abc' }
        )

        node_qset = Node.objects.all()
        self.assertEquals(
            node_qset.values('addr')[0],
            { 'addr': 'aa:bb:cc:dd:ee:ff' }
        )

        sensor_qset = Sensor.objects.all()
        self.assertEquals(
            sensor_qset.values('name')[0],
            { 'name': 'sensor1' }
        )

        probe_req = probe_req_qset[0]

        self.assertEqual(
            probe_req.node, node_qset[0]
        )

        self.assertEqual(
            probe_req.sensor, sensor_qset[0]
        )

class PerformanceTests(TestCase):
    def setUp(self):
        self.no_servicesets = 700
        self.no_nodes = 180
        self.no_probereqs = 50000

    def test_bulk_create(self):
        current_time = timezone.now()

        ssid_list = []
        for i in range(0, self.no_servicesets):
            ssid_list.append('ssid-{0}'.format(i))

        addr_list = []
        for i in range(0, self.no_nodes):
            addr_list.append('mac-{0}'.format(i))

        big_list = []
        for i in range(0, self.no_probereqs):
            big_list.append({
                'ssid': ssid_list[i % self.no_servicesets],
                'addr': addr_list[i % self.no_nodes],
                'datetime': current_time + datetime.timedelta(hours=i),
            })

        ProbeReq.add_list('file_name.pcap', big_list)

        time_finished = timezone.now()

        print("bulk took: {0}".format(time_finished - current_time))

        self.assertEqual(ProbeReq.objects.count(), self.no_probereqs)
        self.assertEqual(Node.objects.count(), self.no_nodes)
        self.assertEqual(ServiceSet.objects.count(), self.no_servicesets)


    def test_nonbulk_create(self):

        current_time = timezone.now()

        sensor, created = Sensor.objects.get_or_create(name='sensor1')

        ssid_list = []
        for i in range(0, self.no_servicesets):
            s = ServiceSet(ssid='ssid-{0}'.format(i))
            s.save()
            ssid_list.append(s)

        addr_list = []
        for i in range(0, self.no_nodes):
            n = Node(addr='mac-{0}'.format(i))
            n.save()

            addr_list.append(n)

        for i in range(0, self.no_probereqs):
            pr = ProbeReq(
                    serviceset=ssid_list[i % self.no_servicesets],
                    node=addr_list[i % self.no_nodes],
                    datetime=current_time + datetime.timedelta(hours=i),
                    sensor=sensor
                )

            pr.save()

        time_finished = timezone.now()

        print("nonbulk took: {0}".format(time_finished - current_time))

        self.assertEqual(ProbeReq.objects.count(), self.no_probereqs)
        self.assertEqual(Node.objects.count(), self.no_nodes)
        self.assertEqual(ServiceSet.objects.count(), self.no_servicesets)
