import React from "react";
import { Box, Icon, Text } from "@chakra-ui/react";
import PropTypes from "prop-types";

const SummaryBox = ({ icon, value, label, percentage, gradient, iconColor }) => {
  return (
    <Box
      borderRadius="32px"
      padding="32px"
      bgGradient={gradient}
      overflow="hidden"
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="flex-start"
      gap="25px"
      boxShadow="md"
      color="white"
    >
      <Box
        width="57px"
        height="57px"
        padding="10px"
        bg="white"
        borderRadius="17px"
        border="1px solid rgba(255, 255, 255, 0.50)"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        {React.isValidElement(icon) ? (
          <Icon as={icon.type} w={6} h={6} color={iconColor} />
        ) : (
          <Text color="red">Invalid Icon</Text>
        )}
      </Box>
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="flex-end"
        width="100%"
      >
        <Box>
          <Text fontSize="37px" fontWeight="bold">
            {value}
          </Text>
          <Text fontSize="19px" fontWeight="bold">
            {label}
          </Text>
        </Box>
        <Box
          padding="12px 15px"
          bg="rgba(255, 255, 255, 0.35)"
          borderRadius="41px"
          border="1px solid rgba(255, 255, 255, 0.50)"
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          <Text fontSize="19px" fontWeight="bold">
            {percentage}
          </Text>
        </Box>
      </Box>
    </Box>
  );
};

SummaryBox.propTypes = {
  icon: PropTypes.element.isRequired,
  value: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  percentage: PropTypes.string.isRequired,
  gradient: PropTypes.string.isRequired,
  iconColor: PropTypes.string.isRequired,
};

export default SummaryBox;
