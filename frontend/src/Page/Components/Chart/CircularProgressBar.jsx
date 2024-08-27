import React from "react";
import { Box, CircularProgress, CircularProgressLabel, Text } from "@chakra-ui/react";
import PropTypes from "prop-types";

const CircularProgressBar = ({ label, value, color }) => {
  return (
    <Box textAlign="center">
      <CircularProgress value={value} color={color} size="120px">
        <CircularProgressLabel fontSize="xl">{value}%</CircularProgressLabel>
      </CircularProgress>
      <Text mt={2} fontSize="xl">
        {label}
      </Text>
    </Box>
  );
};

CircularProgressBar.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  color: PropTypes.string.isRequired,
};

export default CircularProgressBar;
