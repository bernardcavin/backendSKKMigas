import React, { useState } from 'react';
import {
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Button,
  Alert,
} from '@material-tailwind/react';
import { Dropzone, FileItem } from "@dropzone-ui/react";
import * as XLSX from 'xlsx';

const FormDepthVSDays = () => {
  const [formData, setFormData] = useState({
    kegiatan: "",
    days: "",
    start_depth: "",
    end_depth: "",
  });

  console.table(formData);
  

  const [tableData, setTableData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [alert, setAlert] = useState(null);
  const [files, setFiles] = useState([]);

  const expectedHeaders = ["Kode Item", "Nama Item", "Terjual", "Harga", "Stok", "Label"];

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

  const handleFileChange = (incomingFiles) => {
    const file = incomingFiles[0]?.file; // Ensure we're working with a File object
    if (file) {
      setFiles(incomingFiles);
      handleFileUpload(file);
    }
  };

  const handleFileRemove = (file) => {
    setFiles(files.filter(f => f.file !== file));
    setTableData([]);
    setHeaders([]);
  };

  // Handle input change
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleAddSection = () => {
    // Logic untuk menambah section baru bisa ditambahkan di sini
    console.log("Tambah Section button clicked");
  };

  return (
    <Card variant="filled" className="w-full">
      <CardHeader floated={false} className="mb-4 shadow-none">
        <Typography variant="h5" color="black">
          Depth vs Days
        </Typography>
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
      <div className="flex flex-col w-full">
              <Typography color="black" className="font-bold">
                Upload File
              </Typography>
              <div className="mt-4">
                <Dropzone
                  onChange={handleFileChange}
                  value={files}
                  maxFiles={1}
                  accept=".csv, .xlsx, .xls"
                  label="Drag and Drop or Choose a Local File"
                  footer={false}
                  style={{ border: "2px dashed #E5E7EB", padding: "20px", textAlign: "center" }}
                >
                  {files.map((fileWrapper) => (
                    <FileItem
                      key={fileWrapper.file.name}
                      file={fileWrapper.file}
                      onDelete={() => handleFileRemove(fileWrapper.file)}
                      localization="EN-en"
                    />
                  ))}
                </Dropzone>
              </div>
            </div>
        <div className="mt-4">
          <div className="flex flex-row w-full justify-between gap-4">
            <div className="flex flex-col w-full ">
              <Typography color="black" className="font-bold">
                Kegiatan
              </Typography>
              <Input
                type="text"
                placeholder="Kegiatan"
                name="kegiatan"
                value={formData.kegiatan}
                onChange={handleChange}
                className="mb-2"
              />
            </div>
            <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Days
            </Typography>
            <Input
              type="text"
              placeholder="Days"
              name="days"
              value={formData.days}
              onChange={handleChange}
            />
          </div>
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
        
        <Button color="blue" className="mt-4" onClick={handleAddSection}>
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
            <thead>
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
