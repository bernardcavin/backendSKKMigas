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

const CardPageSumur = ({ sendData }) => {
    const [formData, setFormData] = useState({
        job:{
            name: '',
            pekerjaan: '',
            tipe_kontrak: '',
            no_afe: '',
            tahun_wpnb: '',
            tujuan: ''
        }
    });

  // Handle input change for text and select inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
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
          Sumur
        </Typography>
        <hr className="my-2 border-gray-800" />
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Nama Sumur
          </Typography>
          <Input
            type="text"
            name="nama_sumur"
            value={formData.nama_sumur}
            onChange={handleChange}
            placeholder="Masukkan Nama Sumur"
          />
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
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            No AFE
          </Typography>
          <Input
            type="text"
            name="no_afe"
            value={formData.no_afe}
            onChange={handleChange}
            variant="outlined"
            placeholder="Masukkan No AFE"
          />
        </div>
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Tahun WP&B
          </Typography>
          <Select
            label="Pilih Tahun WP&B"
            name="tahun_wpnb"
            value={formData.tahun_wpnb}
            onChange={handleChange}
          >
            {Array.from({ length: 2024 - 2010 + 1 }, (_, i) => 2010 + i).map(
              (year) => (
                <Option key={year} value={year.toString()}>
                  {year}
                </Option>
              )
            )}
          </Select>
        </div>
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Tujuan
          </Typography>
          <Input
            type="text"
            name="tujuan"
            value={formData.tujuan}
            onChange={handleChange}
            variant="outlined"
            placeholder="Masukkan Tujuan"
          />
        </div>
      </CardBody>
    </Card>
  );
};

export default CardPageSumur;
