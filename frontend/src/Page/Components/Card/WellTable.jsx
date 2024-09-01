import { Box, Button, Badge, IconButton } from "@chakra-ui/react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { EditIcon, DeleteIcon, ViewIcon } from "@chakra-ui/icons";
import "./../../../assets/css/ag-grid-theme-builder.css";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { FaInfoCircle } from "react-icons/fa";
import { AllEnums, getDataPlanningExploration } from "../../API/AllEnums";
import { useEffect, useState } from "react";
// Komponen StatusBadge
function StatusBadge({ value }) {
  let colorScheme = "gray";

  if (value === "APPROVED") {
    colorScheme = "green";
  } else if (value === "REJECTED") {
    colorScheme = "yellow";
  } else if (value === "SUSPENDED") {
    colorScheme = "orange";
  }

  return (
    <Badge
      colorScheme={colorScheme}
      whiteSpace={"normal"}
      lineHeight={"1.2"}
      padding={"6px 8px"}
      borderRadius={"6px"}
      width={150}
      fontSize={"14px"}
      textAlign={"center"}
      variant="solid"
    >
      {value}
    </Badge>
  );
}

StatusBadge.propTypes = {
  value: PropTypes.string.isRequired,
};

const ButtonInfo = ({ value }) => {
  return (
    <IconButton
      colorScheme="blue"
      mb={2}
      icon={<FaInfoCircle size={"20px"} />}
    />
  );
};
// Komponen ActionButtons
function ActionButtons({ id }) {
  return (
    <Box display="flex" gap="2">
      <Button
        leftIcon={<EditIcon />}
        colorScheme="blue"
        width={"80px"}
        variant="solid"
      >
        Edit
      </Button>
      <Button leftIcon={<DeleteIcon />} colorScheme="red" width={"80px"}>
        Delete
      </Button>
      <Button
        as={Link}
        width={"90px"}
        height={"40px"} // Gunakan Link dari react-router-dom
        to={`/viewplanning/${id}/`}
        leftIcon={<ViewIcon />}
        colorScheme="green"
        size="sm"
      >
        View
      </Button>
    </Box>
  );
}

ActionButtons.propTypes = {
  id: PropTypes.number.isRequired, // Prop untuk id
};

// Komponen WellTable
const WellTable = () => {
  const columnDefs = [
    {
      headerName: "Info",
      field: "info",
      cellRenderer: ButtonInfo,
      flex :1,
      cellStyle: {
        fontSize: "18px",
      },
    },
    {
      headerName: "Nama Sumur",
      field: "well_name",
      filter: "agTextColumnFilter",
      cellStyle: {
        fontSize: "18px",
      },
      flex:3 // Default width for this column
    },
    {
      headerName: "Tanggal Mulai",
      field: "job_start_date",
      filter: "agDateColumnFilter",
      cellStyle: {
        fontSize: "18px",
      },
      flex:2 // Default width for this column
    },
    {
      headerName: "Tanggal Akhir",
      field: "job_end_date",
      filter: "agDateColumnFilter",
      cellStyle: {
        fontSize: "18px",
      },
      flex:2 // Default width for this column
    },
    {
      headerName: "Tanggal Pengajuan",
      field: "plan_date_proposed",
      filter: "agDateColumnFilter",
      cellStyle: {
        fontSize: "18px",
      },
      flex:2 // Default width for this column
    },
    {
      headerName: "Status",
      field: "plan_status",
      filter: "agTextColumnFilter",
      flex:2,
      cellRenderer: StatusBadge,
      cellStyle: { overflow: "visible" },
    },
    {
      headerName: "Aksi",
      field: "job_plan_id",
      cellRenderer: (params) => <ActionButtons id={params.value} />,
      width: 300, // Default width for this column
    },
  ];
  const [data, setData] = useState([]);
  
  
  useEffect(() => {
    const CombinedData = async () => {
      try {
        const result = await getDataPlanningExploration();

        return setData(result);
      } catch (error) {
        console.log(error);
      }
    };

    CombinedData();
  }, []);

  const rowData = [
    {
      info: 1,
      namaSumur: "WELL000",
      tanggalMulai: "2024-08-01 08:00",
      status: "SUSPENDED",
      id: "8fcf592a-e579-49ce-898c-9a3a9d08a51b", // id yang sesuai untuk tiap item
    },
    {
      info: 2,
      namaSumur: "WELL011",
      tanggalMulai: "2024-08-02 09:00",
      status: "SUSPENDED",
      id: "85e089d0-e4cc-4471-bc9e-5ba095d6be40",
    },
    {
      info: 3,
      namaSumur: "WELL022",
      tanggalMulai: "2024-08-03 07:30",
      status: "APPROVED",
      id: "a6eb7c4f-7b2a-4a98-9882-03f1f909c0bd",
    },
    {
      info: 4,
      namaSumur: "WELL033",
      tanggalMulai: "2024-08-04 10:00",
      status: "APPROVED",
      id: "62cd785a-e50a-4e7a-a832-a29a6db88ae3",
    },
    {
      info: 5,
      namaSumur: "WELL010",
      tanggalMulai: "2024-08-05 11:00",
      status: "REJECTED",
      id: "c985f999-fc41-4a8f-85cd-5be332b32444",
    },
  ];

  return (
    <Box
      className="ag-theme-alpine"
      style={{ height: 400, width: "100%" }}
      shadow={"md"}
      rounded={"2xl"}
      p={2}
    >
      <AgGridReact
        columnDefs={columnDefs}
        rowData={data}
        defaultColDef={{
          flex: 0,
          minWidth: 100,
          filter: false,
          sortable: true,
          resizable: true, 
        }}
      />
    </Box>
  );
};

export default WellTable;
