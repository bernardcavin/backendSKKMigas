import React, { useState, useEffect } from 'react';
import { Card, CardBody, CardHeader, Input, Typography, Button, Select, Option } from '@material-tailwind/react';

const FormPageSchedule = ({ sendData }) => {
    // State to manage form data
    const [formData, setFormData] = useState({
        startDate: '',
        endDate: '',
        position: ''
    });

    // Handle input change
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));

        // Special handling for startDate to reset endDate if it is before startDate
        if (name === 'startDate') {
            if (value > formData.endDate) {
                setFormData(prevState => ({
                    ...prevState,
                    endDate: ''
                }));
            }
        }
    };

    // Handle change for Select component
    const handleSelectChange = (value) => {
        setFormData(prevState => ({
            ...prevState,
            position: value
        }));
    };

    
    
    useEffect(() => {
        sendData(formData);
    }, [formData]);

    return (
        <Card variant='filled' className='w-full' shadow={true}>
            <CardHeader floated={false} className="mb-0" shadow={false}>
                <div className="flex justify-between">
                    <Typography variant='h5' color='black'>
                        Schedule
                    </Typography>
                    <Button color='blue' className='h-[34px] flex justify-center items-center'>
                        Upload File
                    </Button>
                    <input type="file" placeholder="Casing" className='ml-4' hidden />
                </div>
                <hr className="my-2 border-gray-800" />
            </CardHeader>
            <CardBody className='flex-col flex gap-4'>
                <div className="flex flex-col">
                    <div className="flex flex-col mb-2">
                        <Typography color="black" className='font-bold'>
                            Posisi
                        </Typography>
                        <Select
                            label='Posisi'
                            name="position"
                            value={formData.position}
                            onChange={handleSelectChange}>
                            <Option value="VP Drilling/Katek Tambang">VP Drilling/Katek Tambang</Option>
                            <Option value="VP Padang">VP Padang</Option>
                        </Select>
                    </div>

                    <div className="flex flex-col mt-2">
                        <div>
                            <label className='font-bold text-black'>
                                Start Date
                                <Input
                                    type="date"
                                    name="startDate"
                                    value={formData.startDate}
                                    onChange={handleChange}
                                />
                            </label>
                            <br />
                            <label className='font-bold text-black'>
                                End Date
                                <Input
                                    type="date"
                                    name="endDate"
                                    value={formData.endDate}
                                    onChange={handleChange}
                                    min={formData.startDate}
                                />
                            </label>
                        </div>
                    </div>
                </div>
            </CardBody>
        </Card>
    );
}

export default FormPageSchedule;
