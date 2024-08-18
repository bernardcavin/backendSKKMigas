import React from 'react'
import { Card, CardBody, CardHeader, Input, Typography, Select, Option, Button, CardFooter } from '@material-tailwind/react'
import { useState, useEffect } from 'react'
import RadioButton from './ChildComponets/RadioButton';
import DateRangePicker from './ChildComponets/DateRangePicker';
import { Cog8ToothIcon, GlobeAsiaAustraliaIcon, UserGroupIcon } from '@heroicons/react/24/outline';
import axios from 'axios';
import CardPageSumur from './Forms/FormPageSumur';
import FormHSEPlan from './Forms/FormPageDrilling';
import FormPageLainnya from './Forms/FormPageLainnya';
import FormPagePersonel from './Forms/FormPagePersonel';
import FormPagePosisi from './Forms/FormPagePosisi';
import FormPageSchedule from './Forms/FormPageSchedule';
import FormPageTrajectory from './Forms/FormPageTrajectory';
import FormPageCasing from './Forms/FormPageCasing';
import FormPageDepthVSDays from './Forms/FormPageDepthVSDays';
import FormPageWBS from './Forms/FormPageWBS';
import FormDepthVSDays from './Forms/FormPageDepthVSDays';
import FormWellStrat from './Forms/FormPageWellStrat';
import FormPageDrilling from './Forms/FormPageDrilling';
import CardPageJob from './Forms/FormPageJob';

