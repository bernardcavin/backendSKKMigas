import React, { useState, useEffect } from 'react';
import { Card, CardBody, CardHeader, Input, Typography, Button, Select, Option, CardFooter } from '@material-tailwind/react';

const FormPageTrajectory = ({ sendData }) => {

    const TABLE_HEAD = ["Name", "Job", "Employed", "Action","Date"];

    const TABLE_ROWS = [
        {
            name: "John Michael",
            job: "Manager",
            date: "23/04/18",
        },
        {
            name: "Alexa Liras",
            job: "Developer",
            date: "23/04/18",
        },
        {
            name: "Laurent Perrier",
            job: "Executive",
            date: "19/09/17",
        },
        {
            name: "Michael Levi",
            job: "Developer",
            date: "24/12/08",
        },
        {
            name: "Richard Gran",
            job: "Manager",
            date: "04/10/21",
        },
    ];
    const [data, setData] = useState({
        tipe_bor: '',
        innerDiameter: '',
        outerDiameter: '',
        weight: '',
        grade: '',
        start_depth: '',
        end_depth: '',
    });




    // Handle input change
    const handleChange = (e) => {
        const { name, value } = e.target;
    
        // Convert the value to integer if it's a number field
        const newValue = name === 'innerDiameter' || name === 'outerDiameter' || name === 'weight' || name === 'grade' || name === 'start_depth' || name === 'end_depth'
            ? parseInt(value, 10) || 0 // parseInt(value, 10) converts to integer, || '' handles empty input
            : value;
    
        setData(prevState => ({
            ...prevState,
            [name]: newValue
        }));
    };
    


    const handleSelectChange = (value) => {
        setData(prevState => ({
            ...prevState,
            tipe_bor: value
        }));
    };

    useEffect(() => {

        sendData(data);

    }, [data]);

    return (
        <>
            <div className="flex flex-col w-full">
                <Card variant='filled' className='w-full mb-4' shadow={true}>
                    <CardHeader floated={false} className="mb-0" shadow={false}>
                        <div className="flex justify-between">
                            <Typography variant='h5' color='black'>
                                Trajectory
                            </Typography>
                            <input type="file" placeholder="Casing" className='ml-4' hidden />
                        </div>
                        <hr className="my-5 border-gray-800" />
                        <Button color='blue' className='h-[34px] mb-4 flex justify-center items-center'>
                            Upload File
                        </Button>
                    </CardHeader>
                </Card>
                <Card variant='filled' className='w-full' shadow={true}>
                    <CardHeader floated={false} className="mb-0" shadow={false}>
                        <div className="flex justify-between">
                            <Typography variant='h5' color='black'>
                                Casing
                            </Typography>
                            <Button color='blue' className='h-[34px] flex justify-center items-center' >
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
                                    Tipe
                                </Typography>
                                <Select label='Select Tipe' onChange={handleSelectChange}>
                                    <Option value="conductor">Conductor</Option>
                                    <Option value="semi-conductor">Semi Conductor</Option>
                                </Select>
                            </div>

                            <div className="flex flex-col mt-2">
                                <Typography color="black" className='font-bold'>
                                    Inner Diameter
                                </Typography>
                                <Input
                                    type="number"
                                    name="innerDiameter"
                                    placeholder="Inner Diameter"
                                    className=''
                                    min={0}
                                    value={parseInt(data.innerDiameter)}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="flex flex-col mt-4">
                                <Typography color="black" className='font-bold'>
                                    Outer Diameter
                                </Typography>
                                <Input
                                    type="number"
                                    name="outerDiameter"
                                    placeholder="Outer Diameter"
                                    className=''
                                    min={0}
                                    value={data.outerDiameter}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="flex flex-col mt-2">
                                <Typography color="black" className='font-bold mt-2'>
                                    Weight
                                </Typography>
                                <Input
                                    type="number"
                                    name="weight"
                                    placeholder="Weight"
                                    className=''
                                    min={0}
                                    value={data.weight}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="flex flex-col mt-2">
                                <Typography color="black" className='font-bold mt-2'>
                                    Grade
                                </Typography>
                                <Input
                                    type="number"
                                    name="grade"
                                    placeholder="Grade"
                                    className=''
                                    min={0}
                                    value={data.grade}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="flex flex-col mt-2">
                                <Typography color="black" className='font-bold mt-2'>
                                    Start Depth
                                </Typography>
                                <Input
                                    type="number"
                                    name="start_depth"
                                    placeholder="Start Depth"
                                    className=''
                                    min={0}
                                    value={data.start_depth}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="flex flex-col mt-2">
                                <Typography color="black" className='font-bold mt-2'>
                                    End Depth
                                </Typography>
                                <Input
                                    type="number"
                                    name="end_depth"
                                    placeholder="End Depth"
                                    className=''
                                    min={0}
                                    value={data.end_depth}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>
                    </CardBody>
                    <CardFooter>
                        <Card className="h-36 w-full overflow-y-scroll">
                            <table className="w-full min-w-max table-auto text-left">
                                <thead>
                                    <tr>
                                        {TABLE_HEAD.map((head) => (
                                            <th key={head} className="border-b border-blue-gray-100 bg-blue-gray-50 p-4">
                                                <Typography
                                                    variant="small"
                                                    color="blue-gray"
                                                    className="font-normal leading-none opacity-70"
                                                >
                                                    {head}
                                                </Typography>
                                            </th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {TABLE_ROWS.map(({ name, job, date }, index) => {
                                        const isLast = index === TABLE_ROWS.length - 1;
                                        const classes = isLast ? "p-4" : "p-4 border-b border-blue-gray-50";

                                        return (
                                            <tr key={name}>
                                                <td className={classes}>
                                                    <Typography variant="small" color="blue-gray" className="font-normal">
                                                        {name}
                                                    </Typography>
                                                </td>
                                                <td className={`${classes} bg-blue-gray-50/50`}>
                                                    <Typography variant="small" color="blue-gray" className="font-normal">
                                                        {job}
                                                    </Typography>
                                                </td>
                                                <td className={classes}>
                                                    <Typography variant="small" color="blue-gray" className="font-normal">
                                                        {date}
                                                    </Typography>
                                                </td>
                                                <td className={`${classes} bg-blue-gray-50/50`}>
                                                    <Typography as="a" href="#" variant="small" color="blue-gray" className="font-medium">
                                                        Edit
                                                    </Typography>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </Card>

                    </CardFooter>
                </Card>
            </div>
        </>
    );
}

export default FormPageTrajectory;
