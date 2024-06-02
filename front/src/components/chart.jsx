import React, { useEffect, useState } from "react";
import ApexChart from "react-apexcharts";

const Chart = () => {
  const [chartdata, setChartdata] = useState([]);
  const [loading, setLoading] = useState(true);
  const getChartdata = async () => {
    const json = await (
      await fetch("http://127.0.0.1:8000/nasdaq_chart")
    ).json();
    setChartdata(json);
    setLoading(false);
  };
  useEffect(() => {
    getChartdata();
  }, []);
  return (
    <div>
      {loading ? (
        <h1>로딩중...</h1>
      ) : (
        <ApexChart
          type="candlestick"
          height="500"
          series={[
            {
              data: chartdata.map((item) => {
                return [
                  item.date,
                  Number(item.stock_high_price.split(",").join("")),
                  Number(item.stock_low_price.split(",").join("")),
                  Number(item.stock_market_price.split(",").join("")),
                  Number(item.stock_closing_price.split(",").join("")),
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
              labels: {
                show: true,
                datetimeFormatter: {
                  day: "yyyy.MM.dd",
                },
              },
              axisTicks: { show: true },
              axisBorder: { show: true },
              type: "datetime",
            },
          }}
        ></ApexChart>
      )}
    </div>
  );
};

export default Chart;
