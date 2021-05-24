import Header from "../components/header"
import "./Genre.css";
import React from "react";
import { Bar, Doughnut } from "react-chartjs-2";
import { useEffect } from "react";
import axios from "axios";
import config from "../config/config";
import { useState } from "react";
import "./Stat.css";

export default function Stat(props) {
  const [yearStat, setYearStat] = useState({
    labels: [],
    data: []
  });
  const [genreStat, setGenreStat] = useState({
    labels: [],
    data: []
  });

  useEffect(() => {
    async function fetch() {
      try {
        const res = await axios.get(`${config.SERVER_URI}`+"/statistic");
        if (res && res.status === 200) {
          setYearStat(res.data.statisticYear)
          setGenreStat(res.data.statisticGenres)
        }
      }
      catch(e) {
        console.error(e);
      }
    }
    fetch()
  }, []);

  const MAX = genreStat.data.reduce((res, curr) => res + curr, 0);

  const ylabels = yearStat.labels.map((item, index, labels) => {
    if (index === 0) {
      return "Trước " + item;
    }
    return labels[index-1] + "-" + labels[index];
  });

  // const randomColors = randomColor({
  //   count: 6,//genreStat.labels.length
  //   hue: 'green'
  // })

  // console.log(randomColors)
  let startColor = 255;
  const randomColors = genreStat.labels.map((item, index) => {
    startColor -= 20;
    return `rgba(${startColor}, ${255 - startColor}, 0, 1)`;
  })
  const randomBColors = genreStat.labels.map((item, index) => {
    startColor -= 30;
    return `rgba(20, ${startColor}, ${255 - startColor}, 1)`;
  })
  console.debug("Random"+JSON.stringify(randomColors));

  const sData = {
    labels: [...genreStat.labels],
    datasets: [
      {
        label: 'Tỉ lệ phim',
        data: genreStat.data.map(e => e/MAX),
        backgroundColor: randomColors,
        // borderColor: randomBColors,
        // borderColor: [
        //   'rgba(255, 99, 132, 1)',
        //   'rgba(54, 162, 235, 1)',
        //   'rgba(255, 206, 86, 1)',
        //   'rgba(75, 192, 192, 1)',
        //   'rgba(153, 102, 255, 1)',
        //   'rgba(255, 159, 64, 1)',
        // ],
        borderWidth: 1,
      },
    ],
  };

  return(
    <div className="container-films">
      <Header />
      <div style={{marginTop:"100px"}}></div>
      <div className="stat-container">
        <div>
          <h6 style={{color: "white"}}>
            Thống kê số lượng phim theo khoảng thời gian
          </h6>
          <Bar
            data={{
              labels: ylabels,
              datasets: [
                {
                  label: "Khoảng thời gian",
                  backgroundColor: ["lightBlue"
                  //   "#3e95cd",
                  //   "#8e5ea2",
                  //   "#3cba9f",
                  //   "#e8c3b9",
                  //   "#c45850"
                  ],
                  data: [...yearStat.data]
                }
              ]
            }}
            options={{
              legend: { display: true },
              title: {
                color: "white",
                display: true,
                text: "Thống kê phim"
              }
            }}
          />
        </div>
      </div>
      <div className="stat-container">
        <h6 style={{color: "white", marginTop: "50px"}}>
          Thống kê tỉ lệ phim theo thể loại
        </h6>
        <Doughnut data={sData} />
      </div>
    </div>
  )
}