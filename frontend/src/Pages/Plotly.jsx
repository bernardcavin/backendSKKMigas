import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import './JobCountChart.css';

const JobCountChart = () => {
  const [barChartData, setBarChartData] = useState(null);
  const [pieChartData, setPieChartData] = useState(null);
  const [lineChartData, setLineChartData] = useState(null);
  const [barLayout, setBarLayout] = useState(null);
  const [pieLayout, setPieLayout] = useState(null);
  const [lineLayout, setLineLayout] = useState(null);
  const [totalCounts, setTotalCounts] = useState(null);
  const [currentMonthCounts, setCurrentMonthCounts] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch('http://localhost:8000/dashboard/count-jobs-month', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        processData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load data. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const processData = (data) => {
    setTotalCounts(data.TOTAL);
    setCurrentMonthCounts(data.CURRENT_MONTH);

    // Bar Chart Data
    const barData = data.PLOT_DATA.data.map(series => ({
      ...series,
      type: 'bar',
    }));
    setBarChartData(barData);

    // Pie Chart Data
    const pieData = [{
      values: [
        data.TOTAL.DRILLING.EXPLORATION,
        data.TOTAL.DRILLING.DEVELOPMENT,
        data.TOTAL.WOWS.WORKOVER,
        data.TOTAL.WOWS.WELLSERVICE
      ],
      labels: ['Drilling Exploration', 'Drilling Development', 'WOWS Workover', 'WOWS Well Service'],
      type: 'pie',
      hole: 0.4,
      textinfo: 'label+percent',
      insidetextorientation: 'radial'
    }];
    setPieChartData(pieData);

    // Line Chart Data
    const months = data.PLOT_DATA.data[0].x;
    const lineData = [
      {
        x: months,
        y: data.PLOT_DATA.data[0].y,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Drilling'
      },
      {
        x: months,
        y: data.PLOT_DATA.data[1].y,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'WOWS'
      }
    ];
    setLineChartData(lineData);

    // Layouts
    setBarLayout({
      title: 'Monthly Job Counts',
      barmode: 'group',
      bargap: 0.15,
      bargroupgap: 0.1,
      xaxis: { title: 'Month' },
      yaxis: { title: 'Number of Jobs' }
    });

    setPieLayout({
      title: 'Total Job Distribution',
      height: 400,
      width: 500,
    });

    setLineLayout({
      title: 'Job Trends Over Time',
      xaxis: { title: 'Month' },
      yaxis: { title: 'Number of Jobs' }
    });
  };

  if (isLoading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!barChartData || !pieChartData || !lineChartData) return <div>No data available</div>;

  return (
    <div className="job-count-chart">
      <h2 className="main-title">Job Count Summary</h2>
      <div className="summary-container">
        <div className="summary-box">
          <h3>Total Counts</h3>
          <p>Drilling Exploration: {totalCounts?.DRILLING.EXPLORATION}</p>
          <p>Drilling Development: {totalCounts?.DRILLING.DEVELOPMENT}</p>
          <p>WOWS Workover: {totalCounts?.WOWS.WORKOVER}</p>
          <p>WOWS Well Service: {totalCounts?.WOWS.WELLSERVICE}</p>
        </div>
        <div className="summary-box">
          <h3>Current Month Counts</h3>
          <p>Drilling Exploration: {currentMonthCounts?.DRILLING.EXPLORATION}</p>
          <p>Drilling Development: {currentMonthCounts?.DRILLING.DEVELOPMENT}</p>
          <p>WOWS Workover: {currentMonthCounts?.WOWS.WORKOVER}</p>
          <p>WOWS Well Service: {currentMonthCounts?.WOWS.WELLSERVICE}</p>
        </div>
      </div>
      <div className="charts-container">
        <div className="chart-box">
          <Plot
            data={barChartData}
            layout={barLayout}
            config={{ responsive: true }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
        <div className="chart-box">
          <Plot
            data={pieChartData}
            layout={pieLayout}
            config={{ responsive: true }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
        <div className="chart-box full-width">
          <Plot
            data={lineChartData}
            layout={lineLayout}
            config={{ responsive: true }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      </div>
    </div>
  );
};

export default JobCountChart;