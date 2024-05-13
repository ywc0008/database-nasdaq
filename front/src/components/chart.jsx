import React, { useEffect, useState } from "react";
import ApexChart from "react-apexcharts";

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
  const [chartdata,setChartdata]=useState([])
  const [loading, setLoading] = useState(true);
  const getChartdata=async()=>{
    const json=await(
      await  fetch("http://127.0.0.1:8000/nasdaq_chart")
    ).json();
    setChartdata(json);
    setLoading(false);
  }
  console.log(chartdata);
  useEffect(()=>{
    getChartdata();
  },[])
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
                item.stock_high_price,
                item.stock_low_price,
                item.stock_closing_price,
                item.stock_market_price,
              ];
            }),
          },
        ]}
        options={{
          theme: { mode: "dark" },
          chart: {
            toolbar: { show: false },
            background: "transparent",
          },
          stroke: { curve: "smooth", width: 1 },
          grid: { show: true },
          yaxis: { show: true },
          xaxis: {
            labels: {
              show: true,
              datetimeFormatter: {
                day: 'yyyy.MM.dd',
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
  )
};

export default Chart;
