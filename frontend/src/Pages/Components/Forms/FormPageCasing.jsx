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
  const [casingTypes, setCasingTypes] = useState([]);

  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setCasingTypes(response.data.casing_type);
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching casing types:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, []);

  const [formData, setFormData] = useState({
    casing_type: "",
    inner_diameter: "",
    outer_diameter: "",
    weight: "",
    grade: "",
    start_depth: "",
    end_depth: "",
  });
    
    console.log(formData);
    

  // Handle input change for text and select inputs
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSelectChange = (value) => {
    console.log("Selected Casing Type:", value);
    setFormData((prevState) => ({
      ...prevState,
      casing_type: value,
    }));
  };

  useEffect(() => {
    // This effect could be used to send data or any other side effect based on formData changes
    console.log(formData);
  }, [formData]);

  return (
    <Card variant="filled" className="w-full">
      <CardHeader floated={false} className="mb-2 shadow-none">
        <Typography variant="h5" color="black">
          Casing
        </Typography>
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Tipe
          </Typography>
          <Select
            label="Pilih Tipe Casing"
            name="casing_type"
            value={formData.casing_type}
            onChange={handleSelectChange}
          >
            {casingTypes.map((type, index) => (
              <Option key={index} value={type}>
                {type}
              </Option>
            ))}
          </Select>
        </div>
        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Upload File
          </Typography>
          <Input type="file" accept=".csv, .xlsx, .xls" className="w-full" />
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Inner Diameter
            </Typography>
            <Input
              type="text"
              placeholder="Inner Diameter"
              name="inner_diameter"
              value={formData.inner_diameter}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Outer Diameter
            </Typography>
            <Input
              type="text"
              placeholder="Outer Diameter"
              name="outer_diameter"
              value={formData.outer_diameter}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Weight
            </Typography>
            <Input
              type="text"
              placeholder="Weight"
              name="weight"
              value={formData.weight}
              onChange={handleChange}
            />
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
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Start Depth
            </Typography>
            <Input
              type="text"
              placeholder="Start Depth"
              name="start_depth"
              value={formData.start_depth}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              End Depth
            </Typography>
            <Input
              type="text"
              placeholder="End Depth"
              name="end_depth"
              value={formData.end_depth}
              onChange={handleChange}
            />
          </div>
        </div>
      </CardBody>
      <CardBody className="bg-blue-100 h-16 flex items-center justify-center">
        <Typography color="black">Table</Typography>
      </CardBody>
      <CardBody className="bg-lime-100 h-16 flex items-center justify-center">
        <Typography color="black">Gambar Casing</Typography>
      </CardBody>
    </Card>
  );
};

export default Casing;
