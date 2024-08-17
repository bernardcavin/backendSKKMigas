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
    elevasiMinsiLevel: "",
    MSL: "",
    latitudePermukaan: "",
    latitudeSubsurface: "",
    longitudePermukaan: "",
    longitudeSubsurface: "",
  });

  

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
        <div className="flex flex-col">
          <div className="flex flex-row">
            <div className="flex flex-col w-full">
              <Typography color="black" className="font-bold">
                Posisi
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
                Elevasi GL
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
                Elevasi RKB
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
                Elevasi Minsi Level
              </Typography>
              <Input
                type="text"
                placeholder="Elevasi Minsi Level"
                name="elevasiMinsiLevel"
                value={data.elevasiMinsiLevel}
                onChange={handleInputChange}
              />
            </div>
            <div className="flex flex-col w-full">
              <Typography color="black" className="font-bold">
                MSL
              </Typography>
              <Input
                type="text"
                placeholder="MSL"
                name="MSL"
                value={data.MSL}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>
        <div className="flex w-full gap-4">
          <div className="flex flex-col w-full">
            <div className="flex flex-col">
              <Typography color="black" variant="h6">
                Latitude Permukaan
              </Typography>
              <Typography color="black" variant="small">
                Presisi 6 Angka dibelakang koma: ESPG:4326
              </Typography>
              <Input
                type="text"
                variant="outline"
                placeholder="Latitude Permukaan"
                name="latitudePermukaan"
                value={data.latitudePermukaan}
                onChange={handleInputChange}
              />
            </div>
            <div className="flex flex-col">
              <Typography color="black" variant="h6">
                Longitude Permukaan
              </Typography>
              <Typography color="black" variant="small">
                Presisi 6 Angka dibelakang koma: ESPG:4326
              </Typography>
              <Input
                type="text"
                variant="outline"
                placeholder="Longitude Permukaan"
                name="longitudePermukaan"
                value={data.longitudePermukaan}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="flex flex-col w-full">
            <div className="flex flex-col">
              <Typography color="black" variant="h6">
                Latitude Subsurface
              </Typography>
              <Typography color="black" variant="small">
                Presisi 6 Angka dibelakang koma: ESPG:4326
              </Typography>
              <Input
                type="text"
                variant="outline"
                placeholder="Latitude Subsurface"
                name="latitudeSubsurface"
                value={data.latitudeSubsurface}
                onChange={handleInputChange}
              />
            </div>
            <div className="flex flex-col">
              <Typography color="black" variant="h6">
                Longitude Subsurface
              </Typography>
              <Typography color="black" variant="small">
                Presisi 6 Angka dibelakang koma: ESPG:4326
              </Typography>
              <Input
                type="text"
                variant="outline"
                placeholder="Longitude Subsurface"
                name="longitudeSubsurface"
                value={data.longitudeSubsurface}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default FormPagePosisi;
