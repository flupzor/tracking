from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    """
    The PCAP sensor which was used as input.
    """

    name = models.CharField(max_length=100)


class ServiceSet(models.Model):
    """
    A serviceset which can consist of multiple BSSIDs.
    """

    ssid = models.CharField(max_length=100)


class Node(models.Model):
    """
    A Node in the 802.11 network.
    """
    addr = models.CharField(max_length=100)


class SignalStrength(models.Model):
    """
    The signal strength measured of a node. Useful
    to determine the distance from the Sensor.
    """
    datetime_recorded = models.DateTimeField()

    rssi = models.IntegerField(help_text="Received signal strength")
    iee80211_frame_sha256_hash = models.CharField(
        help_text="The hash over the IEEE8 802.11 that has been received.",
        max_length=64
    )


class ProbeReq(models.Model):
    """
    When a certain Node was seen looking for a certain Service Set
    """

    node = models.ForeignKey(Node)
    serviceset = models.ForeignKey(ServiceSet)

    datetime = models.DateTimeField()
    sensor = models.ForeignKey(Sensor)

    @classmethod
    def add_list(cls, sensor_name, probe_req_list):
        """
        A method to effeciently add a list of NodeSeen, Node, ServiceSet
        and Sensor models to the database.

        This method is efficient for bulk creation. It guarantees that only a constant
        amount of SQL queries will be executed.

        For certain inputs this function will be slower. Please test using the
        PerformanceTest in the test.py file
        """

        sensor, created = Sensor.objects.get_or_create(name=sensor_name)

        def bulk_create(model_cls, key, item_list):
            keys_to_create = set([item.get(key) for item in item_list])

            model_filter = {
                "{key}__in".format(key=key): keys_to_create,
            }

            # A list of ssids which already have been created.
            created_pk_and_key_list = model_cls.objects.filter(**model_filter).values('pk', key)
            created_key_list = [pk_and_key[key] for pk_and_key in created_pk_and_key_list]
            not_created_key_list = filter(lambda key: key not in created_key_list, keys_to_create)

            # And create the ServiceSets in one go.
            model_cls.objects.bulk_create(
                [model_cls(**{key: item_key}) for item_key in not_created_key_list]
            )

            newly_created_models = model_cls.objects.filter(**model_filter)

            return {getattr(new_model, key): new_model for new_model in newly_created_models}

        serviceset_list = bulk_create(ServiceSet, 'ssid', probe_req_list)
        node_list = bulk_create(Node, 'addr', probe_req_list)

        cls.objects.bulk_create(
            [
                cls(
                    node=node_list[probe_req['addr']],
                    serviceset=serviceset_list[probe_req['ssid']],
                    datetime=probe_req['datetime'],
                    sensor=sensor
                ) for probe_req in probe_req_list
            ]
        )
