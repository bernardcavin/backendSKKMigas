import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const Plotly = () => {
  const [plotData, setPlotData] = useState(null);
  const [layout, setLayout] = useState(null);
  const [totalCounts, setTotalCounts] = useState(null);
  const [currentMonthCounts, setCurrentMonthCounts] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('token');
        console.log(token+'ini token '); // Atau dapatkan token dari state management Anda
        const response = await fetch('http://localhost:8000/dashboard/count-jobs-month', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setPlotData(data.PLOT_DATA.data);
        setLayout(data.PLOT_DATA.layout);
        setTotalCounts(data.TOTAL);
        setCurrentMonthCounts(data.CURRENT_MONTH);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load data. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!plotData || !layout) {
    return <div>No data available</div>;
  }

  return (
    <div>
      <h2>Job Count Summary</h2>
      <div>
        <h3>Total Counts</h3>
        <p>Drilling Exploration: {totalCounts.DRILLING.EXPLORATION}</p>
        <p>Drilling Development: {totalCounts.DRILLING.DEVELOPMENT}</p>
        <p>WOWS Workover: {totalCounts.WOWS.WORKOVER}</p>
        <p>WOWS Well Service: {totalCounts.WOWS.WELLSERVICE}</p>
      </div>
      <div>
        <h3>Current Month Counts</h3>
        <p>Drilling Exploration: {currentMonthCounts.DRILLING.EXPLORATION}</p>
        <p>Drilling Development: {currentMonthCounts.DRILLING.DEVELOPMENT}</p>
        <p>WOWS Workover: {currentMonthCounts.WOWS.WORKOVER}</p>
        <p>WOWS Well Service: {currentMonthCounts.WOWS.WELLSERVICE}</p>
      </div>
      <Plot
        data={plotData}
        layout={{...layout, width: 900, height: 500}}
        config={{responsive: true}}
      />
    </div>
  );
};

export default Plotly;