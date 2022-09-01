# Copyright (c) 2021 Microsoft Open Technologies, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#    THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
#    CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
#    LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
#    FOR A PARTICULAR PURPOSE, MERCHANTABILITY OR NON-INFRINGEMENT.
#
#    See the Apache Version 2.0 License for specific language governing
#    permissions and limitations under the License.
#
#    Microsoft would like to thank the following companies for their review and
#    assistance with these files: Intel Corporation, Mellanox Technologies Ltd,
#    Dell Products, L.P., Facebook, Inc., Marvell International Ltd.
#
#
from time import sleep


from sai_test_base import T0TestBase
from sai_thrift.sai_headers import *
from ptf import config
from ptf.testutils import *
from ptf.thriftutils import *
from sai_utils import *
from config.fdb_configer import t0_fdb_tear_down_helper


class Vlan_Domain_Forwarding_Test(T0TestBase):
    """
    Verify the basic VLAN forwarding.
    In L2, if segement with VLAN tag and sends to a VLAN port, 
    segment should be forwarded inside a VLAN domain.
    """

    def setUp(self):
        """
        Set up test
        """
        T0TestBase.setUp(self, is_reset_default_vlan=False)

    def runTest(self):
        """
        Test VLAN forwarding
        """
        try:
            print("VLAN forwarding test.")
            for index in range(2, 9):
                print("Forwarding in VLAN {} from {} to port: {}".format(
                    10,
                    self.dut.port_obj_list[1].dev_port_index,
                    self.dut.port_obj_list[index].dev_port_index))
                pkt = simple_udp_packet(eth_dst=self.servers[1][index].mac,
                                        eth_src=self.servers[1][1].mac,
                                        vlan_vid=10,
                                        ip_id=101,
                                        ip_ttl=64)

                send_packet(
                    self, self.dut.port_obj_list[1].dev_port_index, pkt)
                verify_packet(
                    self, pkt, self.dut.port_obj_list[index].dev_port_index)
                verify_no_other_packets(self, timeout=1)

            for index in range(10, 17):
                print("Forwarding in VLAN {} from {} to port: {}".format(
                    20,
                    self.dut.port_obj_list[9].dev_port_index,
                    self.dut.port_obj_list[index].dev_port_index))
                pkt = simple_udp_packet(eth_dst=self.servers[1][index].mac,
                                        eth_src=self.servers[1][9].mac,
                                        vlan_vid=20,
                                        ip_id=101,
                                        ip_ttl=64)
                send_packet(
                    self, self.dut.port_obj_list[9].dev_port_index, pkt)
                verify_packet(
                    self, pkt, self.dut.port_obj_list[index].dev_port_index)
                verify_no_other_packets(self, timeout=1)
        finally:
            pass

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()


class UntagAccessToAccessTest(T0TestBase):
    """
    This test verifies the VLAN function around untag and access ports.
    """

    def setUp(self):
        super().setUp()

    def runTest(self):
        """
        Forwarding between tagged ports with untagged pkt
        """
        print("\nUntagAccessToAccessTest()")
        try:
            for index in range(2, 9):
                print("Sending untagged packet from vlan10 tagged port {} to vlan10 tagged port: {}".format(
                    self.dut.port_obj_list[1].dev_port_index,
                    self.dut.port_obj_list[index].dev_port_index))
                pkt = simple_udp_packet(eth_dst=self.servers[1][index].mac,
                                        eth_src=self.servers[1][1].mac,
                                        ip_id=101,
                                        ip_ttl=64)
                send_packet(
                    self, self.dut.port_obj_list[1].dev_port_index, pkt)
                verify_packet(
                    self, pkt, self.dut.port_obj_list[index].dev_port_index)
                verify_no_other_packets(self, timeout=2)
            for index in range(10, 17):
                print("Sending untagged packet from vlan20 tagged port {} to vlan20 tagged port: {}".format(
                    self.dut.port_obj_list[9].dev_port_index,
                    self.dut.port_obj_list[index].dev_port_index))
                pkt = simple_udp_packet(eth_dst=self.servers[1][index].mac,
                                        eth_src=self.servers[1][9].mac,
                                        ip_id=101,
                                        ip_ttl=64)
                send_packet(
                    self, self.dut.port_obj_list[9].dev_port_index, pkt)
                verify_packet(
                    self, pkt, self.dut.port_obj_list[index].dev_port_index)
                verify_no_other_packets(self, timeout=2)
        finally:
            pass

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()


