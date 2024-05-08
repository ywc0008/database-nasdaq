import React from "react";
import ApexChart from "react-apexcharts";
import data from "../DB.json";

/* const Chart = () => {
  return (
    <div>
      <ul>
        {data.data.map((item, index) => (
          <li key={index}>
            <h1>{item.date}</h1>
            <h2>{item.stock_closing_price}</h2>
            <h2>{item.stock_high_price}</h2>
            <h2>{item.stock_low_price}</h2>
            <h2>{item.stock_market_price}</h2>
            <h2>{item.stock_movement}</h2>
            <h2>{item.stock_trading_volume}</h2>
          </li>
        ))}
      </ul>
    </div>
  );
}; */

const Chart = () => {
  return (
    <ApexChart
      type="candlestick"
      series={[
        {
          data: data.data.map((item) => {
            return [
              item.date,
              item.stock_closing_price,
              item.stock_high_price,
              item.stock_low_price,
              item.stock_market_price,
            ];
          }),
        },
      ]}
      options={{
        theme: { mode: "dark" },
        chart: {
          toolbar: { show: true },
          background: "transparent",
        },
        stroke: { curve: "smooth", width: 1 },
        grid: { show: true },
        yaxis: { show: true },
        xaxis: {
          labels: { show: false },
          axisTicks: { show: false },
          axisBorder: { show: false },
          type: "datetime",
        },
      }}
    ></ApexChart>
  );
};

export default Chart;
