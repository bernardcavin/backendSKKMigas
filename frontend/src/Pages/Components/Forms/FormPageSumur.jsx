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
  const [wellClass, setWellClass] = useState([]);
  const [profileType, setProfileType] = useState([]);


  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setTypeWell(response.data.well_type);
      // console.log(response.data);
      // console.log(response.data);
      // Menyimpan data ke dalam state
    } catch (error) {
      console.error("Error fetching well types:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, [setTypeWell]);

  // useEffect(() => {
  //   sendData(formData);
  // }, [formData]);


  // Panggil saat file diproses
  const [formData, setFormData] = useState({


    uwi: "string",
    field_id: "string",
    well_name: "string",
    alias_long_name: "string",
    well_type: "OIL",
    well_class: "WILDCAT",
    well_status: "Active",
    profile_type: "DIRECTIONAL",
    environment_type: "MARINE",
    surface_longitude: 0,
    surface_latitude: 0,
    bottom_hole_longitude: 0,
    bottom_hole_latitude: 0,
    line_name: "string",
    spud_date: "2024-08-17T19:23:22.433Z",
    final_drill_date: "2024-08-17T19:23:22.433Z",
    completion_date: "2024-08-17T19:23:22.433Z",
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
    remark: "string",


  });

  console.log(formData);



  const statusOptions = ["Valid", "Proses", "Ditolak"];

  // Handle input change for text and select inputs
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSelectChangeTypeWell = (value) => {
    console.log("Selected Type Well:", value);
    setFormData((prevState) => ({
      ...prevState,
      type_well: value,
    }));
  };
  const handleSelectChangeStatusAFE = (value) => {
    console.log("Selected Type Well:", value);
    setFormData((prevState) => ({
      ...prevState,
      type_well: value,
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
              placeholder="uwi"
              name="uwi"
              value={formData.uwi}
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
              value={formData.field_id}
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
              name="well_name"
              value={formData.well_name}
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
              name="alias_long_name"
              value={formData.alias_long_name}
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
              checked={formData.pekerjaan === "Eksplorasi"}
            />
            <RadioButton
              label={"Eksploitasi"}
              nameLabel="pekerjaan"
              title="Eksploitasi"
              onChange={() => handleRadioChange("pekerjaan", "Eksploitasi")}
              checked={formData.pekerjaan === "Eksploitasi"}
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
              value={formData.well_status}
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
              value={formData.profile_type}
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
              value={formData.e}
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
              value={formData.spud_date}
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
              value={formData.total_cost_afe_approve}
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
                checked={formData.reEntry === "Ya"}
              />
              <RadioButton
                label={"Tidak"}
                nameLabel="reEntry"
                title="Tidak"
                onChange={() => handleRadioChange("reEntry", "Tidak")}
                checked={formData.reEntry === "Tidak"}
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
              Realisasi Mulai
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Realisasi Mulai"
              name="realisasi_mulai"
              value={formData.realisasi_mulai}
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
              value={formData.realisasi_selesai}
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
              value={formData.realisasi_total_budget}
              onChange={handleChange}
            />
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default CardPageSumur;