class MismatchDropTest(T0TestBase):
    """
    This test verifies the VLAN function around untag and access ports.
    """

    def setUp(self):
        super().setUp()

    def runTest(self):
        """
        Dropping between tagged ports with mismatched tagged pkt
        """
        print("\nUnmatchDropTest()")
        try:
            for index in range(1, 9):
                print("Sending vlan20 tagged packet from vlan20 tagged port {} to vlan10 tagged port: {}".format(
                    self.dut.port_obj_list[9].dev_port_index,
                    self.dut.port_obj_list[index].dev_port_index))
                pkt = simple_udp_packet(eth_dst=self.servers[1][index].mac,
                                        eth_src=self.servers[1][9].mac,
                                        vlan_vid=20,
                                        ip_id=101,
                                        ip_ttl=64)
                send_packet(
                    self, self.dut.port_obj_list[9].dev_port_index, pkt)
                verify_no_other_packets(self, timeout=2)
            for index in range(9, 17):
                print("Sending vlan10 tagged packet from {} to vlan20 tagged port: {}".format(
                    self.dut.port_obj_list[1].dev_port_index,
                    self.dut.port_obj_list[index].dev_port_index))
                pkt = simple_udp_packet(eth_dst=self.servers[1][index].mac,
                                        eth_src=self.servers[1][1].mac,
                                        vlan_vid=10,
                                        ip_id=101,
                                        ip_ttl=64)
                send_packet(
                    self, self.dut.port_obj_list[1].dev_port_index, pkt)
                verify_no_other_packets(self, timeout=2)
        finally:
            pass

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()


class TaggedVlanFloodingTest(T0TestBase):
    """
    For mac flooding in the VLAN scenario, before learning the mac address from the packet,
    the packet sent to the VLAN port will flood to other ports, and the egress ports
    will be in the same VLAN as the ingress port.
    """

    def setUp(self):
        super().setUp()

    def runTest(self):
        print("\nTaggedVlanFloodingTest")
        try:
            macX = 'EE:EE:EE:EE:EE:EE'
            pkt = simple_udp_packet(eth_dst=macX,
                                    eth_src=self.servers[1][1].mac,
                                    vlan_vid=10,
                                    ip_id=101,
                                    ip_ttl=64)
            send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
            print(self.dut.vlans[10].port_idx_list)
            verify_each_packet_on_multiple_port_lists(self, [pkt], [self.get_dev_port_indexes(
                list(filter(lambda item: item != 1, self.dut.vlans[10].port_idx_list)))])
        finally:
            pass

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()


class UnTaggedVlanFloodingTest(T0TestBase):
    """
    UnTaggedVlanFloodingTest
    For mac flooding in the VLAN scenario, before learning the mac address from the packet,
    the packet sent to the VLAN port will flood to other ports, and the egress ports
    will be in the same VLAN as the ingress port.
    """

    def setUp(self):
        super().setUp()

    def runTest(self):
        print("\nUnTaggedVlanFloodingTest")
        try:
            macX = 'EE:EE:EE:EE:EE:EE'
            pkt = simple_udp_packet(eth_dst=macX,
                                    eth_src=self.servers[1][1].mac,
                                    ip_id=101,
                                    ip_ttl=64)
            send_packet(self, self.dut.port_obj_list[1].dev_port_index, pkt)
            verify_each_packet_on_multiple_port_lists(self, [pkt], [self.get_dev_port_indexes(
                list(filter(lambda item: item != 1, self.dut.vlans[10].port_idx_list)))])
        finally:
            pass

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()


class BroadcastTest(T0TestBase):
    """
    Drop untagged packet when the destination port from MAC table search
    is the port which packet comes into the switch.
    """

    def setUp(self):
        super().setUp()

    def runTest(self):
        print("\nBroadcastTest")
        try:
            macX = 'FF:FF:FF:FF:FF:FF'
            # untag
            untagged_pkt = simple_udp_packet(eth_dst=macX,
                                             eth_src=self.servers[1][1].mac,
                                             ip_id=101,
                                             ip_ttl=64)
            send_packet(
                self, self.dut.port_obj_list[1].dev_port_index, untagged_pkt)
            verify_each_packet_on_multiple_port_lists(self, [untagged_pkt], [self.get_dev_port_indexes(
                list(filter(lambda item: item != 1, self.dut.vlans[10].port_idx_list)))])
            # tag
            tagged_pkt = simple_udp_packet(eth_dst=macX,
                                           eth_src=self.servers[1][1].mac,
                                           vlan_vid=10,
                                           ip_id=101,
                                           ip_ttl=64)
            send_packet(
                self, self.dut.port_obj_list[1].dev_port_index, tagged_pkt)
            verify_each_packet_on_multiple_port_lists(self, [tagged_pkt], [self.get_dev_port_indexes(
                list(filter(lambda item: item != 1, self.dut.vlans[10].port_idx_list)))])
        finally:
            pass

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()


class ArpRequestFloodingTest(T0TestBase):
    """
    This test verifies the flooding when receive a arp request
    """

    def setUp(self):
        T0TestBase.setUp(self, is_reset_default_vlan=False)
        ip2 = "192.168.0.2"
        self.arp_request = simple_arp_packet(
            eth_dst=self.servers[1][2].mac,
            arp_op=1,
            ip_tgt=ip2,
            hw_tgt=self.servers[1][2].mac)

    def runTest(self):
        print("ArpRequestFloodingTest")
        send_packet(
            self, self.dut.port_obj_list[1].dev_port_index, self.arp_request)
        verify_each_packet_on_multiple_port_lists(
            self, [self.arp_request], [self.get_dev_port_indexes(list(filter(lambda item: item != 1, self.dut.vlans[10].port_idx_list)))])

    def tearDown(self):
        """
        TearDown process
        """
        super().tearDown()
