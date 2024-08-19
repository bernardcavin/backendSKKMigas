import React, { useEffect, useState } from 'react';
import {
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Button,
  Alert,
} from '@material-tailwind/react';

const WorkBreakdownStructure = ({ sendData}) => {
  const [formData, setFormData] = useState({
    event: "",
    start_date: "",
    end_date: "",
    remarks: "",
  });
    
  

  const [tableData, setTableData] = useState([]);
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    sendData(tableData);
  }, [tableData]);
  

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
      // Check the dates immediately after setting them
    if (name === "end_date") {
        const startDate = new Date(formData.start_date);
        const endDate = new Date(value);
  
        if (endDate < startDate) {
          setAlert({
            type: "error",
            message: "End date cannot be earlier than start date.",
          });
        } else {
          setAlert(null); // Clear alert if dates are valid
        }
      }
  };

  const handleAddEvent = () => {
    if (formData.event && formData.start_date && formData.end_date) {
      setTableData([...tableData, formData]);
      console.log(tableData);
      
      setFormData({ event: "", start_date: "", end_date: "", remarks: "" });
      setAlert(null);
    } else {
      setAlert({
        type: "error",
        message: "Please fill in all required fields.",
      });
    }
  };

  return (
    <Card variant="filled" className="w-full">
      <CardHeader floated={false} className="mb-4 shadow-none flex justify-between items-center">
        <Typography variant="h5" color="black">
          Work Breakdown Structure
        </Typography>
        <Button color="black" onClick={handleAddEvent}>
          Add Event
        </Button>
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Event
          </Typography>
          <Input
            type="text"
            placeholder="Event"
            name="event"
            value={formData.event}
            onChange={handleChange}
          />
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Start Date
            </Typography>
            <Input
              type="datetime-local"
              placeholder="Start Date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              End Date
            </Typography>
                      <Input
                          min={formData.start_date}
              type="datetime-local"
              placeholder="End Date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-col w-full">
          <Typography color="black" className="font-bold">
            Remarks
          </Typography>
          <Input
            type="text"
            placeholder="Remarks"
            name="remarks"
            value={formData.remarks}
            onChange={handleChange}
          />
        </div>

        {alert && (
          <Alert color="red" className="mt-4">
            {alert.message}
          </Alert>
        )}

        <CardBody className="flex-col flex gap-4 h-96 overflow-y-auto">
          {tableData.length > 0 ? (
            <table className="min-w-full table-auto border-collapse border border-gray-200">
              <thead className="sticky top-0 bg-white">
                <tr>
                  <th className="border border-gray-300 p-2 bg-gray-100 text-left">Event</th>
                  <th className="border border-gray-300 p-2 bg-gray-100 text-left">Start Date</th>
                  <th className="border border-gray-300 p-2 bg-gray-100 text-left">End Date</th>
                  <th className="border border-gray-300 p-2 bg-gray-100 text-left">Remarks</th>
                </tr>
              </thead>
              <tbody>
                {tableData.map((row, index) => (
                  <tr key={index} className="border border-gray-300">
                    <td className="border border-gray-300 p-2">{row.event}</td>
                    <td className="border border-gray-300 p-2">{row.start_date}</td>
                    <td className="border border-gray-300 p-2">{row.end_date}</td>
                    <td className="border border-gray-300 p-2">{row.remarks}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <Typography color="black" className="text-center">
              No data available. Please add an event.
            </Typography>
          )}
        </CardBody>
      </CardBody>
    </Card>
  );
};

export default WorkBreakdownStructure;
