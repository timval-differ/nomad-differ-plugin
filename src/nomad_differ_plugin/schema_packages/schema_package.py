from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    'nomad_differ_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class NewSchemaPackage(Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    lab_id = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    data_file = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity)
    )
    process_time = Quantity(type=str, shape=['*'])
    header_timestamp = Quantity(type=str, shape=['*'])
    status = Quantity(type=str, shape=['*'])
    foreline_pressure = Quantity(type=float, shape=['*'])
    rheed_pressure = Quantity(type=float, shape=['*'])
    loadlock_main_pressure = Quantity(type=float, shape=['*'])
    process_pressure = Quantity(type=float, shape=['*'])
    main_pressure = Quantity(type=float, shape=['*'])
    loadlock_foreline_pressure = Quantity(type=float, shape=['*'])
    main_setpoint_pressure = Quantity(type=float, shape=['*'])
    mass_flow_ar_reading = Quantity(type=float, shape=['*'])
    mass_flow_n2_reading = Quantity(type=float, shape=['*'])
    mass_flow_o2_reading = Quantity(type=float, shape=['*'])
    mass_flow_ar_setpoint = Quantity(type=float, shape=['*'])
    mass_flow_n2_setpoint = Quantity(type=float, shape=['*'])
    mass_flow_o2_setpoint = Quantity(type=float, shape=['*'])
    main_turbo_current = Quantity(type=float, shape=['*'])
    rheed_turbo_current = Quantity(type=float, shape=['*'])
    loadlock_turbo_current = Quantity(type=float, shape=['*'])
    main_turbo_speed = Quantity(type=float, shape=['*'])
    rheed_turbo_speed = Quantity(type=float, shape=['*'])
    loadlock_turbo_speed = Quantity(type=float, shape=['*'])
    main_heating_setpoint = Quantity(type=float, shape=['*'])
    main_heating_reading = Quantity(type=float, shape=['*'])
    heating_output_power = Quantity(type=float, shape=['*'])
    pyrometer_control = Quantity(type=float, shape=['*'])
    pyrometer_emissivity = Quantity(type=float, shape=['*'])
    motion_hx = Quantity(type=float, shape=['*'])
    motion_hy = Quantity(type=float, shape=['*'])
    motion_hz = Quantity(type=float, shape=['*'])
    motion_ht = Quantity(type=float, shape=['*'])
    motion_hs = Quantity(type=float, shape=['*'])
    motion_shutter = Quantity(type=float, shape=['*'])
    motion_tx = Quantity(type=float, shape=['*'])
    motion_ty = Quantity(type=float, shape=['*'])
    motion_tz = Quantity(type=float, shape=['*'])
    motion_ts = Quantity(type=float, shape=['*'])
    ablation_laser_on = Quantity(type=str, shape=['*'])
    ablation_laser_pulse_counter = Quantity(type=float, shape=['*'])
    ablation_laser_repetition_rate = Quantity(type=float, shape=['*'])
    transfer_valve = Quantity(type=str, shape=['*'])
    gas_valve_1 = Quantity(type=str, shape=['*'])
    gas_valve_2 = Quantity(type=str, shape=['*'])
    gas_valve_3 = Quantity(type=str, shape=['*'])
    gas_valve_4 = Quantity(type=str, shape=['*'])
    gas_valve_5 = Quantity(type=str, shape=['*'])
    gas_valve_6 = Quantity(type=str, shape=['*'])
    gas_valve_7 = Quantity(type=str, shape=['*'])

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        logger.info('SputterDeposition.normalize', parameter=configuration.parameter)
        if self.lab_id is None and self.name is not None:
            self.lab_id = self.name


m_package.__init_metainfo__()
