import React from 'react';
import { Line } from 'react-chartjs-2';

const LineChartComponent = ({ data, options }) => {
  
  return <Line data={data} options={options} />;
};

export default LineChartComponent;
