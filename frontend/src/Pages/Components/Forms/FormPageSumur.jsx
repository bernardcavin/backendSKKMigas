import React, { useState, useEffect } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Typography,
  Select,
  Option,
  CardFooter,
  Button,
  Alert,
} from "@material-tailwind/react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const CardPageSumur = ({ sendData }) => {
  const navigate = useNavigate();
  const [typeWell, setTypeWell] = useState([]);
  const [wellClass, setWellClass] = useState([]);
  const [profileType, setProfileType] = useState([]);
  const [environmentType, setEnvironmentType] = useState([]);
  const [wellStatus, setWellStatus] = useState([]);
  const [dataPhase, setDataPhase] = useState([]);
  const [typeOuom, setTypeOuom] = useState([]);
  const [depthDatum, setDepthDatum] = useState([]);
  const [successMsg, setSuccessMsg] = useState("");

  const [formData, setFormData] = useState({
    data_phase: "",
    user: "",
    uwi: "",
    field_id: "",
    well_name: "",
    alias_long_name: "",
    well_type: "",
    well_class: "",
    well_status: "",
    profile_type: "",
    environment_type: "",
    surface_longitude: 0,
    surface_latitude: 0,
    bottom_hole_longitude: 0,
    bottom_hole_latitude: 0,
    maximum_inclination: 0,
    maximum_azimuth: 0,
    line_name: "",
    spud_date: "",
    final_drill_date: "",
    completion_date: "",
    rotary_table_elev: 0,
    rotary_table_elev_ouom: "",
    kb_elev: 0,
    kb_elev_ouom: "FEET",
    derrick_floor_elev: 0,
    derrick_floor_elev_ouom: "FEET",
    ground_elev: 0,
    ground_elev_ouom: "FEET",
    mean_sea_level: 0,
    mean_sea_level_ouom: "RT",
    depth_datum: "RT",
    kick_off_point: 0,
    kick_off_point_ouom: "FEET",
    drill_td: 0,
    drill_td_ouom: "FEET",
    log_td: 0,
    log_td_ouom: "FEET",
    max_tvd: 0,
    max_tvd_ouom: "FEET",
    projected_depth: 0,
    projected_depth_ouom: "FEET",
    final_td: 0,
    final_td_ouom: "FEET",
    remark: "string",
  });

  // console.table(formData);
  

  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/well/create",
        JSON.stringify(formData),
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      console.log(response.status);
      setSuccessMsg("Data Berhasil Dimasukkan");
    } catch (error) {
      console.error("Error fetching well types:", error.response.data);
    }
  };

  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setTypeWell(response.data.well_type);
      setWellClass(response.data.well_class);
      setEnvironmentType(response.data.environment);
      setProfileType(response.data.profile_type);
      setWellStatus(response.data.well_status);
      setDataPhase(response.data.data_phase);
      setTypeOuom(response.data.casing_uom);
      setDepthDatum(response.data.depth_datum);
    } catch (error) {
      console.error("Error fetching well types:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, []);

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

  const handleSelectChangeTypeOuom = (value) => {
    setFormData((prevState) => ({
      ...prevState,
      rotary_table_elev_ouom: value,
      kb_elev_ouom: value,
      derrick_floor_elev_ouom: value,
      ground_elev_ouom: value,
      kick_off_point_ouom: value,
      drill_td_ouom: value,
      log_td_ouom: value,
      max_tvd_ouom: value,
      projected_depth_ouom: value,
      final_td_ouom: value,
    }));
  };

  useEffect(() => {
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
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              UWI
            </Typography>
            <Input
              type="text"
              placeholder="uwi"
              name="uwi"
              value={formData.uwi}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Nama Sumur
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Nama Sumur"
              name="well_name"
              value={formData.well_name}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Nama Lengkap Sumur
            </Typography>
            <Input
              type="text"
              placeholder="Masukkan Nama Lengkap Sumur"
              name="alias_long_name"
              value={formData.alias_long_name}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Type Well
            </Typography>
            <Select
              label="Pilih Type Well"
              name="well_type"
              onChange={handleSelectChange("well_type")}
            >
              {typeWell.map((type, index) => (
                <Option key={index} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Profile Type
            </Typography>
            <Select
              label="Pilih Profile Type"
              name="profile_type"
              onChange={handleSelectChange("profile_type")}
            >
              {profileType.map((type, index) => (
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
              Well Status
            </Typography>
            <Select
              label="Pilih Well Status"
              name="well_status"
              onChange={handleSelectChange("well_status")}
            >
              {wellStatus.map((status, index) => (
                <Option key={index} value={status}>
                  {status}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Well Class
            </Typography>
            <Select
              label="Pilih Well Class"
              name="well_class"
              onChange={handleSelectChange("well_class")}
            >
              {wellClass.map((classOption, index) => (
                <Option key={index} value={classOption}>
                  {classOption}
                </Option>
              ))}
            </Select>
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Environment Type
            </Typography>
            <Select
              label="Pilih Environment Type"
              name="environment_type"
              onChange={handleSelectChange("environment_type")}
            >
              {environmentType.map((envType, index) => (
                <Option key={index} value={envType}>
                  {envType}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Spud Date
            </Typography>
            <Input
              type="datetime-local"
              placeholder="Masukkan Spud Date"
              name="spud_date"
              value={formData.spud_date}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Data Phase
            </Typography>
            <Select
              label="Pilih Data Phase"
              name="data_phase"
              onChange={handleSelectChange("data_phase")}
            >
              {dataPhase.map((phase, index) => (
                <Option key={index} value={phase}>
                  {phase}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Type Jarak
            </Typography>
            <Select
              label="Pilih Type Jarak"
              name="rotary_table_elev_ouom"
              onChange={handleSelectChangeTypeOuom}
            >
              {typeOuom.map((ouom, index) => (
                <Option key={index} value={ouom}>
                  {ouom}
                </Option>
              ))}
            </Select>
          </div>
        </div>
        {/* Rest of the form elements go here, following the same pattern */}
      </CardBody>
      <CardFooter>
        <Button onClick={handleSubmit}>Submit</Button>
        {successMsg && <Alert>{successMsg}</Alert>}
      </CardFooter>
    </Card>
  );
};

export default CardPageSumur;
