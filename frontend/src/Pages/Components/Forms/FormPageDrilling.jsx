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
import { useEffect } from "react";
import axios from "axios";

const FormHSEPlan = ({ sendData }) => {



  const [data, setData] = useState({
    hazard_type: "",
    hazard_description: "",
    severity: "",
    mitigation: "",
    remark: ""
  });


  console.table(data);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };
  const [hazardType, setHazardType] = useState([]);
  const [severity, setSeverity] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/utils/enum/all").then((response) => {
      // console.log(response.data.hazard_type);
      setHazardType(response.data.hazard_type);
      setSeverity(response.data.severity);
    })
  }, [setHazardType])
  useEffect(() => {
    sendData(data);
  }, [data]);

  const handleSelectChange = (value) => {
    setData((prevState) => ({
      ...prevState,
      hazard_type: value,
    }));
  };
  const handleSelectChangeSeverity = (value) => {
    setData((prevState) => ({
      ...prevState,
      severity: value,
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
              Tipe Hazard
            </Typography>
            <Select label="Tipe Hazard" onChange={handleSelectChange}>
              {hazardType.map((hazard, index) => (
                <Option key={index} value={hazard}>{hazard}</Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col mt-2">
            <Typography color="black" className="font-bold">
              Hazard Description
            </Typography>
            <Input
              type="text"
              placeholder="Hazard Description"
              name="hazard_description"
              value={data.potensiBahaya}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col mb-2">
            <Typography color="black" className="font-bold">
              Severity
            </Typography>
            <Select label="Severity" onChange={handleSelectChangeSeverity}>
              {severity.map((hazard, index) => (
                <Option key={index} value={hazard}>{hazard}</Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col mt-4">
            <Typography color="black" className="font-bold">
              Mitigation
            </Typography>
            <Input
              type="text"
              placeholder="Mitigation"
              name="mitigation"
              value={data.upayaPengandilan}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col mt-4">
            <Typography color="black" className="font-bold">
              Remark
            </Typography>
            <Input
              type="text"
              placeholder="Remark"
              name="remark"
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
