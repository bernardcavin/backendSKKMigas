import React, { useState, useEffect } from "react";
import {
    Card,
    CardBody,
    CardHeader,
    Input,
    Typography,
    Select,
    Option,
} from "@material-tailwind/react";
import RadioButton from "../ChildComponets/RadioButton";
import axios from "axios";

const CardPageJob = ({ sendData }) => {


    const [date, setHandleDate] = useState('')
    const [rigType, setRigType] = useState([])

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/utils/enum/all").then((response) => {
            setRigType(response.data.rig_type);

        })
    }, []);

    //   const getAllData = async () => {
    //     try {
    //       const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
    //       setTypeWell(response.data.well_type);
    //       setWellClass(response.data.well_class);
    //       setEnvironmentType(response.data.environment);



    //       // console.log(response.data);
    //       // console.log(response.data);
    //       // Menyimpan data ke dalam state
    //     } catch (error) {
    //       console.error("Error fetching well types:", error);
    //     }
    //   };

    //   useEffect(() => {
    //     getAllData();
    //   }, [setTypeWell]);

    // useEffect(() => {
    //   sendData(formData);
    // }, [formData]);


    // Panggil saat file diproses
    const [formData, setFormData] = useState({
        field_id: "String", // Kosongkan jika tidak ada nilai yang pasti
        contract_type: "COST-RECOVERY",
        afe_number: "String", // Kosongkan jika tidak ada nilai yang pasti
        wpb_year: 0,
        plan_start: "2024-08-18T14:51:19.093Z",
        plan_end: "2024-08-18T14:51:19.093Z",
        plan_total_budget: 0,
        rig_name: "String", // Kosongkan jika tidak ada nilai yang pasti
        rig_type: "JACK-UP",
        rig_horse_power: 0
    });

    const statusOptions = ["Valid", "Proses", "Ditolak"];
    const wellStatus = ["ACTIVE", "PROSES", "DEACTIVATE"];

    const handleSelectChange = (name) => (value) => {
        setFormData((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleChange = (event) => {
        const { name, value, type } = event.target;



        setFormData((prevState) => ({
            ...prevState,
            [name]: type === "number" ? parseInt(value) : value,
        }));
    };

    // Handle change for radio buttons
    const handleRadioChange = (name, value) => {
        setFormData((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    useEffect(() => {
        // Call sendData whenever formData changes
        sendData(formData);


    }, [formData]);

    return (
        <Card variant="filled" className="w-full" shadow={true}>
            <CardHeader floated={false} className="mb-0" shadow={false}>
                <Typography variant="h5" color="black">
                    Job
                </Typography>
                <hr className="my-2 border-gray-800" />
            </CardHeader>
            <CardBody className="flex-col flex gap-4">
                <div className="flex flex-col">
                    <Typography color="black" className="font-bold">
                        Pekerjaan
                    </Typography>
                    <div className="flex flex-row">
                        <RadioButton
                            label={"EKSPLORASI"}
                            nameLabel="drilling_class"
                            title="EKSPLORASI"
                            onChange={() => handleRadioChange("drilling_class", "EKSPLORASI")}
                            checked={formData.drilling_class === "EKSPLORASI"}
                        />
                        <RadioButton
                            label={"EKSPLOTASI"}
                            nameLabel="drilling_class"
                            title="EKSPLOTASI"
                            onChange={() => handleRadioChange("drilling_class", "EKSPLOTASI")}
                            checked={formData.drilling_class === "EKSPLOTASI"}
                        />
                    </div>
                </div>

                <div className="flex flex-col mt-4">
                    <Typography color="black" className="font-bold">
                        Tipe Kontrak
                    </Typography>
                    <div className="flex flex-row">
                        <RadioButton
                            label={"GROSS-SPLIT"}
                            nameLabel="contract_type"
                            title="GROSS-SPLIT"
                            onChange={() => handleRadioChange("contract_type", "GROSS-SPLIT")}
                            checked={formData.contract_type === "GROSS-SPLIT"}
                        />
                        <RadioButton
                            label={"COST-RECOVERY"}
                            nameLabel="contract_type"
                            title="COST-RECOVERY"
                            onChange={() =>
                                handleRadioChange("contract_type", "COST-RECOVERY")
                            }
                            checked={formData.contract_type === "COST-RECOVERY"}
                        />
                    </div>
                </div>
                <div className="flex flex-col w-full">
                    <Typography color="black" className="font-bold">
                        Field
                    </Typography>
                    <Input
                        type="text"
                        placeholder="Field"
                        name="field"
                        value={formData.field_id}
                        onChange={handleChange}
                    />
                </div>
                {/* Dimasukkan Ke Dalam FORM JOB */}
                <div className="flex flex-row w-full gap-4">
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            No AFE
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan No AFE"
                            name="afe_number"
                            value={formData.afe_number}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Status AFE
                        </Typography>
                        <Select
                            label="Pilih Status AFE"
                            name="status_afe"
                            value={formData.status_afe}
                            onChange={handleSelectChange("status_afe")}
                            disabled={true}
                        >
                            {statusOptions.map((option) => (
                                <Option key={option} value={option}>
                                    {option}
                                </Option>
                            ))}
                        </Select>
                    </div>
                </div>

                <div className="flex flex-row w-full gap-4">
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Tahun WPB
                        </Typography>
                        <Input
                            type="number"
                            placeholder="Masukkan Tahun WPB"
                            name="wpb_year"
                            value={formData.wpb_year}
                            onChange={handleChange}

                        />
                    </div>
                </div>

                {/* Rencana Fields */}
                <div className="flex flex-row w-full gap-4">
                    <div className="flex flex-col w-full">

                        <div>
                            <label className='font-bold text-black'>
                                Rencana Mulai Tajak
                                <Input
                                    type="date"
                                    name="plan_start"
                                    value={formData.plan_start}
                                    onChange={handleChange}
                                />
                            </label>
                            <br />

                        </div>
                    </div>
                    <div className="flex flex-col w-full">
                        <label className='font-bold text-black'>
                            Rencana Selesai Tajak
                            <Input
                                type="date"
                                name="endDate"
                                value={formData.plan_end}
                                onChange={handleChange}
                                min={formData.plan_start}
                            />
                        </label>
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rencana Total Budget
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan Rencana Total Budget"
                            name="rencana_total_budget"
                            value={formData.rencana_total_budget}
                            onChange={handleChange}
                            disabled={true}
                        />
                    </div>
                </div>

                {/* Realisasi Fields */}
                <div className="flex flex-row w-full gap-4">
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rig Name
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan Rig Name"
                            name="rig_name"
                            value={formData.rig_name}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rig Type
                        </Typography>
                        <Select
                            label="Pilih Rig Type"
                            name="rig_type"
                            onChange={handleSelectChange("rig_type")}
                        >
                            {rigType.map((option) => (
                                <Option key={option} value={option}>
                                    {option}
                                </Option>
                            ))}
                        </Select>
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rig HP
                        </Typography>
                        <Input
                            type="number"
                            placeholder="Masukkan Rig HP"
                            name="rig_horse_power"
                            value={formData.rig_horse_power}
                            onChange={handleChange}
                        />
                    </div>
                </div>
            </CardBody>
        </Card>
    );
};

export default CardPageJob;
