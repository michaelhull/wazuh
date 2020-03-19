# Copyright (C) 2015-2020, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import logging

from aiohttp import web

import wazuh.syscollector as syscollector
from api.encoder import dumps
from api.util import remove_nones_to_dict, parse_api_param, raise_if_exc
from wazuh.core.cluster.dapi.dapi import DistributedAPI

logger = logging.getLogger('wazuh')


async def get_hardware_info(request, agent_id, pretty=False, wait_for_complete=False, select=None):
    """ Get hardware info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param select: Select which fields to return (separated by comma)
    :return: Data
    """
    f_kwargs = {'agent_list': [agent_id],
                'select': select,
                'element_type': 'hardware'}
    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_hotfix_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None, sort=None,
                          search=None, select=None, hotfix=None):
    """ Get info about an agent's hotfixes

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/. at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param select: Select which fields to return (separated by comma)
    :param hotfix: Filters by hotfix in Windows agents
    :return:
    """

    filters = {'hotfix': hotfix}

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'hotfixes'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_network_address_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None,
                                   select=None, sort=None, search=None, iface=None, proto=None, address=None,
                                   broadcast=None, netmask=None):
    """ Get network address info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param iface: Filters by interface name
    :param proto: Filters by IP protocol
    :param address: IP address associated with the network interface
    :param broadcast: Filters by broadcast direction
    :param netmask: Filters by netmask
    :return: Data
    """
    filters = {'iface': iface,
               'proto': proto,
               'address': address,
               'broadcast': broadcast,
               'netmask': netmask}

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'netaddr'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_network_interface_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None,
                                     select=None, sort=None, search=None, name=None, adapter=None, state=None,
                                     mtu=None):
    """ Get network interface info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param name: Name of the network interface
    :param adapter: Filters by adapter
    :param state: Filters by state
    :param mtu: Filters by mtu
    :return: Data
    """
    filters = {'adapter': adapter,
               'type': request.query.get('type', None),
               'state': state,
               'name': name,
               'mtu': mtu}
    # Add nested fields to kwargs filters
    nested = ['tx.packets', 'rx.packets', 'tx.bytes', 'rx.bytes', 'tx.errors', 'rx.errors', 'tx.dropped', 'rx.dropped']
    for field in nested:
        filters[field] = request.query.get(field, None)

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'netiface'
                }

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_network_protocol_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None,
                                    select=None, sort=None, search=None, iface=None, gateway=None, dhcp=None):
    """ Get network protocol info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param iface: Filters by iface
    :param gateway: Filters by gateway
    :param dhcp: Filters by dhcp
    :return: Data
    """
    filters = {'iface': iface,
               'type': request.query.get('type', None),
               'gateway': gateway,
               'dhcp': dhcp}

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'netproto'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_os_info(request, agent_id, pretty=False, wait_for_complete=False, select=None):
    """ Get OS info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param select: Select which fields to return (separated by comma)
    :return: Data
    """
    f_kwargs = {'agent_list': [agent_id],
                'select': select,
                'element_type': 'os'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_packages_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None, select=None,
                            sort=None, search=None, vendor=None, name=None, architecture=None, version=None):
    """ Get packages info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param vendor: Filters by vendor
    :param name: Filters by name
    :param architecture: Filters by architecture
    :param version: Filters by version
    :return: Data
    """
    filters = {'vendor': vendor,
               'name': name,
               'architecture': architecture,
               'format': request.query.get('format', None),
               'version': version}

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'packages'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_ports_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None, select=None,
                         sort=None, search=None, pid=None, protocol=None, tx_queue=None, state=None, process=None):
    """ Get ports info of an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param pid: Filters by pid
    :param protocol: Filters by protocol
    :param tx_queue: Filters by tx_queue
    :param state: Filters by state
    :param process: Filters by process
    :return: Data
    """
    filters = {'pid': pid,
               'protocol': protocol,
               'tx_queue': tx_queue,
               'state': state,
               'process': process}
    # Add nested fields to kwargs filters
    nested = ['local.ip', 'local.port', 'remote.ip']
    for field in nested:
        filters[field] = request.query.get(field, None)

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'ports'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)


async def get_processes_info(request, agent_id, pretty=False, wait_for_complete=False, offset=0, limit=None,
                             select=None, sort=None, search=None, pid=None, state=None, ppid=None, egroup=None,
                             euser=None, fgroup=None, name=None, nlwp=None, pgrp=None, priority=None, rgroup=None,
                             ruser=None, sgroup=None, suser=None):
    """ Get processes info an agent

    :param agent_id: Agent ID
    :param pretty: Show results in human-readable format
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
    ascending or descending order.
    :param search: Looks for elements with the specified string
    :param pid: Filters by process pid
    :param state: Filters by process state
    :param ppid: Filters by process parent pid
    :param egroup: Filters by process egroup
    :param euser Filters by process euser
    :param fgroup: Filters by process fgroup
    :param name: Filters by process name
    :param nlwp: Filters by process nlwp
    :param pgrp: Filters by process pgrp
    :param priority: Filters by process priority
    :param rgroup: Filters by process rgroup
    :param ruser: Filters by process ruser
    :param sgroup: Filters by process sgroup
    :param suser: Filters by process suser
    :return: Data
    """
    filters = {'state': state,
               'pid': pid,
               'ppid': ppid,
               'egroup': egroup,
               'euser': euser,
               'fgroup': fgroup,
               'name': name,
               'nlwp': nlwp,
               'pgrp': pgrp,
               'priority': priority,
               'rgroup': rgroup,
               'ruser': ruser,
               'sgroup': sgroup,
               'suser': suser}

    f_kwargs = {'agent_list': [agent_id],
                'offset': offset,
                'limit': limit,
                'select': select,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'filters': filters,
                'element_type': 'processes'}

    dapi = DistributedAPI(f=syscollector.get_item_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=dumps)
