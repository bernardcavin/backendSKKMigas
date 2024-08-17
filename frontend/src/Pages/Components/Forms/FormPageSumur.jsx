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

const CardPageSumur = ({ sendData }) => {
  const [typeWell, setTypeWell] = useState([]);

  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setTypeWell(response.data.well_type);
      console.log(response.data);
      // Menyimpan data ke dalam state
    } catch (error) {
      console.error("Error fetching well types:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, []);

  // Panggil saat file diproses
  const [formData, setFormData] = useState({
    job: {
      name: "",
      pekerjaan: "",
      tipe_kontrak: "",
      no_afe: "",
      well_status: "",
      profile_type: "",
      environtment_type: "",
      spud_date: "",
      total_cost_afe_approve: "",
      rencana_mulai_tajak: "",
      rencana_selesai_operasi: "",
      rencana_total_budget: "",
      realisasi_mulai: "",
      realisasi_selesai: "",
      realisasi_total_budget: "",
    },
  });

  const typeWellOptions = [
    "Wildcat",
    "Deliniasi",
    "Infill",
    "Produser",
    "Stepout",
  ];
  const statusOptions = ["Valid", "Proses", "Ditolak"];

  // Handle input change for text and select inputs
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      job: {
        ...prevState.job,
        [name]: value,
      },
    }));
  };

  const handleSelectChangeTypeWell = (value) => {
    console.log("Selected Type Well:", value);
    setFormData((prevState) => ({
      ...prevState,
      job: {
        ...prevState.job,
        type_well: value,
      },
    }));
  };

  // Handle change for radio buttons
  const handleRadioChange = (name, value) => {
    setFormData((prevState) => ({
      ...prevState,
      job: {
        ...prevState.job,
        [name]: value,
      },
    }));
  };

  useEffect(() => {
    // Call sendData whenever formData changes
    sendData(formData);
    console.log(formData);
    
  }, [formData]);

  return (
    <Card variant="filled" className="w-full" shadow={true}>
      <CardHeader floated={false} className="mb-0" shadow={false}>
        <Typography variant="h5" color="black">
          Sumur
        </Typography>
        <hr className="my-2 border-gray-800" />
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              UWI
            </Typography>
            <Input
              type="text"
              placeholder="UWI"
              name="UWI"
              value={formData.job.UWI}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Field
            </Typography>
            <Input
              type="text"
              placeholder="Field"
              name="field"
              value={formData.job.field}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Nama Sumur
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Nama Sumur"
              name="nama_sumur"
              value={formData.job.nama_sumur}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Nama Lengkap Sumur
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Nama Lengkap Sumur"
              name="nama_lengkap_sumur"
              value={formData.job.nama_lengkap_sumur}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Pekerjaan
          </Typography>
          <div className="flex flex-row">
            <RadioButton
              label={"Eksplorasi"}
              nameLabel="pekerjaan"
              title="Eksplorasi"
              onChange={() => handleRadioChange("pekerjaan", "Eksplorasi")}
              checked={formData.job.pekerjaan === "Eksplorasi"}
            />
            <RadioButton
              label={"Eksploitasi"}
              nameLabel="pekerjaan"
              title="Eksploitasi"
              onChange={() => handleRadioChange("pekerjaan", "Eksploitasi")}
              checked={formData.job.pekerjaan === "Eksploitasi"}
            />
          </div>
        </div>
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Type Well
          </Typography>
          <Select
            label="Pilih Type Well"
            name="type_well"
            value={formData.type_well}
            onChange={handleSelectChangeTypeWell}
          >
            {typeWell.map((typeWell, index) => (
              <Option key={index} value={typeWell}>
                {typeWell}
              </Option>
            ))}
          </Select>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Well Status
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Well Status"
              name="well_status"
              value={formData.job.well_status}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Profile Type
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Profile Type"
              name="profile_type"
              value={formData.job.profile_type}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Environment type
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Environment Type"
              name="environment_type"
              value={formData.job.environment_type}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Spud Date
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Spud Date"
              name="spud_date"
              value={formData.job.spud_date}
              onChange={handleChange}
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
              checked={formData.job.tipe_kontrak === "Gross Split"}
            />
            <RadioButton
              label={"Cost Recovery"}
              nameLabel="tipe_kontrak"
              title="Cost Recovery"
              onChange={() =>
                handleRadioChange("tipe_kontrak", "Cost Recovery")
              }
              checked={formData.job.tipe_kontrak === "Cost Recovery"}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              No AFE
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan No AFE"
              name="no_afe"
              value={formData.job.no_afe}
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
              value={formData.job.status_afe}
              onChange={handleChange}
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
              type="text"
              placeholder="Masukkan Total Cost AFE Approve"
              name="total_cost_afe_approve"
              value={formData.job.total_cost_afe_approve}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Re-entry
            </Typography>
            <div className="flex flex-row">
              <RadioButton
                label={"Ya"}
                nameLabel="reEntry"
                title="Ya"
                onChange={() => handleRadioChange("reEntry", "Ya")}
                checked={formData.job.reEntry === "Ya"}
              />
              <RadioButton
                label={"Tidak"}
                nameLabel="reEntry"
                title="Tidak"
                onChange={() => handleRadioChange("reEntry", "Tidak")}
                checked={formData.job.reEntry === "Tidak"}
              />
            </div>
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
              value={formData.job.rencana_mulai_tajak}
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
              value={formData.job.rencana_selesai_operasi}
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
              value={formData.job.rencana_total_budget}
              onChange={handleChange}
            />
          </div>
        </div>

        {/* Realisasi Fields */}
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Realisasi Mulai
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Realisasi Mulai"
              name="realisasi_mulai"
              value={formData.job.realisasi_mulai}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Realisasi Selesai
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Realisasi Selesai"
              name="realisasi_selesai"
              value={formData.job.realisasi_selesai}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Realisasi Total Budget
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Realisasi Total Budget"
              name="realisasi_total_budget"
              value={formData.job.realisasi_total_budget}
              onChange={handleChange}
            />
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default CardPageSumur;
