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
  Alert
} from "@material-tailwind/react";
import RadioButton from "../ChildComponets/RadioButton";
import axios from "axios";
import { Navigate, useNavigate } from "react-router-dom";

const CardPageSumur = ({ sendData }) => {
  const navigate = useNavigate();
  const [typeWell, setTypeWell] = useState([]);
  const [wellClass, setWellClass] = useState([]);
  const [profileType, setProfileType] = useState([]);
  const [environmentType, setEnvironmentType] = useState([]);
  const [wellStatus, setWellStatus] = useState([])

  const [succesMsg, setSuccesMsg] = useState('');



  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/well/create", JSON.stringify(formData),
        {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        }
      ).then((response) => {
        console.log(response.status);
        setSuccesMsg("Data Berhasil Dimasukkan");

      })
    } catch (error) {
      console.error("Error fetching well types:", error.response.data);

    }
  }
  const getAllData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/utils/enum/all");
      setTypeWell(response.data.well_type);
      setWellClass(response.data.well_class);
      setEnvironmentType(response.data.environment);
      setProfileType(response.data.profile_type);
      setWellStatus(response.data.well_status)





      // console.log(response.data);
      // console.log(response.data);
      // Menyimpan data ke dalam state
    } catch (error) {
      console.error("Error fetching well types:", error);
    }
  };

  useEffect(() => {
    getAllData();
  }, [1]);

  // useEffect(() => {
  //   sendData(formData);
  // }, [formData]);


  // Panggil saat file diproses
  const [formData, setFormData] = useState({
    data_phase: "PLAN",
    user: "string",
    uwi: "string",
    field_id: "string",
    well_name: "string",
    alias_long_name: "string",
    well_type: "OIL",
    well_class: "WILDCAT",
    well_status: "Active",
    profile_type: "DIRECTIONAL",
    environment_type: "MARINE",
    surface_longitude: 0,
    surface_latitude: 0,
    bottom_hole_longitude: 0,
    bottom_hole_latitude: 0,
    maximum_inclination: 0,
    maximum_azimuth: 0,
    line_name: "string",
    spud_date: "2024-08-18T13:44:40.536Z",
    final_drill_date: "2024-08-18T13:44:40.536Z",
    completion_date: "2024-08-18T13:44:40.536Z",
    rotary_table_elev: 0,
    rotary_table_elev_ouom: "FEET",
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
    well_documents: [
      {
        file_id: "string",
        title: "string",
        media_type: "EXTERNAL_HARDDISK",
        document_type: "string",
        remark: "string"
      }
    ],
    well_casings: [
      {
        casing_type: "CONDUCTOR PIPE",
        grade: "string",
        inside_diameter: 0,
        inside_diameter_ouom: "INCH",
        outside_diameter: 0,
        outside_diameter_ouom: "INCH",
        base_depth: 0,
        base_depth_ouom: "FEET"
      }
    ],
    well_trajectories: [
      {
        file_id: "string"
      }
    ],
    well_ppfgs: [
      {
        file_id: "string"
      }
    ],
    well_logs: [
      {
        file_id: "string"
      }
    ],
    well_drilling_parameters: [
      {
        file_id: "string"
      }
    ],
    well_strat: [
      {
        strat_unit_id: "string",
        depth_datum: "RT",
        top_depth: 0,
        bottom_depth: 0,
        depth_uoum: "FEET"
      }
    ]

  });





  const statusOptions = ["Valid", "Proses", "Ditolak"];


  // Handle input change for text and select inputs
  // const handleChange = (event) => {
  //   const { name, value, type } = event.target;


  //   setFormData((prevState) => ({
  //     ...prevState,
  //     planned_well: {
  //       ...prevState.planned_well,
  //       [name]: type === "number" ? parseInt(value) : value,
  //     },
  //   }));
  // };


  const handleChange = (event) => {
    const { name, value, type } = event.target;


    setFormData((prevState) => ({
      ...prevState,
      [name]: type === "number" ? parseInt(value) : value,

    }));
  };


  const handleSelectChangeTypeWell = (value) => {

    setFormData((prevState) => ({
      ...prevState,
      planned_well: {
        ...prevState.planned_well,
        well_type: value,
      },
    }));
  };
  const handleSelectChangeStatusAFE = (value) => {

    setFormData((prevState) => ({
      ...prevState,
      status_afe: value,
    }));
  };
  const handleSelectChangeWellClass = (value) => {

    setFormData((prevState) => ({
      ...prevState,
      well_class: value,
    }));
  };
  // const handleSelectChange = (name) => (value) => {
  //   setFormData((prevState) => ({
  //     ...prevState,
  //     planned_well: {
  //       ...prevState.planned_well,
  //       [name]: value,
  //     },
  //   }));
  // };
  const handleSelectChange = (name) => (value) => {
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,

    }));
  };

  // Handle change for radio buttons
  const handleRadioChange = (name, value) => {
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  useEffect(() => {
    // Call sendData whenever formData changes
    sendData(formData);
    console.log(formData);






  }, [formData]);

  return (

    <Card variant="filled" className="w-full" shadow={true}>
      {succesMsg ?
        (
          <Alert color="green" className="">{succesMsg}</Alert>
        ) : null}
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
              name="type_well"

              onChange={handleSelectChange("well_type")}
            >
              {typeWell.map((typeWell, index) => (
                <Option key={index} value={typeWell}>
                  {typeWell}
                </Option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Profile Type
            </Typography>
            <Select
              label="Pilih Type Well"
              name="Profile_type"
              onChange={handleSelectChange("profile_type")}
            >
              {profileType.map((typeWell, index) => (
                <Option key={index} value={typeWell}>
                  {typeWell}
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
              label="Well Status"
              name="well_status"

              onChange={handleSelectChange("well_status")}
            >
              {wellStatus.map((typeWell, index) => (
                <Option key={index} value={typeWell}>
                  {typeWell}
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
              {wellClass.map((typeWell, index) => (
                <Option key={index} value={typeWell}>
                  {typeWell}
                </Option>
              ))}
            </Select>
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Environment type
            </Typography>

            <Select name="environment_type"

              onChange={handleSelectChange("environment_type")} label="Pilih Environment type">
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
              type="date"
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
              Lintang Lubang Bawah
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Lintang Lubang Bawah"
              name="bottom_hole_latitude"
              value={formData.bottom_hole_latitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Garis Bujur Lubang Bawah
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Bawah"
              name="bottom_hole_longitude"
              value={formData.bottom_hole_longitude}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Lintang Lubang Atas
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Lintang Lubang Atas "
              name="surface_hole_latitude"
              value={formData.surface_latitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Garis Bujur Lubang Atas
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Ketinggian Tanah
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Elevasi Kb
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Kick Off Point
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Log TD
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Max TVD
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Maximum Azimuth
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Mean Sea Level
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Project Depth
            </Typography>
            <Input
              type="number"
              placeholder="Masukkan Garis Bujur Lubang Atas"
              name="surface_hole_longitude"
              value={formData.surface_longitude}
              onChange={handleChange}
            />
          </div>
        </div>
        {/* Dimasukkan Ke Dalam FORM JOB */}

      </CardBody>
      <CardFooter>


      </CardFooter>
    </Card>
  );
};

export default CardPageSumur;
