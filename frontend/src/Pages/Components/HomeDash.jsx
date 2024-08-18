import React, { useState, useEffect } from 'react';
import BarChart from './ChartComponets/BarChart';
import PieChart from './ChartComponets/PieChart';
import LineChart from './ChartComponets/LineChart';
import './../JobCountChart.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Typography,
  Select,
  Option,
  Button,
} from "@material-tailwind/react";

const HomeDash = () => {
  const [barChartData, setBarChartData] = useState(null);
  const [pieChartData, setPieChartData] = useState(null);
  const [lineChartData, setLineChartData] = useState(null);
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
    const barData = {
      labels: data.PLOT_DATA.data[0].x,
      datasets: data.PLOT_DATA.data.map((series, index) => ({
        label: series.name,
        data: series.y,
        backgroundColor: `rgba(75, 192, 192, ${0.6 + index * 0.1})`,
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      }))
    };
    setBarChartData(barData);

    // Pie Chart Data
    const pieData = {
      labels: ['Drilling Exploration', 'Drilling Development', 'WOWS Workover', 'WOWS Well Service'],
      datasets: [
        {
          data: [
            data.TOTAL.DRILLING.EXPLORATION,
            data.TOTAL.DRILLING.DEVELOPMENT,
            data.TOTAL.WOWS.WORKOVER,
            data.TOTAL.WOWS.WELLSERVICE
          ],
          backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 1,
        },
      ],
    };
    setPieChartData(pieData);

    // Line Chart Data
    const lineData = {
      labels: data.PLOT_DATA.data[0].x,
      datasets: data.PLOT_DATA.data.map((series, index) => ({
        label: series.name,
        data: series.y,
        fill: false,
        borderColor: `rgba(75, 192, 192, ${1 - index * 0.1})`,
        tension: 0.1,
      }))
    };
    setLineChartData(lineData);
  };

  const chartAnimation = {
    duration: 1000, // Durasi animasi dalam milidetik
    easing: 'easeInOutQuad', // Tipe easing untuk animasi
  };

  if (isLoading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!barChartData || !pieChartData || !lineChartData) return <div>No data available</div>;

  return (
    <div className="card text-center flex-col">
      <Typography variant="h3" color="black" className='mt-10 mb-10'>
      Job Count Summary
        </Typography>
      <div className="charts-container">
        <div className='flex flex-row gap-4 w-full h-1/3'>
        <div className="chart-box w-3/5 p-5">
          <BarChart data={barChartData} options={{ responsive: true, animation: chartAnimation, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Monthly Job Counts' } } }} />
        </div>
        <div className="chart-box w-2/5 p-5">
          <PieChart data={pieChartData} options={{ responsive: true, animation: chartAnimation, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Total Job Distribution' } } }} />
        </div>
        </div>
        <div className="chart-box full-width p-5">
          <LineChart data={lineChartData} options={{ responsive: true, animation: chartAnimation, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Job Trends Over Time' } }, scales: { x: { title: { display: true, text: 'Month' } }, y: { title: { display: true, text: 'Number of Jobs' } } } }} />
        </div>
      </div>
    </div>
  );
}

export default HomeDash;
