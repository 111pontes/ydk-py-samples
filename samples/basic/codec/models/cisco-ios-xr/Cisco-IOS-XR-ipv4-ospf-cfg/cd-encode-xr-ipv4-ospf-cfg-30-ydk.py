#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Encode configuration for model Cisco-IOS-XR-ipv4-ospf-cfg.

usage: cd-encode-xr-ipv4-ospf-cfg-30-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_ospf_cfg \
    as xr_ipv4_ospf_cfg
from ydk.types import Empty
import logging


def config_ospf(ospf):
    """Add config data to ospf object."""
    # OSPF process
    process = ospf.processes.Process()
    process.process_name = "DEFAULT"
    process.default_vrf.router_id = "172.16.255.1"
    process.start = Empty()

    # Area 0
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 0
    area_area_id.running = Empty()

    # loopback interface passive
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "Loopback0"
    name_scope.running = Empty()
    name_scope.passive = True
    area_area_id.name_scopes.name_scope.append(name_scope)

    # gi0/0/0/0 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/0"
    name_scope.running = Empty()
    name_scope.network_type = xr_ipv4_ospf_cfg.OspfNetworkEnum.point_to_point
    area_area_id.name_scopes.name_scope.append(name_scope)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # Area 1
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 1
    area_area_id.running = Empty()

    # gi0/0/0/1 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/1"
    name_scope.running = Empty()
    name_scope.network_type = xr_ipv4_ospf_cfg.OspfNetworkEnum.point_to_point
    area_area_id.name_scopes.name_scope.append(name_scope)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # append process config
    ospf.processes.process.append(process)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    ospf = xr_ipv4_ospf_cfg.Ospf()  # create object
    config_ospf(ospf)  # add object configuration

    # encode and print object
    print(codec.encode(provider, ospf))

    provider.close()
    exit()
# End of script
