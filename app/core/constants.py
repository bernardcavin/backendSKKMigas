from enum import Enum as PyEnum


class UnitType(PyEnum):
    METRICS = 'Metrics'
    IMPERIAL = 'Imperial'


uom = {
    UnitType.METRICS: {
        'Dimensionless': 'frac',
        'Time': 's',
        'Length': 'm',
        'Area': 'm²',
        'Volume': 'm³',
        'Weight': 'kg',
        'Amount of chemical substance': 'mol',
        'Molar mass': 'kg/mol',
        'Pipe Diameter': 'm',
        'Temperature': '°C',
        'Pressure': 'kPa',
        'Volumetric flow rate (oil & water)': 'cmd',
        'Volumetric flow rate (gas)': 'cmd',
        'GOR': 'm³/m³',
        'Density (liquids)': 'kg/m³',
        'Density (gases)': 'kg/m³',
        'Specific gravity': '1',
        'Compressibility': 'Pa⁻¹',
        'Permeability': 'm²',
        'Porosity': 'frac',
        'Dynamic Viscosity': 'Pa·s',
        'Productivity': 'm³/(Pa·s)',
        'Transmissibility': 'm³/(Pa·s)',
        'Pressure diffusivity': 'm²/s',
        'Wellbore storage': 'm³/Pa',
        'Thermal conductivity': 'W/(m·K)',
        'Specific heat capacity': 'J/(kg·K)',
        'Thermal diffusivity': 'm²/s'
    },
    UnitType.IMPERIAL: {
        'Dimensionless': 'frac',
        'Time': 'hr',
        'Length': 'ft',
        'Area': 'ft²',
        'Volume': 'bbl',
        'Weight': 'lb',
        'Amount of chemical substance': 'mol',
        'Molar mass': 'lb/mol',
        'Pipe Diameter': 'in',
        'Temperature': '°F',
        'Pressure': 'psi',
        'Volumetric flow rate (oil & water)': 'bpd',
        'Volumetric flow rate (gas)': 'scf/d',
        'GOR': 'scf/bbl',
        'Density (liquids)': 'lb/ft³',
        'Density (gases)': 'lb/ft³',
        'Specific gravity': '1',
        'Compressibility': 'psi⁻¹',
        'Permeability': 'md',
        'Porosity': 'frac',
        'Dynamic Viscosity': 'cp',
        'Productivity': 'bbl/(psi·d)',
        'Transmissibility': 'bbl/(psi·d)',
        'Pressure diffusivity': 'ft²/s',
        'Wellbore storage': 'bbl/psi',
        'Thermal conductivity': 'BTU/(hr·ft·°F)',
        'Specific heat capacity': 'BTU/(lb·°F)',
        'Thermal diffusivity': 'ft²/s'
    }
}