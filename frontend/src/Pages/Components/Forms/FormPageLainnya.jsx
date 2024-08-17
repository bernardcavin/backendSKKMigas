import React, { useState } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Typography,
  Button,
  CardFooter,
} from "@material-tailwind/react";
import RadioButton from "../ChildComponets/RadioButton";

const FormPageLainnya = () => {
  const [data, setData] = useState({
    kedalamanAkhirMD: "",
    kedalamanAkhirTVDSS: "",
    kontenHidro: "",
    tipeRig: "",
    kapasitasRig: "",
  });

  

  const handleChange = (e) => {
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
          Lainnya
        </Typography>
        <hr className="my-2 border-gray-800" />
      </CardHeader>
      <CardBody className="flex-col flex gap-4">
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Kedalaman Akhir (MD)
          </Typography>
          <Input
            type="number"
            placeholder="Kedalaman Akhir (MD)"
            name="kedalamanAkhirMD"
            value={data.kedalamanAkhirMD}
            onChange={handleChange}
          />
        </div>
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Kedalaman Akhir (TVDSS)
          </Typography>
          <Input
            type="number"
            placeholder="Kedalaman Akhir (TVDSS)"
            name="kedalamanAkhirTVDSS"
            value={data.kedalamanAkhirTVDSS}
            onChange={handleChange}
          />
        </div>
        <div className="flex flex-col">
          <Typography color="black" className="font-bold">
            Konten Hidro Karbon
          </Typography>
          <div className="flex flex-row">
            <RadioButton
              label={"Oil"}
              nameLabel="kontenHidro"
              title="Oil"
              onChange={() => handleRadioChange("kontenHidro", "Oil")}
              checked={data.kontenHidro === "Oil"}
            />
            <RadioButton
              label={"Gas"}
              nameLabel="kontenHidro"
              title="Gas"
              onChange={() => handleRadioChange("kontenHidro", "Gas")}
              checked={data.kontenHidro === "Gas"}
            />
            <RadioButton
              label={"Dry"}
              nameLabel="kontenHidro"
              title="Dry"
              onChange={() => handleRadioChange("kontenHidro", "Dry")}
              checked={data.kontenHidro === "Dry"}
            />
          </div>
          <Typography color="black" className="font-bold">
            Tipe Rig
          </Typography>
          <div className="flex flex-row">
            <RadioButton
              label={"Jackup"}
              nameLabel="tipeRig"
              title="Jackup"
              onChange={() => handleRadioChange("tipeRig", "Jackup")}
              checked={data.tipeRig === "Jackup"}
            />
            <RadioButton
              label={"Rig Darat"}
              nameLabel="tipeRig"
              title="Rig Darat"
              onChange={() => handleRadioChange("tipeRig", "Rig Darat")}
              checked={data.tipeRig === "Rig Darat"}
            />
            <RadioButton
              label={"Swampbarge"}
              nameLabel="tipeRig"
              title="Swampbarge"
              onChange={() => handleRadioChange("tipeRig", "Swampbarge")}
              checked={data.tipeRig === "Swampbarge"}
            />
            <RadioButton
              label={"Drillship"}
              nameLabel="tipeRig"
              title="Drillship"
              onChange={() => handleRadioChange("tipeRig", "Drillship")}
              checked={data.tipeRig === "Drillship"}
            />
            <RadioButton
              label={"Floater"}
              nameLabel="tipeRig"
              title="Floater"
              onChange={() => handleRadioChange("tipeRig", "Floater")}
              checked={data.tipeRig === "Floater"}
            />
            <RadioButton
              label={"Semisap"}
              nameLabel="tipeRig"
              title="Semisap"
              onChange={() => handleRadioChange("tipeRig", "Semisap")}
              checked={data.tipeRig === "Semisap"}
            />
          </div>
          <div className="flex flex-col">
            <Typography color="black" className="font-bold ">
              Kapasitas Rig (Horse Power)
            </Typography>
            <Input
              type="number"
              placeholder="Kapasitas Rig"
              name="kapasitasRig"
              value={data.kapasitasRig}
              onChange={handleChange}
              className="mt-2"
            />
          </div>
        </div>
      </CardBody>

      <CardFooter className="flex justify-between">
        <Button className="" color="blue" onClick={() => setHandlePage(2)}>
          Prev
        </Button>
        <Button className="" color="blue" onClick={() => setHandlePage(4)}>
          Next
        </Button>
      </CardFooter>
    </Card>
  );
};

export default FormPageLainnya;
