import React from 'react';
import { Bar } from 'react-chartjs-2';

const BarChart = ({ data, options }) => {
  const chartOptions = {
    ...options,
    animation: {
      duration: 1500, // Durasi animasi lebih lama
      easing: 'easeOutBounce', // Tipe easing untuk animasi
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          display: false, // Sembunyikan gridlines vertikal
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(200, 200, 200, 0.2)', // Ubah warna gridlines horizontal
        },
      },
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 14,
            family: 'Arial',
          },
          color: '#333', // Warna teks label
        },
      },
      title: {
        display: true,
        text: 'Monthly Job Counts',
        font: {
          size: 18,
        },
        color: '#333', // Warna judul
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.7)', // Warna background tooltip
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 12,
        },
        borderColor: '#fff',
        borderWidth: 1,
      },
    },
  };

  const chartData = {
    ...data,
    datasets: data.datasets.map((dataset, index) => ({
      ...dataset,
      backgroundColor: [
        `rgba(255, 99, 132, 0.6)`,
        `rgba(54, 162, 235, 0.6)`,
        `rgba(255, 206, 86, 0.6)`,
        `rgba(75, 192, 192, 0.6)`,
        `rgba(153, 102, 255, 0.6)`,
        `rgba(255, 159, 64, 0.6)`,
      ][index % 6], // Ubah warna bar
      borderColor: [
        `rgba(255, 99, 132, 1)`,
        `rgba(54, 162, 235, 1)`,
        `rgba(255, 206, 86, 1)`,
        `rgba(75, 192, 192, 1)`,
        `rgba(153, 102, 255, 1)`,
        `rgba(255, 159, 64, 1)`,
      ][index % 6],
      borderWidth: 2, // Lebih tebal border bar
      hoverBackgroundColor: [
        `rgba(255, 99, 132, 0.8)`,
        `rgba(54, 162, 235, 0.8)`,
        `rgba(255, 206, 86, 0.8)`,
        `rgba(75, 192, 192, 0.8)`,
        `rgba(153, 102, 255, 0.8)`,
        `rgba(255, 159, 64, 0.8)`,
      ][index % 6],
    })),
  };

  return <Bar data={chartData} options={chartOptions} />;
};

export default BarChart;
