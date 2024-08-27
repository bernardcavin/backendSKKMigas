import React from "react";
import { Box, Text, Icon } from "@chakra-ui/react";

const CustomCard = ({ icon, title, value, unit }) => {
  return (
    <Box
      p={4}
      borderWidth="1px"
      borderRadius="lg"
      boxShadow="sm"
      display="flex"
      alignItems="center"
      bg="white"
      minW="200px"
    >
      <Icon as={icon} boxSize={8} mr={4} />
      <Box>
        <Text fontWeight="bold">{title}</Text>
        <Text fontSize="2xl" fontWeight="bold">
          {value} {unit}
        </Text>
      </Box>
    </Box>
  );
};

export default CustomCard;
