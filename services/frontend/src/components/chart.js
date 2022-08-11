import * as React from "react";
import { Line } from "react-chartjs-2";
import {CategoryScale} from 'chart.js';
import Chart from 'chart.js/auto';
Chart.register(CategoryScale);

/*
    Order Line Chart Element by Date
 */
function OrdersChart (props) {
    const lineChartData = {
    labels: props.labels,
    datasets: [
      {
        data: props.data,
        label: "Orders",
        borderColor: "black",
        fill: true,
        lineTension: 0.5
      }
    ]
  };

  return (
    <Line
      type="line"
      width={160}
      height={60}
      options={{
        title: {
          display: true,
          text: "Orders",
          fontSize: 20
        },
        legend: {
          display: true,
          position: "top"
        }
      }}
      data={lineChartData}
    />)
}

export default OrdersChart