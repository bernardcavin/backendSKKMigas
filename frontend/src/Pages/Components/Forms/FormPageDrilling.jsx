import React, { useState } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Typography,
  Select,
  Option,
  Button,
} from "@material-tailwind/react";

const FormHSEPlan = ({ sendData }) => {
  const [data, setData] = useState({
    descPekerjaan: "",
    potensiBahaya: "",
    upayaPengandilan: "",
  });

  

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSelectChange = (value) => {
    setData((prevState) => ({
      ...prevState,
      descPekerjaan: value,
    }));
  };

  return (
    <Card variant="filled" className="w-full" shadow={true}>
      <CardHeader floated={false} className="mb-0" shadow={false}>
        <div className="flex justify-between">
          <Typography variant="h5" color="black">
            Drilling Hazard
          </Typography>
          <Button
            color="blue"
            className="h-[34px] flex justify-center items-center"
          >
            Upload File
          </Button>
          <input type="file" placeholder="Casing" className="ml-4" hidden />
        </div>
        <hr className="my-2 border-gray-800" />
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-col">
          <div className="flex flex-col mb-2">
            <Typography color="black" className="font-bold">
              Deskripsi Pekerjaan
            </Typography>
            <Select label="Posisi" onChange={handleSelectChange}>
              <Option value="VP Drilling/Katek Tambang">
                VP Drilling/Katek Tambang
              </Option>
              <Option value="VP Padang">VP Padang</Option>
            </Select>
          </div>

          <div className="flex flex-col mt-2">
            <Typography color="black" className="font-bold">
              Potensi Bahaya
            </Typography>
            <Input
              type="text"
              placeholder="Potensi Bahaya"
              name="potensiBahaya"
              value={data.potensiBahaya}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col mt-4">
            <Typography color="black" className="font-bold">
              Upaya Pengandilan
            </Typography>
            <Input
              type="text"
              placeholder="Upaya Pengandilan"
              name="upayaPengandilan"
              value={data.upayaPengandilan}
              onChange={handleChange}
            />
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default FormHSEPlan;
