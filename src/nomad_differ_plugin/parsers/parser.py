from typing import (
    TYPE_CHECKING,
)

import csv
from collections import defaultdict
from pathlib import Path

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.parsing.parser import MatchingParser

from nomad_differ_plugin.schema_packages.schema_package import NewSchemaPackage

configuration = config.get_plugin_entry_point(
    'nomad_differ_plugin.parsers:parser_entry_point'
)


def _append_value(values: dict[str, list[str]], column: str, target: str, row: dict[str, str]) -> None:
    value = row.get(column)
    if value is None:
        return

    value = value.strip()
    if value == '':
        return

    values[target].append(value)


def _to_float_list(values: list[str]) -> list[float]:
    parsed_values: list[float] = []
    for value in values:
        try:
            parsed_values.append(float(value))
        except ValueError:
            continue
    return parsed_values


class NewParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('NewParser.parse', parameter=configuration.parameter)

        csv_path = Path(mainfile)
        if not csv_path.exists():
            raise FileNotFoundError(f'CSV file not found: {mainfile}')

        mapped_values: dict[str, list[str]] = defaultdict(list)
        column_map = {
            'timestamp': 'process_time',
            'Header:Timestamp [date,time]': 'header_timestamp',
            'Header:Status []': 'status',
            'Pressures:Foreline [mbar]': 'foreline_pressure',
            'Pressures:RHEED [mbar]': 'rheed_pressure',
            'Pressures:Loadlock Main [mbar]': 'loadlock_main_pressure',
            'Pressures:Process [mbar]': 'process_pressure',
            'Pressures:Main [mbar]': 'main_pressure',
            'Pressures:Loadlock foreline [mbar]': 'loadlock_foreline_pressure',
            'Pressures:Main setpoint [mbar]': 'main_setpoint_pressure',
            'Mass flows:Ar (reading) [sccm]': 'mass_flow_ar_reading',
            'Mass flows:N2 (reading) [sccm]': 'mass_flow_n2_reading',
            'Mass flows:O2 (reading) [sccm]': 'mass_flow_o2_reading',
            'Mass flows:Ar (setpoint) [sccm]': 'mass_flow_ar_setpoint',
            'Mass flows:N2 (setpoint) [sccm]': 'mass_flow_n2_setpoint',
            'Mass flows:O2 (setpoint) [sccm]': 'mass_flow_o2_setpoint',
            'Turbos:Main current [A]': 'main_turbo_current',
            'Turbos:RHEED current [A]': 'rheed_turbo_current',
            'Turbos:Loadlock current [A]': 'loadlock_turbo_current',
            'Turbos:Main speed [Hz]': 'main_turbo_speed',
            'Turbos:RHEED speed [Hz]': 'rheed_turbo_speed',
            'Turbos:Loadlock speed [Hz]': 'loadlock_turbo_speed',
            'Heating:Main (setpoint) [degC]': 'main_heating_setpoint',
            'Heating:Main (reading) [degC]': 'main_heating_reading',
            'Heating:Output power [%]': 'heating_output_power',
            'Pyrometers:Control [degC]': 'pyrometer_control',
            'Pyrometers:Control emissivity []': 'pyrometer_emissivity',
            'Motion:HX [mm]': 'motion_hx',
            'Motion:HY [mm]': 'motion_hy',
            'Motion:HZ [mm]': 'motion_hz',
            'Motion:HT [deg]': 'motion_ht',
            'Motion:HS [deg]': 'motion_hs',
            'Motion:Shutter [deg]': 'motion_shutter',
            'Motion:TX [mm]': 'motion_tx',
            'Motion:TY [mm]': 'motion_ty',
            'Motion:TZ [mm]': 'motion_tz',
            'Motion:TS [deg]': 'motion_ts',
            'Optical:Abblation laser on []': 'ablation_laser_on',
            'Optical:Abblation laser pulse counter []': 'ablation_laser_pulse_counter',
            'Optical:Abblation laser repetition rate [Hz]': 'ablation_laser_repetition_rate',
            'Valves:Transfer Valve []': 'transfer_valve',
            'Gas valves:Gas Valve 1 []': 'gas_valve_1',
            'Gas valves:Gas Valve 2 []': 'gas_valve_2',
            'Gas valves:Gas Valve 3 []': 'gas_valve_3',
            'Gas valves:Gas Valve 4 []': 'gas_valve_4',
            'Gas valves:Gas Valve 5 []': 'gas_valve_5',
            'Gas valves:Gas Valve 6 []': 'gas_valve_6',
            'Gas valves:Gas Valve 7 []': 'gas_valve_7',
        }

        with csv_path.open('r', encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                for column, target in column_map.items():
                    _append_value(mapped_values, column, target, row)

        data = NewSchemaPackage()
        data.name = csv_path.stem
        data.lab_id = csv_path.split('-')[0]
        data.data_file = str(csv_path)
        data.process_time = mapped_values['process_time']
        data.header_timestamp = mapped_values['header_timestamp']
        data.status = mapped_values['status']
        data.foreline_pressure = _to_float_list(mapped_values['foreline_pressure'])
        data.rheed_pressure = _to_float_list(mapped_values['rheed_pressure'])
        data.loadlock_main_pressure = _to_float_list(mapped_values['loadlock_main_pressure'])
        data.process_pressure = _to_float_list(mapped_values['process_pressure'])
        data.main_pressure = _to_float_list(mapped_values['main_pressure'])
        data.loadlock_foreline_pressure = _to_float_list(mapped_values['loadlock_foreline_pressure'])
        data.main_setpoint_pressure = _to_float_list(mapped_values['main_setpoint_pressure'])
        data.mass_flow_ar_reading = _to_float_list(mapped_values['mass_flow_ar_reading'])
        data.mass_flow_n2_reading = _to_float_list(mapped_values['mass_flow_n2_reading'])
        data.mass_flow_o2_reading = _to_float_list(mapped_values['mass_flow_o2_reading'])
        data.mass_flow_ar_setpoint = _to_float_list(mapped_values['mass_flow_ar_setpoint'])
        data.mass_flow_n2_setpoint = _to_float_list(mapped_values['mass_flow_n2_setpoint'])
        data.mass_flow_o2_setpoint = _to_float_list(mapped_values['mass_flow_o2_setpoint'])
        data.main_turbo_current = _to_float_list(mapped_values['main_turbo_current'])
        data.rheed_turbo_current = _to_float_list(mapped_values['rheed_turbo_current'])
        data.loadlock_turbo_current = _to_float_list(mapped_values['loadlock_turbo_current'])
        data.main_turbo_speed = _to_float_list(mapped_values['main_turbo_speed'])
        data.rheed_turbo_speed = _to_float_list(mapped_values['rheed_turbo_speed'])
        data.loadlock_turbo_speed = _to_float_list(mapped_values['loadlock_turbo_speed'])
        data.main_heating_setpoint = _to_float_list(mapped_values['main_heating_setpoint'])
        data.main_heating_reading = _to_float_list(mapped_values['main_heating_reading'])
        data.heating_output_power = _to_float_list(mapped_values['heating_output_power'])
        data.pyrometer_control = _to_float_list(mapped_values['pyrometer_control'])
        data.pyrometer_emissivity = _to_float_list(mapped_values['pyrometer_emissivity'])
        data.motion_hx = _to_float_list(mapped_values['motion_hx'])
        data.motion_hy = _to_float_list(mapped_values['motion_hy'])
        data.motion_hz = _to_float_list(mapped_values['motion_hz'])
        data.motion_ht = _to_float_list(mapped_values['motion_ht'])
        data.motion_hs = _to_float_list(mapped_values['motion_hs'])
        data.motion_shutter = _to_float_list(mapped_values['motion_shutter'])
        data.motion_tx = _to_float_list(mapped_values['motion_tx'])
        data.motion_ty = _to_float_list(mapped_values['motion_ty'])
        data.motion_tz = _to_float_list(mapped_values['motion_tz'])
        data.motion_ts = _to_float_list(mapped_values['motion_ts'])
        data.ablation_laser_on = mapped_values['ablation_laser_on']
        data.ablation_laser_pulse_counter = _to_float_list(mapped_values['ablation_laser_pulse_counter'])
        data.ablation_laser_repetition_rate = _to_float_list(mapped_values['ablation_laser_repetition_rate'])
        data.transfer_valve = mapped_values['transfer_valve']
        data.gas_valve_1 = mapped_values['gas_valve_1']
        data.gas_valve_2 = mapped_values['gas_valve_2']
        data.gas_valve_3 = mapped_values['gas_valve_3']
        data.gas_valve_4 = mapped_values['gas_valve_4']
        data.gas_valve_5 = mapped_values['gas_valve_5']
        data.gas_valve_6 = mapped_values['gas_valve_6']
        data.gas_valve_7 = mapped_values['gas_valve_7']

        archive.data = data
