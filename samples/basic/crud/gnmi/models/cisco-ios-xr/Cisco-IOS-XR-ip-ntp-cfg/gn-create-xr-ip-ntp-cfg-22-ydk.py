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
Create configuration for model Cisco-IOS-XR-ip-ntp-cfg.

usage: gn-create-xr-ip-ntp-cfg-22-ydk.py [-h] [-v] device

positional arguments:
  device         gNMI device (http://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.path import Repository
from ydk.services import CRUDService
from ydk.gnmi.providers import gNMIServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_ntp_cfg \
    as xr_ip_ntp_cfg
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_ntp(ntp):
    """Add config data to ntp object."""
    peer_vrf = ntp.peer_vrfs.PeerVrf()
    peer_vrf.vrf_name = "default"
    peer_ipv4 = peer_vrf.peer_ipv4s.PeerIpv4()
    peer_ipv4.address_ipv4 = "10.0.0.1"
    peer_type_ipv4 = peer_ipv4.PeerTypeIpv4()
    peer_type_ipv4.peer_type = xr_ip_ntp_cfg.NtpPeer.server
    peer_type_ipv4.source_interface = "Loopback0"
    peer_ipv4.peer_type_ipv4.append(peer_type_ipv4)
    peer_vrf.peer_ipv4s.peer_ipv4.append(peer_ipv4)
    ntp.peer_vrfs.peer_vrf.append(peer_vrf)
    ntp.update_calendar = Empty()


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="gNMI device (http://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create gNMI provider
    repository = Repository(YDK_REPO_DIR+device.hostname)
    provider = gNMIServiceProvider(repo=repository,
                                   address=device.hostname,
                                   port=device.port,
                                   username=device.username,
                                   password=device.password)
    # create CRUD service
    crud = CRUDService()

    ntp = xr_ip_ntp_cfg.Ntp()  # create object
    config_ntp(ntp)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, ntp)

    exit()
# End of script
