"""
 Copyright (c) 2024, Eeum, Inc.

 This software is licensed under the terms of the Revised BSD License.
 See LICENSE for details.
"""

# pylint: disable=duplicate-code
from asyncio import gather, create_task
from opencxl.util.component import RunnableComponent
from opencxl.cxl.device.cxl_type1_device import CXLType1Device
from opencxl.cxl.component.switch_connection_client import SwitchConnectionClient
from opencxl.cxl.component.cxl_component import CXL_COMPONENT_TYPE


class CxlType1DeviceClient(RunnableComponent):
    def __init__(
        self,
        port_index: int,
        host: str = "0.0.0.0",
        port: int = 8000,
    ):
        label = f"Port{port_index}"
        super().__init__(label)
        self._sw_conn_client = SwitchConnectionClient(
            port_index, CXL_COMPONENT_TYPE.LD, host=host, port=port
        )
        self._cxl_type1_device = CXLType1Device(
            transport_connection=self._sw_conn_client.get_cxl_connection(),
            label=label,
        )

    async def _run(self):
        tasks = [
            create_task(self._sw_conn_client.run()),
            create_task(self._cxl_type1_device.run()),
        ]
        await self._change_status_to_running()
        await gather(*tasks)

    async def _stop(self):
        tasks = [
            create_task(self._sw_conn_client.stop()),
            create_task(self._cxl_type1_device.stop()),
        ]
        await gather(*tasks)