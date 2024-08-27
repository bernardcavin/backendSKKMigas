// eslint-disable-next-line no-unused-vars
import React from "react";
import { Box, Icon, Text } from "@chakra-ui/react";
import PropTypes from 'prop-types';

// Komponen CustomCard
const CustomCard = ({ icon, count, label, bgColor, iconColor, iconBgColor }) => {
  return (
    <Box
      p={6}
      bg={bgColor}
      color="black"
      borderRadius="2xl"
      boxShadow="md"
      display="flex"
      alignItems="center"
      gap={4}
    >
      <Box
        w="80px"
        h="80px"
        bg={iconBgColor}
        borderRadius="17px"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <Icon as={icon} boxSize={8} color={iconColor} />
      </Box>
      <Box>
        <Text fontSize="35px" fontWeight="bold">
          {count}
        </Text>
        <Text fontSize="23px" fontWeight="normal">
          {label}
        </Text>
      </Box>
    </Box>
  );
};

CustomCard.propTypes = {
  icon: PropTypes.elementType.isRequired, // Menggunakan elementType untuk Chakra UI icon
  count: PropTypes.number.isRequired,
  label: PropTypes.string.isRequired,
  bgColor: PropTypes.string.isRequired,
  iconColor: PropTypes.string.isRequired,
  iconBgColor: PropTypes.string.isRequired,
};

export default CustomCard;
