import { useEffect, useState } from "react";
import {
  Box,
  VStack,
  HStack,
  SimpleGrid,
  Button,
  Text,
} from "@chakra-ui/react";
import { FaClipboardCheck, FaTimesCircle, FaCheckCircle } from "react-icons/fa";
import { Link, Outlet, useNavigate } from "react-router-dom";
import CustomCard from "./../Components/Card/CustomCard"; // Path yang sesuai
import WellTable from "./../Components/Card/WellTable"; // Path yang sesuai
import axios from "axios";
import { useLocation } from "react-router-dom";
import { getDataPlanningExploration } from "../API/AllEnums";

const PengajuanPekerjaan = ({ handleTambahData }) => {
  const location = useLocation();
  const [dataDrilling, setDataDrilling] = useState(null);

  const [showPengajuanPekerjaan, setShowPengajuanPekerjaan] = useState(true);

  const sendData = (data) => {
    setDataDrilling(data);
  };
  const ShowButtonSubmit = () => {
    return (
      <Button colorScheme="blue" onClick={HandleSubmit}>
        Submit Data
      </Button>
    );
  };
  const [dataSubmit, setdataSumbit] = useState({
    planned_well: {},
  });

  useEffect(() => {
    if (location.pathname === "/dashboard/submission/pengajuanform") {
      setShowPengajuanPekerjaan(!showPengajuanPekerjaan);
    } else if (location.pathname === "/dashboard/submission") {
      setShowPengajuanPekerjaan(true);
    }
  }, [location.pathname]);

  useEffect(() => {
    if (dataDrilling?.teknisData) {
      const filterObject = (obj, keysToRemove) => {
        return Object.keys(obj)
          .filter((key) => !keysToRemove.includes(key)) // Hanya simpan kunci yang tidak diinginkan
          .reduce((result, key) => {
            result[key] = obj[key];
            return result;
          }, {});
      };
      const wellWithoutUnit = filterObject(dataDrilling.teknisData.elevasi, [
        "unit",
      ]);

      const plannedWellData = {
        ...dataDrilling.teknisData.well,
        ...dataDrilling.teknisData.koordinat,
        ...wellWithoutUnit,
      };

      //Filter Data

      const jobData = {
        ...dataDrilling.operasionalData.proposedJob,
      };

      const work_breakdown = {
        ...dataDrilling.operasionalData.workBreakdown,
      };
      const jobDocument = {
        ...dataDrilling.operasionalData.jobDocument,
      };
      const well_casing = {
        ...dataDrilling.teknisData.wellSummary,
      };
      const job_Operation_Days = {
        ...dataDrilling.operasionalData.jobOperationDays,
      };
      const newjobOperationDays = filterObject(
        dataDrilling.operasionalData.jobOperationDays,
        ["unit"]
      );
      const { totalBudget, ...newJobData } = jobData;
      setdataSumbit({
        proposed_job: {
          ...newJobData,
          well: plannedWellData,
          work_breakdown_structure: work_breakdown,
          contract_type: "COST-RECOVERY",
          drilling_class: "EXPLORATION",
          job_instance_type: "INITIAL PROPOSAL",
          job_operation_days: newjobOperationDays,
          total_budget: 0,
          well: {
            uwi: "string",
            field_id: "string",
            area_id: "string",
            kkks_id: "string",
            data_phase: "PROPOSED",
            well_name: "string",
            alias_long_name: "string",
            well_type: "WILDCAT",
            well_status: "Active",
            well_profile_type: "DIRECTIONAL",
            hydrocarbon_target: "OIL",
            environment_type: "MARINE",
            surface_longitude: 0,
            surface_latitude: 0,
            bottom_hole_longitude: 0,
            bottom_hole_latitude: 0,
            maximum_inclination: 0,
            azimuth: 0,
            line_name: "string",
            spud_date: "2024-08-24T13:38:32.114Z",
            final_drill_date: "2024-08-24T13:38:32.114Z",
            completion_date: "2024-08-24T13:38:32.114Z",
            rotary_table_elev: 0,
            rotary_table_elev_uom: "FEET",
            kb_elev: 0,
            kb_elev_uom: "FEET",
            derrick_floor_elev: 0,
            derrick_floor_elev_uom: "FEET",
            ground_elev: 0,
            ground_elev_uom: "FEET",
            mean_sea_level: 0,
            mean_sea_level_uom: "FEET",
            depth_datum: "RT",
            kick_off_point: 0,
            kick_off_point_uom: "FEET",
            maximum_tvd: 0,
            maximum_tvd_uom: "FEET",
            final_md: 0,
            final_md_uom: "FEET",
            remark: "string",
            well_summary: dataDrilling.teknisData.wellSummary,
            well_stratigraphy: dataDrilling.teknisData.stratigraphy,
            well_casing: dataDrilling.teknisData.wellCasing,
            well_test: dataDrilling.teknisData.wellTest,
            well_casing: well_casing,
            well_document: jobDocument,
            well_trajectories: [
              {
                file_id: "string",
                data_format: "IMAGE",
                data_class: "WELL TRAJECTORY",
              },
            ],
            well_ppfgs: [
              {
                file_id: "string",
                data_format: "IMAGE",
                data_class: "PPFG",
              },
            ],
            well_logs: [
              {
                file_id: "string",
                data_format: "IMAGE",
                data_class: "WELL LOG",
              },
            ],
            well_drilling_parameters: [
              {
                file_id: "string",
                data_format: "IMAGE",
                data_class: "DRILLING PARAMETER",
              },
            ],
          },
        },
      });
    }
  }, [dataDrilling]);

  // console.log(dataDrilling);
  // console.log(location);

  const HandleSubmit = () => {
    try {
      const response = axios.post(
        "http://127.0.0.1:8000/job/planning/create/exploration",
        JSON.stringify(dataSubmit),
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response) {
        alert("Data Berhasil Disimpan");
      }
    } catch (error) {
      console.log("Error Dalam Kirim Data", error);
    }
  };

  // useEffect(() => {
  //   if (dataDrilling?.teknisData) {
  //     const { unit, ...wellWithoutUnit } = dataDrilling.teknisData.elevasi;
  //     console.log(wellWithoutUnit);

  //     const plannedWellData = {
  //       ...dataDrilling.teknisData.well,
  //       ...dataDrilling.teknisData.koordinat, // Contoh jika ada data dari koordinat
  //       ...wellWithoutUnit, // Contoh jika ada data dari elevasi
  //       // Tambahkan sumber data lainnya jika diperlukan
  //     };

  //     setdataSumbit({
  //       planned_well: plannedWellData
  //     });
  //   }
  // }, [dataDrilling])

  // console.log(dataSubmit);

  // const navigate = useNavigate();
  const warnabutton = "teal";
  // console.log(showPengajuanPekerjaan);

  const PengajuanPekerjaanItems = () => {
    const [dataCount, setDataCount] = useState([]);
    
    
    useEffect(() => {
      const getDataPlanning = async () => {
        try {
          const response = await getDataPlanningExploration();
          setDataCount(response);

        } catch (error) {
          console.error("Error get Data Well And Start Date", error);
        }
      }
      getDataPlanning();
    }, []);
    
    
    return (
      <>
        <Text fontSize={"3em"} fontWeight={"bold"} mt={5}>
          Planning Exploration
        </Text>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} mt={5}>
          <CustomCard
            icon={FaClipboardCheck}
            // count={dataCount.length}
            label="Diajukan"
            bgColor="white"
            iconBgColor="#ECF2FE"
            iconColor="#3478ff"
          />
          <CustomCard
            icon={FaTimesCircle}
            // count={dataCount.filter((item) => item.status === "REJECTED").length}
            label="Ditolak"
            bgColor="white"
            iconBgColor="#FEE2E2"
            iconColor="#bd0808"
          />
          <CustomCard
            icon={FaCheckCircle}
            // count={dataCount.filter((item) => item.status === "APPROVED").length}
            label="Disetujui"
            bgColor="white"
            iconBgColor="#E6FFFA"
            iconColor="#00c9a1"
          />
        </SimpleGrid>

        {/* Tombol Tambah Data */}
        <HStack justify="flex-end" mt={4} mb={4}>
          <Button
            colorScheme="blue"
            as={Link}
            to={"/dashboard/planning/planningform"}
          >
            Tambah Data
          </Button>
        </HStack>

        {/* Tabel */}
        <Box>
          <WellTable />
        </Box>
      </>
    );
  };

  return (
    <>
      <Box p={5}>
        <VStack spacing={4} align="stretch">
          {/* Section Cards */}
          {showPengajuanPekerjaan ? <PengajuanPekerjaanItems /> : null}
          <Outlet context={{ sendData }} />

          {showPengajuanPekerjaan ? null : <ShowButtonSubmit />}
        </VStack>
      </Box>
    </>
  );
};

export default PengajuanPekerjaan;
