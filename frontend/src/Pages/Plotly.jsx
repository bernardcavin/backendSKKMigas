import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const Plot3D = () => {
  const [plotData, setPlotData] = useState(null);

  useEffect(() => {
    const fetchPlotData = async () => {
      try {
        const response = await fetch('http://localhost:8000/plot3d-data');
        const data = await response.json();
        setPlotData(data);
      } catch (error) {
        console.error('Error fetching plot data:', error);
      }
    };

    fetchPlotData();
  }, []);

  if (!plotData) {
    return <div>Loading plot...</div>;
  }

  return (
    <div>
      <h1>3D Plot with Plotly</h1>
      <Plot
        data={plotData.data}
        layout={plotData.layout}
        config={{ responsive: true }}
        style={{ width: "100%", height: "600px" }}
      />
    </div>
  );
};

export default Plot3D;