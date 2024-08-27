import React, { useEffect, useState } from 'react'
import { Box, FormControl, FormLabel, Input, Select, SimpleGrid, Textarea } from '@chakra-ui/react'
import { AllEnums } from '../API/AllEnums'

const TeknisForms = () => {
    const [allEnum, setAllEnum] = React.useState([]);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);

    const [sendData, setSendData] = useState({
        planned_well: {
            uwi: "string",
            field_id: "string",
            well_name: "string",
            alias_long_name: "string",
            well_type: "OIL",
            well_class: "WILDCAT",
            well_status: "Active",
            profile_type: "DIRECTIONAL",
            environment_type: "MARINE",
            surface_longitude: 0,
            surface_latitude: 0,
            bottom_hole_longitude: 0,
            bottom_hole_latitude: 0,
            maximum_inclination: 0,
            maximum_azimuth: 0,
            line_name: "string",
            spud_date: "2024-08-22T00:01:22.270Z",
            final_drill_date: "2024-08-22T00:01:22.270Z",
            completion_date: "2024-08-22T00:01:22.270Z",
            rotary_table_elev: 0,
            rotary_table_elev_ouom: "FEET",
            kb_elev: 0,
            kb_elev_ouom: "FEET",
            derrick_floor_elev: 0,
            derrick_floor_elev_ouom: "FEET",
            ground_elev: 0,
            ground_elev_ouom: "FEET",
            mean_sea_level: 0,
            mean_sea_level_ouom: "RT",
            depth_datum: "RT",
            kick_off_point: 0,
            kick_off_point_ouom: "FEET",
            drill_td: 0,
            drill_td_ouom: "FEET",
            log_td: 0,
            log_td_ouom: "FEET",
            max_tvd: 0,
            max_tvd_ouom: "FEET",
            projected_depth: 0,
            projected_depth_ouom: "FEET",
            final_td: 0,
            final_td_ouom: "FEET",
            remark: "string",
            id: "string",


        }
    })

    const handleOnChange = (e) => {
        const { name, value } = e.target;
        setSendData({
            planned_well: {
                ...sendData.planned_well,
                [name]: value
            }
        });

    };

    console.log(sendData);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await AllEnums();
                setAllEnum(data);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [setAllEnum]); //




    return (
        <>
            <Box>
                <Box fontWeight="bold">Well</Box>
                <SimpleGrid columns={2} spacing={4}>
                    <FormControl>
                        <FormLabel>UWI</FormLabel>
                        <Input placeholder="Well UWI" onChange={handleOnChange} name='uwi' required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Nama Sumur</FormLabel>
                        <Input placeholder="Nama Sumur" name='well_name' required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Nama Lengkap Sumur</FormLabel>
                        <Input placeholder="Nama Lengkap Sumur" name='alias_long_name' required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Type Well</FormLabel>
                        <Select placeholder="Dropdown Get API" name='well_type' required>
                            {allEnum.well_type && Object.entries(allEnum.well_type).map(([key, value]) => (
                                <option key={key} value={value}>{value}</option>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Well Status</FormLabel>
                        <Select placeholder="Dropdown Get API" name='well_status' required>
                            {allEnum.well_status && Object.entries(allEnum.well_status).map(([key, value]) => (
                                <option key={key} value={value}>{value}</option>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Hydrocarbon Target</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {allEnum.well_status && Object.entries(allEnum.well_status).map(([key, value]) => (
                                <option key={key} value={value}>{value}</option>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Well Profile Type</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Environment Type</FormLabel>
                        <Input placeholder="Environment Type" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Surface Longitude</FormLabel>
                        <Input placeholder="Surface Longitude" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Surface Latitude</FormLabel>
                        <Input placeholder="Surface Latitude" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Bottom Hole Longitude</FormLabel>
                        <Input placeholder="Bottom Hole Longitude" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Bottom Hole Latitude</FormLabel>
                        <Input placeholder="Bottom Hole Latitude" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Maximum Inclination</FormLabel>
                        <Input placeholder="Maximum Inclination" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Azimuth</FormLabel>
                        <Input placeholder="Azimuth" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Line Name</FormLabel>
                        <Input placeholder="Line Name" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Spud Date</FormLabel>
                        <Input type="date" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Final Drill Date</FormLabel>
                        <Input type="date" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Completion Date</FormLabel>
                        <Input type="date" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Rotary Table Elev</FormLabel>
                        <Input placeholder="Rotary Table Elev" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Rotary Table Elev UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Kb Elev</FormLabel>
                        <Input placeholder="Kb Elev" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Kb Elev UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Derrick Floor Elev</FormLabel>
                        <Input placeholder="Derrick Floor Elev" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Derrick Floor Elev UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Ground Elev</FormLabel>
                        <Input placeholder="Ground Elev" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Ground Elev UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Mean Sea Level</FormLabel>
                        <Input placeholder="Mean Sea Level" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Mean Sea Level UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Depth Datum</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <Box></Box> {/* Empty box for alignment */}
                    <FormControl>
                        <FormLabel>Kick Off Point</FormLabel>
                        <Input placeholder="Kick Off Point" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Kick Off Point UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Maximum TVD</FormLabel>
                        <Input placeholder="Maximum TVD" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Maximum TVD UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Final MD</FormLabel>
                        <Input placeholder="Final MD" required />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Final MD UOM</FormLabel>
                        <Select placeholder="Dropdown Get API" required>
                            {/* Options would be populated from API */}
                        </Select>
                    </FormControl>
                    <FormControl gridColumn="span 2">
                        <FormLabel>Remark</FormLabel>
                        <Textarea placeholder="Remark" required />
                    </FormControl>
                </SimpleGrid>
            </Box>
        </>
    )
}

export default TeknisForms