const PageDepthvsDays = () => {
    return (
        <Card variant='filled' className='w-full' shadow={true}>
            <CardHeader floated={false} className="mb-0" shadow={false}>
                <div className="flex  justify-between">
                    <Typography variant='h5' color='black' >
                        Depth Vs Days
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
                            Kegiatan
                        </Typography>

                        <Input type="text" placeholder="Kegiatan" className='' />
                    </div>

                    <div className="flex flex-col mt-2">
                        <Typography color="black" className='font-bold'>
                            Days
                        </Typography>
                        <Input type="number" placeholder="Days" className='' min={0} />
                    </div>
                    <div className="flex flex-col mt-4">
                        <Typography color="black" className='font-bold'>
                            Start Depth
                        </Typography>
                        <Input type="number" placeholder="Start Depth" className='' min={0} />
                    </div>
                    <div className="flex flex-col mt-2">
                        <Typography color="black" className='font-bold mt-2'>
                            End Depth
                        </Typography>
                        <Input type="number" placeholder="End Depth" className='' min={0} />
                    </div>



                </div>

            </CardBody>

            
        </Card>
    )
}


export default PageDepthvsDays