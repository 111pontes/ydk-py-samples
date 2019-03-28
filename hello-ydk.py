#!/usr/bin/env python3
#
# Copyright 2019 Cisco Systems, Inc.
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
# Read all data for model Cisco-IOS-XR-shellutil-oper and print system
# uptime.
#
# usage: hello-ydk.py
#

import sys
from datetime import timedelta

# model, service and provider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider


if __name__ == "__main__":
    """Main execution path"""

    # create NETCONF session
    provider = NetconfServiceProvider(address="10.0.0.1",
                                      username="admin",
                                      password="admin")

    # create CRUD service
    crud = CRUDService()

    # create system time object
    system_time = Cisco_IOS_XR_shellutil_oper.SystemTime()

    # read system time from device
    system_time = crud.read(provider, system_time)

    # print system uptime
    print("System uptime is " +
          str(timedelta(seconds=system_time.uptime.uptime)))

    sys.exit()
# End of script
