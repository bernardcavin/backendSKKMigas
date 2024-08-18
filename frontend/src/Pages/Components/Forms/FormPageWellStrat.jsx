import React, { useState, useEffect } from "react";
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
import axios from "axios";

const WellStrat = ({ sendData }) => {
  const [depthUom, setDepthUom] = useState([]);
  const [depthDatum, setDepthDatum] = useState([]);
  const [files, setFiles] = useState([]);  // Ini adalah state untuk file yang di-upload

  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setDepthUom(response.data.depth_uom);
      setDepthDatum(response.data.depth_datum);
    } catch (error) {
      console.error("Error fetching depth data:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, [1]);



  const [formData, setFormData] = useState({
    strat_unit_id: "",
    depth_datum: "RT",
    top_depth: 0,
    bottom_depth: 0,
    depth_uoum: "FEET",
  });
  useEffect(() => {
    sendData(formData);
  }, [formData]);

  // console.table(formData);


  const handleChange = (event) => {
    const { name, value, type } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: type === "number" ? parseInt(value) : value,
    }));
  };

  const handleSelectChange = (name) => (value) => {
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFiles([file]);  // Simpan file yang di-upload ke state files
      console.log("File selected:", file.name);
      // Anda dapat menambahkan logika tambahan di sini untuk meng-upload file
    }
  };

  return (
    <Card variant="filled" className="w-full">
      <CardHeader floated={false} className="mb-4 shadow-none flex justify-between items-center">
        <Typography variant="h5" color="black">
          Well Stratification
        </Typography>
        <Button size="lg" color="black" onClick={() => document.getElementById('fileInput').click()}>
          Upload File
        </Button>
        <input
          id="fileInput"
          type="file"
          accept=".csv, .xlsx, .xls"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Strat Unit ID
          </Typography>
          <Input
            type="text"
            placeholder="Strat Unit ID"
            name="strat_unit_id"
            value={formData.strat_unit_id}
            onChange={handleChange}
          />
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Depth Datum
            </Typography>
            <Select
              label="Pilih Depth Datum"
              name="depth_datum"
              onChange={handleSelectChange("depth_datum")}
            >
              {depthDatum.map((datum, index) => (
                <Option key={index} value={datum}>
                  {datum}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Top Depth
            </Typography>
            <Input
              type="number"
              placeholder="Top Depth"
              name="top_depth"
              value={formData.top_depth}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Bottom Depth
            </Typography>
            <Input
              type="number"
              placeholder="Bottom Depth"
              name="bottom_depth"
              value={formData.bottom_depth}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Depth UOM
            </Typography>
            <Select
              label="Pilih Depth UOM"
              name="depth_uoum"
              onChange={handleSelectChange("depth_uoum")}
            >
              {depthUom.map((uom, index) => (
                <Option key={index} value={uom}>
                  {uom}
                </Option>
              ))}
            </Select>
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default WellStrat;
