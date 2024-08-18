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


    const [date,setHandleDate] = useState('')


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
            [name]: value,
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
                    JOB
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
                            label={"Gross Split"}
                            nameLabel="tipe_kontrak"
                            title="Gross Split"
                            onChange={() => handleRadioChange("tipe_kontrak", "Gross Split")}
                            checked={formData.tipe_kontrak === "Gross Split"}
                        />
                        <RadioButton
                            label={"Cost Recovery"}
                            nameLabel="tipe_kontrak"
                            title="Cost Recovery"
                            onChange={() =>
                                handleRadioChange("tipe_kontrak", "Cost Recovery")
                            }
                            checked={formData.tipe_kontrak === "Cost Recovery"}
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
                            name="no_afe"
                            value={formData.no_afe}
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
                            Total Cost AFE Approve
                        </Typography>
                        <Input
                            type="number"
                            placeholder="Masukkan Total Cost AFE Approve"
                            name="total_cost_afe_approve"
                            value={formData.total_cost_afe_approve}
                            onChange={handleChange}

                        />
                    </div>
                </div>

                {/* Rencana Fields */}
                <div className="flex flex-row w-full gap-4">
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rencana Mulai Tajak
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan Rencana Mulai Tajak"
                            name="rencana_mulai_tajak"
                            value={formData.rencana_mulai_tajak}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rencana Selesai Operasi
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan Rencana Selesai Operasi"
                            name="rencana_selesai_operasi"
                            value={formData.rencana_selesai_operasi}
                            onChange={handleChange}
                        />
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
                            name="realisasi_mulai"
                            value={formData.realisasi_mulai}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rig Type
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan Rig Type"
                            name="realisasi_selesai"
                            value={formData.realisasi_selesai}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="flex flex-col w-full">
                        <Typography color="black" className="font-bold">
                            Rig HP
                        </Typography>
                        <Input
                            type="text"
                            placeholder="Masukkan Rig HP"
                            name="realisasi_total_budget"
                            value={formData.realisasi_total_budget}
                            onChange={handleChange}
                        />
                    </div>
                </div>
            </CardBody>
        </Card>
    );
};

export default CardPageJob;
