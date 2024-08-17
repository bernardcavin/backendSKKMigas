import React from 'react'
import { Card, CardBody, CardHeader, Input, Typography, Select, Option, Button } from '@material-tailwind/react'


const FormPagePersonel = () => {
    return (
        <Card variant='filled' className='w-full' shadow={true}>
            <CardHeader floated={false} className="mb-0" shadow={false}>
                <div className="flex  justify-between">
                    <Typography variant='h5' color='black' >
                        Personel
                    </Typography>
                    <Button color='blue' className='h-[34px] flex justify-center items-center'>
                        Upload File
                    </Button>
                    <input type="file" placeholder="Casing" className='ml-4' hidden />
                </div>
                <hr className="my-2 border-gray-800" />
            </CardHeader>
            <CardBody className='flex-col flex gap-4'>

                <div className="flex flex-col ">
                    <div className="flex flex-col mb-2">
                        <Typography color="black" className='font-bold'>
                            Posisi
                        </Typography>


                        <Select label='Posisi'>
                            <Option>VP Drilling/Katek Tambang</Option>
                            <Option>VP Padang</Option>
                        </Select>
                    </div>

                    <div className="flex flex-col mt-2">
                        <Typography color="black" className='font-bold'>
                            Nama
                        </Typography>
                        <Input type="number" placeholder="Nama" className='' min={0} />
                    </div>
                    <div className="flex flex-col mt-4">
                        <Typography color="black" className='font-bold'>
                            Sertifikasi
                        </Typography>
                        <Input type="number" placeholder="Sertifikasi" className='' min={0} />
                    </div>




                </div>

            </CardBody>
        </Card>
    )
}

export default FormPagePersonel