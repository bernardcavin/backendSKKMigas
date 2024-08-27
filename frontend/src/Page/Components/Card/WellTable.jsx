import { Box, Button, Badge } from "@chakra-ui/react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { EditIcon, DeleteIcon, ViewIcon } from "@chakra-ui/icons";
import "./../../../assets/css/ag-grid-theme-builder.css";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

// Komponen StatusBadge
function StatusBadge({ value }) {
  let colorScheme = "gray";

  if (value === "Clear") {
    colorScheme = "green";
  } else if (value ===  "Suspended") {
    colorScheme = "yellow";
  } else if (value ===  "Pending") {
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
      <Button leftIcon={<DeleteIcon />} colorScheme="red"width={"80px"}  >
        Delete
      </Button>
      <Button
        as={Link} 
        width={"90px"}
        height={"40px"}// Gunakan Link dari react-router-dom
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
      headerName: "No",
      field: "no",
      width: 0,
      filter: "agNumberColumnFilter",
      cellStyle: {
        fontSize:'18px'
      }
      
    },
    {
      headerName: "Nama Sumur",
      field: "namaSumur",
      filter: "agTextColumnFilter",
      cellStyle: {
        fontSize:'18px'
      }
    },
    {
      headerName: "Tanggal & Mulai",
      field: "tanggalMulai",
      filter: "agDateColumnFilter",
      cellStyle: {
        fontSize:'18px'
      }
    },
    {
      headerName: "Status",
      field: "status",
      filter: "agTextColumnFilter",
      width: 150, // Atur lebar kolom agar cukup untuk badge
      cellRenderer: StatusBadge,
      cellStyle: { overflow: "visible" }, // Pastikan overflow visible
    },
    {
      headerName: "Aksi",
      field: "id", // Kolom id untuk diteruskan ke ActionButtons
      cellRenderer: (params) => <ActionButtons id={params.value} />, 
      // Kirim id ke ActionButtons
      // cellRenderer: ActionButtons,
    },
  ];

  const rowData = [
    {
      no: 1,
      namaSumur: "WELL000",
      tanggalMulai: "2024-08-01 08:00",
      status: "Suspended",
        id: "8fcf592a-e579-49ce-898c-9a3a9d08a51b", // id yang sesuai untuk tiap item
    },
    {
      no: 2,
      namaSumur: "WELL011",
      tanggalMulai: "2024-08-02 09:00",
      status: "Suspended",
      id: "85e089d0-e4cc-4471-bc9e-5ba095d6be40",
    },
    {
      no: 3,
      namaSumur: "WELL022",
      tanggalMulai: "2024-08-03 07:30",
      status: "Abandoned Junked",
      id: "a6eb7c4f-7b2a-4a98-9882-03f1f909c0bd",
    },
    {
      no: 4,
      namaSumur: "WELL033",
      tanggalMulai: "2024-08-04 10:00",
      status: "Not Drilled",
      id: "62cd785a-e50a-4e7a-a832-a29a6db88ae3",
    },
    {
      no: 5,
      namaSumur: "WELL010",
      tanggalMulai: "2024-08-05 11:00",
      status: "Abandoned Whipstocked",
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
        rowData={rowData}
        defaultColDef={{
          flex: 1,
          minWidth: 100,
          filter: true,
          sortable: true,
        }}
      />
    </Box>
  );
};

export default WellTable;
