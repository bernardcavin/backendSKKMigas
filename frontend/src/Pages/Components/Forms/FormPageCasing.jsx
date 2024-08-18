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

const Casing = () => {
  const [depthUom, setDepthUom] = useState([]);
  const [casingType, setCasingType] = useState([]);
  const [casingUOM, setCasingUOM] = useState([]);
  const [files, setFiles] = useState([]);

  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setDepthUom(response.data.depth_uom);
      setCasingType(response.data.casing_type);
      setCasingUOM(response.data.casing_uom);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, []);

  const [formData, setFormData] = useState({
    casing_type: "",
    grade: "",
    inside_diameter: 0,
    inside_diameter_ouom: "INCH",
    outside_diameter: 0,
    outside_diameter_ouom: "INCH",
    base_depth: 0,
    base_depth_ouom: "FEET",
  });

  console.table(formData);
  

  const handleChange = (event) => {
    const { name, value, type } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: type === "number" ? parseInt(value, 10) : value,
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
    console.log("Selected file:", file);
  };

  return (
    <Card variant="filled" className="w-full">
      <CardHeader floated={false} className="mb-2 shadow-none flex justify-between items-center">
        <Typography variant="h5" color="black">
          Casing
        </Typography>
        <div>
          <Button
            size="lg"
            color="black"
            onClick={() => document.getElementById('fileInput').click()}
          >
            Upload File
          </Button>
          <input
            id="fileInput"
            type="file"
            accept=".csv, .xlsx, .xls"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
      <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Casing Type
            </Typography>
            <Select
              label="Pilih Casing Type"
              name="casing_type"
              onChange={handleSelectChange("casing_type")}
            >
              {casingType.map((type, index) => (
                <Option key={index} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </div>

        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Grade
          </Typography>
          <Input
            type="text"
            placeholder="Grade"
            name="grade"
            value={formData.grade}
            onChange={handleChange}
          />
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Inside Diameter
            </Typography>
            <Input
              type="number"
              min={0}
              placeholder="Inside Diameter"
              name="inside_diameter"
              value={formData.inside_diameter}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Inside Diameter UOM
            </Typography>
            <Select
              label="Pilih Inside Diameter UOM"
              name="inside_diameter_ouom"
              onChange={handleSelectChange("inside_diameter_ouom")}
            >
              {casingUOM.map((type, index) => (
                <Option key={index} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Outside Diameter
            </Typography>
            <Input
              type="number"
              min={0}
              placeholder="Outside Diameter"
              name="outside_diameter"
              value={formData.outside_diameter}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Outside Diameter UOM
            </Typography>
            <Select
              label="Pilih Outside Diameter UOM"
              name="outside_diameter_ouom"
              onChange={handleSelectChange("outside_diameter_ouom")}
            >
              {casingUOM.map((type, index) => (
                <Option key={index} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Base Depth
            </Typography>
            <Input
              type="number"
              min={0}
              placeholder="Base Depth"
              name="base_depth"
              value={formData.base_depth}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Base Depth UOM
            </Typography>
            <Select
              label="Pilih Base Depth UOM"
              name="base_depth_ouom"
              onChange={handleSelectChange("base_depth_ouom")}
            >
              {depthUom.map((type, index) => (
                <Option key={index} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default Casing;
