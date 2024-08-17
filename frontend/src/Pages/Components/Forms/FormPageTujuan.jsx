import { useState } from "react"

const FormPageTujuan = ({sendData}) => {

    const handleValueDate = (e) => {
        const { name, value } = e.target
        setData(prevState => ({
            ...prevState,
            [name]: value
        }))
    }

    
    
    const [data,setData] =  useState({

    })
    
    return (
        <Card variant='filled' className='w-full' shadow={true}>
            <CardHeader floated={false} className="mb-0" shadow={false}>
                <Typography variant='h5' color='black' >
                    Tujuan
                </Typography>
                <hr className="my-2 border-gray-800" />
            </CardHeader>
            <CardBody className='flex-col flex gap-4'>

                <div className="flex flex-col">
                    <Typography color="black" className='font-bold'>
                        Tujuan
                    </Typography>
                    <div className="flex flex-row">
                        {pekerjaan === 'eksplorasi' && <RadioButton
                            label={'Wildcat'}
                            nameLabel="Tujuan"
                            title="Wildcat"
                            onChange={handleTujuanChange}
                            checked={TujuanValue === 'Wildcat'}
                        />}
                        {pekerjaan === 'eksplorasi' && <RadioButton
                            label={'Desalinasi'}
                            nameLabel="Tujuan"
                            title="Desalinasi"
                            onChange={handleTujuanChange}
                            checked={TujuanValue === 'Desalinasi'}
                        />}
                        {pekerjaan === 'eksploitasi' && <RadioButton
                            label={'Infield'}
                            nameLabel="Tujuan"
                            title="Infield"
                            onChange={handleTujuanChange}
                            checked={TujuanValue === 'Infield'}
                        />}
                        {pekerjaan === 'eksploitasi' && <RadioButton
                            label={'Injection'}
                            nameLabel="Tujuan"
                            title="Injection"
                            onChange={handleTujuanChange}
                            checked={TujuanValue === 'Injection'}
                        />}
                        {pekerjaan === 'eksploitasi' && <RadioButton
                            label={'Stepover'}
                            nameLabel="Tujuan"
                            title="Stepover"
                            onChange={handleTujuanChange}
                            checked={TujuanValue === 'Stepover'}
                        />}


                    </div>
                    <div className="flex flex-col">
                        <Typography color="black" className='font-bold'>
                            Recentry
                        </Typography>
                        <div className="flex flex-row">
                            <RadioButton
                                label={'Ya'}
                                nameLabel="Recentry"
                                title="Ya"
                                onChange={handleRecentryChange}
                                checked={Recentry === 'Ya'}
                            />
                            <RadioButton
                                label={'Tidak'}
                                nameLabel="Recentry"
                                title="Tidak"
                                onChange={handleRecentryChange}
                                checked={Recentry === 'Tidak'}
                            />
                        </div>
                    </div>
                    <div className="flex flex-col">
                        <DateRangePicker />
                    </div>
                    <Typography color="black" className='font-bold mt-2'>
                        Tipe Sumur
                    </Typography>
                    <div className="flex flex-row">
                        <RadioButton
                            label={'Vertical'}
                            nameLabel="Tipe Sumur"
                            title="Vertical"
                            onChange={handleTipeSumurChange}
                            checked={TipeSumur === 'Vertical'}
                        />
                        <RadioButton
                            label={'Directional'}
                            nameLabel="Tipe Sumur"
                            title="Directional"
                            onChange={handleTipeSumurChange}
                            checked={TipeSumur === 'Directional'}
                        />
                        <RadioButton
                            label={'Horizontal'}
                            nameLabel="Tipe Sumur"
                            title="Horizontal"
                            onChange={handleTipeSumurChange}
                            checked={TipeSumur === 'Horizontal'}
                        />


                    </div>
                    <div className="flex flex-col">
                        <Typography color='black' className='font-bold '>
                            Wilayah Kerja

                        </Typography>
                        <Input type="number" placeholder="Wilayah Kerja" className='' />
                    </div>
                    <div className="flex flex-col mt-4">
                        <Typography color='black' className='font-bold '>
                            Lapangan

                        </Typography>
                        <Input type="number" placeholder="Lapangan" className='' />
                    </div>



                </div>

            </CardBody>

            <CardFooter className='flex justify-between'>
                <Button className='' color='blue' onClick={() => setHandlePage(3)}>
                    Prev
                </Button>
                <Button className='' color='blue' onClick={() => setHandlePage(5)}>
                    Next
                </Button>
            </CardFooter>
        </Card>
    )
}

export default FormPageTujuan