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
Read all data for model Cisco-IOS-XR-linux-os-reboot-history-oper.

usage: nc-read-xr-linux-os-reboot-history-oper-20-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_linux_os_reboot_history_oper \
    as xr_linux_os_reboot_history_oper
import textwrap
import logging


def process_reboot_history(reboot_history):
    """
    Process data in file_system object.

    Inspired by format in 'show reboot history'.
    """
    # format string for reboot history header
    reboot_history_header = textwrap.dedent("""
        Node: RP/{node}
        ------------------------------------------------------------
        No  Time                      Cause Code  Reason
        --------------------------------------------------------------------------------
        """).strip()
    # format string for reboot history row
    reboot_history_row = textwrap.dedent("""
        {no:0>2}  {time:<25} 0x{cause_code:0>8x}  {reason}
        """).rstrip()

    show_reboot_history = str()
    # iterate over all nodes
    for node in reboot_history.node:
        show_reboot_history += reboot_history_header.format(node=node.node_name)
        # iterate over all reboot history entries
        for reboot_history in node.reboot_history:
            show_reboot_history += reboot_history_row.format(no=reboot_history.no,
                                                             time=reboot_history.time,
                                                             cause_code=reboot_history.cause_code,
                                                             reason=reboot_history.reason)

    # return formatted string
    return(show_reboot_history)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create CRUD service
    crud = CRUDService()

    reboot_history = xr_linux_os_reboot_history_oper.RebootHistory()  # create object

    # read data from NETCONF device
    reboot_history = crud.read(provider, reboot_history)
    print(process_reboot_history(reboot_history))  # process object data

    provider.close()
    exit()
# End of script
