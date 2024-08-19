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
import * as XLSX from 'xlsx';
import { useRef } from "react";


const FormPageDrilling = ({ sendData }) => {

  const [tableData, setTableData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [file, setFile] = useState(null);
  const fileUseReff = useRef(null);


  
  const handleFileUpload = (file) => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        console.log(jsonData);

        if (jsonData.length > 0) {
          const fileHeaders = jsonData[0];
          // const isValid = expectedHeaders.every((header, index) => header === fileHeaders[index]);

          // if (isValid) {
          setHeaders(fileHeaders);
          setTableData(jsonData.slice(1));
          setAlert(null); // Clear any previous alerts
          // } else {
          //   setTableData([]);
          //   setHeaders([]);
          //   setAlert({
          //     type: "error",
          //     message: `Header file tidak sesuai dengan ketentuan. Harus sesuai dengan urutan: ${expectedHeaders.join(', ')}`,
          //   });
          // }
        }
      };
      reader.readAsArrayBuffer(file);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFile([file]);
      handleFileUpload(file);
    }
  };
  console.log(file);

  const [data, setData] = useState({
    hazard_type: "",
    hazard_description: "",
    severity: "",
    mitigation: "",
    remark: ""
  });




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
      <CardBody className="flex-col flex gap-4 h-96 overflow-y-auto">
        {tableData.length > 0 ? (
          <table className="min-w-full table-auto border-collapse border border-gray-200">
            <thead className="sticky top-0 bg-white">
              <tr>
                {headers.map((header, index) => (
                  <th key={index} className="border border-gray-300 p-2 bg-gray-100 text-left">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, rowIndex) => (
                <tr key={rowIndex} className="border border-gray-300">
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} className="border border-gray-300 p-2">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <Typography color="black" className="text-center">
            No data available. Please upload a file.
          </Typography>
        )}
      </CardBody>
    </Card>
  );
};

export default FormPageDrilling;
