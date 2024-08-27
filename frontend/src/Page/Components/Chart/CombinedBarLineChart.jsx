import React from "react";
import Plot from "react-plotly.js";
import { cumulativeData, monthlyData } from "../data"; // Import your data from a separate file

const CombinedBarLineChart = () => {
  return (
    <Plot
      data={[
        {
          x: monthlyData.map((item) => item.month),
          y: monthlyData.map((item) => item.planning),
          type: "bar",
          name: "Perencanaan",
          marker: { color: "#3182CE" },
          text: monthlyData.map((item) => item.planning),
          textposition: "outside",
          yaxis: "y1",
        },
        {
          x: monthlyData.map((item) => item.month),
          y: cumulativeData(monthlyData.map((item) => item.planning)),
          type: "scatter",
          mode: "lines+markers",
          name: "Kumulatif Perencanaan",
          line: { color: "#3182CE", width: 2 },
          marker: { color: "#3182CE" },
          yaxis: "y2",
        },
      ]}
      layout={{
        width: "1100",
        title: "",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        barmode: "group",
        xaxis: { automargin: true },
        yaxis: {
          title: "Jumlah",
          side: "left",
          automargin: true,
          showgrid: true,
          zeroline: true,
        },
        yaxis2: {
          title: "Jumlah Kumulatif",
          overlaying: "y",
          side: "right",
          automargin: true,
          showgrid: false,
          zeroline: false,
        },
        showlegend: true,
        legend: { orientation: "h", y: -0.2 },
      }}
      config={{ responsive: true }}
      useResizeHandler={true}
      style={{ width: "100%", height: "100%" }}
    />
  );
};

export default CombinedBarLineChart;
