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
Encode config for model openconfig-routing-policy.

usage: cd-encode-config-routing-policy-28-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.routing import routing_policy as oc_routing_policy
from ydk.models.bgp import bgp_policy as oc_bgp_policy
from ydk.types import Empty
import logging


def config_routing_policy(routing_policy):
    """Add config data to routing_policy object."""
    # configure policy definition
    policy_definition = routing_policy.policy_definitions.PolicyDefinition()
    policy_definition.name = "POLICY4"
    statement = policy_definition.statements.Statement()
    statement.name = "next-hop-self"
    set_next_hop = oc_bgp_policy.BgpNextHopTypeEnum.SELF
    statement.actions.bgp_actions.set_next_hop = set_next_hop
    statement.actions.accept_route = Empty()
    policy_definition.statements.statement.append(statement)
    routing_policy.policy_definitions.policy_definition.append(policy_definition)


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

    routing_policy = oc_routing_policy.RoutingPolicy()  # create config object
    config_routing_policy(routing_policy)  # add object configuration

    print(codec.encode(provider, routing_policy))  # encode and print object
    provider.close()
    exit()
# End of script
