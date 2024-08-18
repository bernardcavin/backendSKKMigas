import React, { useState, useEffect } from 'react';
import {
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Button,
  Alert,
  Select,
  Option,
} from '@material-tailwind/react';
import * as XLSX from 'xlsx';
import axios from 'axios';

const FormDepthVSDays = ({sendData}) => {
  const [depthUom, setDepthUom] = useState([]);
  const [depthDatum, setDepthDatum] = useState([]);
  const [files, setFiles] = useState([]);  // Pastikan files diinisialisasi dengan useState

  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setDepthUom(response.data.depth_uom);
      setDepthDatum(response.data.depth_datum);
      
    } catch (error) {
    }
  };
  

  useEffect(() => {
    getAllData();
  }, []);


  
  const [formData, setFormData] = useState({
    time: "",
    measured_depth: 0,
    measured_depth_uoum: "",
    measured_depth_datum: "",
    true_vertical_depth: 0,
    true_vertical_depth_uoum: "",
    true_vertical_depth_sub_sea: 0,
    true_vertical_depth_sub_sea_uoum: "",
    daily_cost: 0,
    summary: "",
    current_operations: "",
    next_operations: "",
  });

  useEffect(() => {
    sendData(formData);
    
     
  }, [formData]);
  
  
  const [tableData, setTableData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [alert, setAlert] = useState(null);
  
  const expectedHeaders = ["Time", "Measured Depth", "Measured Depth UOM", "Measured Depth Datum", "True Vertical Depth", "True Vertical Depth UOM", "True Vertical Depth Sub-Sea", "True Vertical Depth Sub-Sea UOM", "Daily Cost", "Summary", "Current Operations", "Next Operations"];

  const handleFileUpload = (file) => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        if (jsonData.length > 0) {
          const fileHeaders = jsonData[0];
          const isValid = expectedHeaders.every((header, index) => header === fileHeaders[index]);

          if (isValid) {
            setHeaders(fileHeaders);
            setTableData(jsonData.slice(1));
            setAlert(null); // Clear any previous alerts
          } else {
            setTableData([]);
            setHeaders([]);
            setAlert({
              type: "error",
              message: `Header file tidak sesuai dengan ketentuan. Harus sesuai dengan urutan: ${expectedHeaders.join(', ')}`,
            });
          }
        }
      };
      reader.readAsArrayBuffer(file);
    }
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
      setFiles([file]);
      handleFileUpload(file);
    }
  };

  const handleFileRemove = () => {
    setFiles([]);
    setTableData([]);
    setHeaders([]);
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return "";
    const date = new Date(dateTimeString);
    return date.toISOString();
};

const handleChange = (event) => {
    const { name, value, type } = event.target;
    setFormData((prevState) => ({
        ...prevState,
        [name]: 
            type === "number" ? parseFloat(value) || 0 :
            name === "time" ? formatDateTime(value) :
            value
    }));
};
 
  
  const handleAddSection = () => {
    
  };

  return (
    <Card variant="filled" className="w-full">
      <CardHeader floated={false} className="mb-4 shadow-none flex justify-between items-center">
        <Typography variant="h5" color="black">
          Job Activity
        </Typography>
        <div>
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
        </div>
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Time
            </Typography>
            <Input
              type="datetime-local"
              placeholder="Time"
              name="time"
              value={formData.time ? formData.time.substring(0, 16) : ""}
              onChange={handleChange}
            />
          </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Measured Depth
            </Typography>
            <Input
              type="number"
              placeholder="Measured Depth"
              name="measured_depth"
              value={formData.measured_depth}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Measured Depth UOUM
            </Typography>
            <Select
              label="Pilih Depth UOUM"
              name="measured_depth_uoum"
              onChange={handleSelectChange("measured_depth_uoum")}
            >
              {depthUom.map((type, index) => (
                <Option key={index} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Measured Depth Datum
            </Typography>
            <Select
              label="Pilih Depth Datum"
              name="measured_depth_datum"
              onChange={handleSelectChange("measured_depth_datum")}
            >
              {depthDatum.map((type, index) => (
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
              True Vertical Depth
            </Typography>
            <Input
              type="number"
              placeholder="True Vertical Depth"
              name="true_vertical_depth"
              value={formData.true_vertical_depth}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
            True Vertical Depth UOUM
            </Typography>
            <Select
              label="Pilih True Vertical Depth UOUM"
              name="true_vertical_depth_uoum"
              onChange={handleSelectChange("true_vertical_depth_uoum")}
            >
              {depthUom.map((type, index) => (
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
              True Vertical Depth Sub-Sea
            </Typography>
            <Input
              type="number"
              placeholder="True Vertical Depth Sub-Sea"
              name="true_vertical_depth_sub_sea"
              value={formData.true_vertical_depth_sub_sea}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
            True Vertical Depth Sub-Sea UOUM
            </Typography>
            <Select
              label="Pilih True Vertical Depth Sub-Sea UOUM"
              name="true_vertical_depth_sub_sea_uoum"
              onChange={handleSelectChange("true_vertical_depth_sub_sea_uoum")}
            >
              {depthUom.map((type, index) => (
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
              Daily Cost
            </Typography>
            <Input
              type="number"
              placeholder="Daily Cost"
              name="daily_cost"
              value={formData.daily_cost}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Summary
            </Typography>
            <Input
              type="text"
              placeholder="Summary"
              name="summary"
              value={formData.summary}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Current Operations
          </Typography>
          <Input
            type="text"
            placeholder="Current Operations"
            name="current_operations"
            value={formData.current_operations}
            onChange={handleChange}
          />
        </div>

        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Next Operations
          </Typography>
          <Input
            type="text"
            placeholder="Next Operations"
            name="next_operations"
            value={formData.next_operations}
            onChange={handleChange}
          />
        </div>

        <Button color="black" className="mt-4 button" size="lg" onClick={handleAddSection}>
          Tambah Section
        </Button>
      </CardBody>

      {alert && (
        <Alert color={alert.type} className="mb-4">
          {alert.message}
        </Alert>
      )}

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

      <CardBody className="bg-lime-100 h-36 flex items-center justify-center">
        <Typography color="black">Grafik</Typography>
      </CardBody>
    </Card>
  );
};

export default FormDepthVSDays;