const FormInput = () => {

    const [pekerjaan, setPekerjaan] = useState('');
    const [tipeKontrak, setTipeKontrak] = useState('');


    const handleAllData = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, ...data
            }
            // Menggabungkan data baru dengan data lama jika diperlukan
        }));

    };
    const handleDataWellStrac = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, planned_well: {
                    ...prevState.job.planned_well, well_strat: {
                        ...prevState.job.planned_well.well_strat, ...data
                    }
                }
            }

        }));

    };
    const handleDataPageDepth = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, job_activity: {
                    ...prevState.job.job_activity, ...data
                }
            }

        }));

    };
    const handleDataWBS = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, work_breakdown_structure: {
                    ...prevState.job.work_breakdown_structure, ...data
                }
            }

        }));

    };
    const handleDataDrilling = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, drilling_hazard: {
                    ...prevState.job.drilling_hazard, ...data
                }
            }

        }));

    };
    const handleDataCasing = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, planned_well: {
                    ...prevState.job.planned_well, well_casing: {
                        ...prevState.job.planned_well.well_casing, ...data
                    }
                }
            }

        }));

    };
    const handleDataSumur = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job, planned_well: {
                    ...prevState.job.planned_well, ...data
                }
            }

        }));

    };




    const initialJobActivity = {
        time: new Date().toISOString(),
        measured_depth: 0,
        measured_depth_uoum: "FEET",
        measured_depth_datum: "RT",
        true_vertical_depth: 0,
        true_vertical_depth_uoum: "FEET",
        true_vertical_depth_sub_sea: 0,
        true_vertical_depth_sub_sea_uoum: "FEET",
        daily_cost: 0,
        summary: "",
        current_operations: "",
        next_operations: ""
    };
    
    const initialWorkBreakdownStructure = {
        event: "",
        start_date: new Date().toISOString(),
        end_data: new Date().toISOString(),
        remarks: ""
    };
    
    const initialWellStrat = {
        strat_unit_id: "",
        depth_datum: "RT",
        top_depth: 0,
        bottom_depth: 0,
        depth_uoum: "FEET"
    };
    
    const [formData, setFormData] = useState({
        job: {
            field_id: "",
            contract_type: "COST-RECOVERY",
            afe_number: "",
            wpb_year: new Date().getFullYear(),
            plan_start: new Date().toISOString(),
            plan_end: new Date().toISOString(),
            plan_total_budget: 0,
            rig_name: "",
            rig_type: "JACK-UP",
            rig_horse_power: 0,
            job_activity: [initialJobActivity],
            work_breakdown_structure: [initialWorkBreakdownStructure],
            drilling_hazard: [
                {
                    hazard_type: "GAS KICK",
                    hazard_description: "",
                    severity: "LOW",
                    mitigation: "",
                    remark: ""
                }
            ],
            job_documents: [
                {
                    title: "",
                    creator_name: "",
                    create_date: new Date().toISOString(),
                    media_type: "EXTERNAL_HARDDISK",
                    document_type: "",
                    item_category: "",
                    item_sub_category: "",
                    digital_format: "",
                    original_file_name: "",
                    digital_size: 0,
                    digital_size_uom: "BYTE",
                    remark: ""
                }
            ],
            drilling_class: "EXPLORATION",
            planned_well: {
                uwi: "",
                field_id: "",
                well_name: "",
                alias_long_name: "",
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
                line_name: "",
                spud_date: new Date().toISOString(),
                final_drill_date: new Date().toISOString(),
                completion_date: new Date().toISOString(),
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
                remark: "",
                well_documents: [],
                well_casings: [],
                well_trajectories: [],
                well_ppfgs: [],
                well_logs: [],
                well_drilling_parameters: [],
                well_strat: [initialWellStrat]
            }
        }
    });
    
    const validateFormData = (data) => {
        const { job } = data;
        
        // Ensure job_activity is an array and remove any extra properties
        job.job_activity = Array.isArray(job.job_activity) 
            ? job.job_activity.map(activity => ({...initialJobActivity, ...activity}))
            : [initialJobActivity];
        
        // Ensure work_breakdown_structure is an array and remove any extra properties
        job.work_breakdown_structure = Array.isArray(job.work_breakdown_structure)
            ? job.work_breakdown_structure.map(wbs => ({...initialWorkBreakdownStructure, ...wbs}))
            : [initialWorkBreakdownStructure];
        
        // Ensure well_strat is an array and remove any extra properties
        job.planned_well.well_strat = Array.isArray(job.planned_well.well_strat)
            ? job.planned_well.well_strat.map(strat => ({...initialWellStrat, ...strat}))
            : [initialWellStrat];
        
        return data;
    };
    
    const handleSubmit = async () => {
        try {
            const validatedData = validateFormData({...formData});
            const response = await axios.post('http://127.0.0.1:8000/job/create/pengajuan/drilling', validatedData, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            });
            console.log('Data Berhasil Dimasukkan:', response.data);
            // Tambahkan logika untuk menangani respons sukses (misalnya, menampilkan pesan sukses, mereset form, dll.)
        } catch (error) {
            console.error('Error saat menambahkan sumur:', error);
            if (error.response) {
                console.error('Response data:', error.response.data);
                console.error('Response status:', error.response.status);
                console.error('Response headers:', error.response.headers);
            }
            // Tambahkan logika untuk menangani error (misalnya, menampilkan pesan error)
        }
    };


    const [handlePage, setHandlePage] = useState(1);

    const classTeknis = handlePage === 1 || handlePage === 2 || handlePage === 3 || handlePage === 4 || handlePage === 5 || handlePage === 6 || handlePage === 7 || handlePage === 8 ? 'bg-blue-500 text-white' : 'bg-gray-300';

    const classRencana = handlePage === 4 || handlePage === 5 || handlePage === 6 || handlePage === 7 || handlePage === 8 ? 'bg-blue-500 text-white' : 'bg-gray-300';
    const classManagement = handlePage === 7 || handlePage === 8 ? 'bg-blue-500 text-white' : 'bg-gray-300';
















    const years = Array.from({ length: 2024 - 2010 + 1 }, (_, i) => 2010 + i);

    return (
        <>

            <div className="flex w-full items-center gap-4 justify-center ">

                <div className="flex flex-col w-full gap-4">
                    <CardPageJob sendData={handleAllData} />
                    <FormDepthVSDays sendData={handleDataPageDepth} />
                    <CardPageSumur sendData={handleDataSumur} />
                    <FormWellStrat sendData={handleDataWellStrac} />
                    <FormPageWBS sendData={handleDataWBS} />
                    <FormPageDrilling sendData={handleDataDrilling} />
                    <FormPageCasing sendData={handleDataCasing} />
                    <Button variant="gradient" color="blue" onClick={handleSubmit} className='w-full'>
                        Submit
                    </Button>


                </div>




                {/* <Card variant='filled' className='w-full ' shadow={true}>

                    <CardBody>
                        <div className="flex flex-col gap-4">
                            <div className="flex flex-row gap-4">
                                <div className={` rounded-full px-3 py-2 flex items-center ${classTeknis}`}>
                                    <GlobeAsiaAustraliaIcon className='h-6 w-6' />
                                </div>
                                <div className="flex flex-col">
                                    <Typography color='black' variant='h6'>
                                        Teknis Umum
                                    </Typography>
                                    <Typography variant='small'>
                                        Informasi Teknis Umum
                                    </Typography>
                                </div>
                            </div>
                            <div className="flex flex-row gap-4">
                                <div className={` rounded-full px-3 py-2 flex items-center ${classRencana}`}>
                                    <Cog8ToothIcon className='h-6 w-6 ' color='' />
                                </div>
                                <div className="flex flex-col">
                                    <Typography color='black' variant='h6'>
                                        Rencana Teknis
                                    </Typography>
                                    <Typography variant='small'>
                                        Rencana Teknis Kegiatan
                                    </Typography>
                                </div>
                            </div>
                            <div className="flex flex-row gap-4">
                                <div className={` rounded-full px-3 py-2 flex items-center ${classManagement}`}>
                                    <UserGroupIcon className='h-6 w-6' />
                                </div>
                                <div className="flex flex-col">
                                    <Typography color='black' variant='h6'>
                                        Project Management
                                    </Typography>
                                    <Typography variant='small'>
                                        Management kegiatan
                                    </Typography>
                                </div>
                            </div>

                            <div className="flex justify-center mt-4">
                                <Button onClick={handleSubmit} color="green">
                                    Submit
                                </Button>
                            </div>
                            <div className="flex justify-center w-full mt-4">
                                <Button onClick={handleSubmit} color="green">
                                    Sebelum
                                </Button>
                                <Button onClick={handleSubmit} color="green">
                                    Selanjutnya
                                </Button>
                            </div>


                        </div>


                    </CardBody>
                </Card> */}
            </div>

        </>
    )
}

export default FormInput