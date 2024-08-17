import React, { useState } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
} from "@material-tailwind/react";
import RadioButton from "../ChildComponets/RadioButton";

const FormPagePosisi = () => {
  const [data, setData] = useState({
    posisi: "",
    satuan: "",
    elevasiGL: "",
    elevasiRKB: "",
    elevasiMSL: "",
    azimuth: "",
    depthDatum: "",
    logTd: "",
    projectDepth: "",
    latitudePermukaan: "",
    longitudePermukaan: "",
    latitudeSubsurface: "",
    longitudeSubsurface: "",
    keterangan: "",
    elevasiDerrickFloor: "",
    kickOffPoint: "",
    drillTd: "",
    maxTVD: "",
    finalTd: "",
  });

  console.log(data);
  

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleRadioChange = (name, value) => {
    setData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  return (
    <Card variant="filled" className="w-full" shadow={true}>
      <CardHeader floated={false} className="mb-0" shadow={false}>
        <Typography variant="h5" color="black">
          Lokasi
        </Typography>
        <hr className="my-2 border-gray-800" />
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Tujuan
            </Typography>
            <div className="flex flex-row">
              <RadioButton
                label={"Offshore"}
                name="posisi"
                title="Offshore"
                onChange={() => handleRadioChange("posisi", "Offshore")}
                checked={data.posisi === "Offshore"}
              />
              <RadioButton
                label={"Onshore"}
                name="posisi"
                title="Onshore"
                onChange={() => handleRadioChange("posisi", "Onshore")}
                checked={data.posisi === "Onshore"}
              />
            </div>
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Satuan
            </Typography>
            <div className="flex flex-row">
              <RadioButton
                label={"Feet(Ft)"}
                name="satuan"
                title="Feet(Ft)"
                onChange={() => handleRadioChange("satuan", "Feet(Ft)")}
                checked={data.satuan === "Feet(Ft)"}
              />
              <RadioButton
                label={"Meter(M)"}
                name="satuan"
                title="Meter(M)"
                onChange={() => handleRadioChange("satuan", "Meter(M)")}
                checked={data.satuan === "Meter(M)"}
              />
            </div>
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Elevasi GL (Ground Level)
            </Typography>
            <Input
              type="text"
              placeholder="Elevasi GL"
              name="elevasiGL"
              value={data.elevasiGL}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Elevasi RKB (Rotary Kelly Bushing)
            </Typography>
            <Input
              type="text"
              placeholder="Elevasi RKB"
              name="elevasiRKB"
              value={data.elevasiRKB}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Elevasi MSL (Mean Sea Level)
            </Typography>
            <Input
              type="text"
              placeholder="Elevasi MSL"
              name="elevasiMSL"
              value={data.elevasiMSL}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Elevasi Derrick Floor
            </Typography>
            <Input
              type="text"
              placeholder="Elevasi Derrick Floor"
              name="elevasiDerrickFloor"
              value={data.elevasiDerrickFloor}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Azimuth / Kemiringan Maks
            </Typography>
            <Input
              type="text"
              placeholder="Azimuth / Kemiringan Maks"
              name="azimuth"
              value={data.azimuth}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Kick Off Point (KOP)
            </Typography>
            <Input
              type="text"
              placeholder="Kick Off Point (KOP)"
              name="kickOffPoint"
              value={data.kickOffPoint}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Depth Datum
            </Typography>
            <Input
              type="text"
              placeholder="Depth Datum"
              name="depthDatum"
              value={data.depthDatum}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Drill Td
            </Typography>
            <Input
              type="text"
              placeholder="Drill Td"
              name="drillTd"
              value={data.drillTd}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Log Td
            </Typography>
            <Input
              type="text"
              placeholder="Log Td"
              name="logTd"
              value={data.logTd}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Max TVD
            </Typography>
            <Input
              type="text"
              placeholder="Max TVD"
              name="maxTVD"
              value={data.maxTVD}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Project Depth
            </Typography>
            <Input
              type="text"
              placeholder="Project Depth"
              name="projectDepth"
              value={data.projectDepth}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Final Td
            </Typography>
            <Input
              type="text"
              placeholder="Final Td"
              name="finalTd"
              value={data.finalTd}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Latitude Permukaan
            </Typography>
            <Input
              type="text"
              placeholder="Latitude Permukaan"
              name="latitudePermukaan"
              value={data.latitudePermukaan}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Latitude Subsurface
            </Typography>
            <Input
              type="text"
              placeholder="Latitude Subsurface"
              name="latitudeSubsurface"
              value={data.latitudeSubsurface}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-row w-full gap-4">
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Longitude Permukaan
            </Typography>
            <Input
              type="text"
              placeholder="Longitude Permukaan"
              name="longitudePermukaan"
              value={data.longitudePermukaan}
              onChange={handleInputChange}
            />
          </div>
          <div className="flex flex-col w-full">
            <Typography color="black" className="font-bold">
              Longitude Subsurface
            </Typography>
            <Input
              type="text"
              placeholder="Longitude Subsurface"
              name="longitudeSubsurface"
              value={data.longitudeSubsurface}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Keterangan
          </Typography>
          <Input
            type="text"
            placeholder="Keterangan"
            name="keterangan"
            value={data.keterangan}
            onChange={handleInputChange}
          />
        </div>
      </CardBody>
    </Card>
  );
};

export default FormPagePosisi;
