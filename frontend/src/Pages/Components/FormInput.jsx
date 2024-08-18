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
                ...prevState.job,planned_well: {
                    ...prevState.job.planned_well, well_strat:{
                        ...prevState.job.planned_well.well_strat, ...data
                    }
                }
            }
            
        }));

    };
    const handleDataPageDepth = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job,job_activity: {
                    ...prevState.job.job_activity, ...data
                }
            }
          
        }));

    };
    const handleDataWBS = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job,work_breakdown_structure: {
                    ...prevState.job.work_breakdown_structure, ...data
                }
            }
          
        }));

    };
    const handleDataDrilling = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job,drilling_hazard: {
                    ...prevState.job.drilling_hazard, ...data
                }
            }
          
        }));

    };
    const handleDataCasing = (data) => {
        setFormData(prevState => ({
            ...prevState, job: {
                ...prevState.job,planned_well: {
                    ...prevState.job.planned_well, well_casing:{
                        ...prevState.job.planned_well.well_casing, ...data
                    }
                }
            }
          
        }));

    };




    const [formData, setFormData] = useState({
        job: {
            planned_well: {
                
            }
        }
    });
    console.log(formData);

    // console.log(formData);




    const handleSubmit = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/wells', formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",

                }
            });
            console.log('Sumur berhasil ditambahkan:', response.data);
            // Tambahkan logika untuk menangani respons sukses (misalnya, menampilkan pesan sukses, mereset form, dll.)
        } catch (error) {
            console.error('Error saat menambahkan sumur:', error);
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
                    {/* <FormWellStrat/> */}
                    {/* <FormPageWBS/> */}
                    {/* <CardPageSumur sendData={handleAllData} /> */}
                    {/* <FormHSEPlan sendData={handleAllData}/> */}
                    {/* <FormPageLainnya /> */}
                    {/* <FormPagePersonel /> */}
                    {/* <FormPageSchedule sendData={handleAllData} /> */}
                    {/* <FormPageTrajectory sendData={handleAllData} /> */}
                    <FormDepthVSDays sendData={handleAllData} />
                    {/* <FormPageCasing sendData={handleAllData} />  */}
                    {/* <CardPageSumur sendData={handleAllData} /> */}
                    {/* <FormHSEPlan /> */}
                    {/* <FormPageLainnya /> */}
                    {/* <FormPagePersonel /> */}
                    {/* <FormPageSchedule sendData={handleAllData} /> */}
                    {/* <FormPageTrajectory sendData={handleAllData} />  */}
                    
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