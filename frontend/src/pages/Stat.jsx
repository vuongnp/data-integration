import Header from "../components/header"
import "./Genre.css";
import React from "react";
import { Bar, Doughnut, Line } from "react-chartjs-2";
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
  const [urlStat, setUrlStat] = useState({
    labels: [],
    data: []
  });
  const [ratingStat, setRating] = useState({
    labels: [],
    data: []
  });

  useEffect(() => {
    async function fetch() {
      try {
        const res = await axios.get(`${config.SERVER_URI}`+"/statistic");
        if (res && res.status === 200) {
          setYearStat(res.data.statisticYear);
          setGenreStat(res.data.statisticGenres);
          setUrlStat(res.data.statisticNumUrls);
          setRating(res.data.statisticAvgRating);
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
  // const randomColors = genreStat.labels.map((item, index) => {
  //   startColor -= 20;
  //   return `rgba(${startColor}, ${255 - startColor}, 1, 0.8)`;
  // })
  // const randomBColors = genreStat.labels.map((item, index) => {
  //   startColor -= 30;
  //   return `rgba(-20, ${startColor}, ${255 - startColor}, 0.8)`;
  // })
  const randomColors = [
    "FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF", "000000", 
    "800000", "008000", "000080", "808000", "800080", "008080", "808080", 
    "C00000", "00C000", "0000C0", "C0C000", "C000C0", "00C0C0", "C0C0C0", 
    "400000", "004000", "000040", "404000", "400040", "004040", "404040", 
    "200000", "002000", "000020", "202000", "200020", "002020", "202020", 
    "600000", "006000", "000060", "606000", "600060", "006060", "606060", 
    "A00000", "00A000", "0000A0", "A0A000", "A000A0", "00A0A0", "A0A0A0", 
    "E00000", "00E000", "0000E0", "E0E000", "E000E0", "00E0E0", "E0E0E0", 
  ];
  const randomHex = randomColors.map((c) => "#" + c);
  function hexToRgbA(hex){
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',1)';
    }
    throw new Error('Bad Hex');
  
  }
  // console.debug("Random"+JSON.stringify(randomColors));

  const sData = {
    labels: [...genreStat.labels],
    datasets: [
      {
        label: 'Tỉ lệ phim',
        data: genreStat.data.map(e => e/MAX),
        backgroundColor: randomColors.map(c => hexToRgbA("#"+c)),
        // borderColor: randomBColors,
        // borderColor: [
        //   'rgba(255, 99, 132, 1)',
        //   'rgba(54, 162, 235, 1)',
        //   'rgba(255, 206, 86, 1)',
        //   'rgba(75, 192, 192, 1)',
        //   'rgba(153, 102, 255, 1)',
        //   'rgba(255, 159, 64, 1)',
        // ],
        borderWidth: 2,
      },
    ],
    responsive: true,
    maintainAspectRatio: false
  };

  return(
    <div className="container-stat">
      <Header />
      <div style={{marginTop:"100px"}}></div>
      <div className="stat-container">
        <div>
          <h3 style={{color: "black"}}>
            Thống kê số lượng phim theo khoảng thời gian
          </h3>
          <Line
            data={{
              labels: ylabels,
              datasets: [
                {
                  label: "Khoảng thời gian",
                  backgroundColor: ["#8e5ea2"
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
                color: "black",
                display: true,
                text: "Thống kê phim"
              }
            }}
          />
        </div>
      </div>
      <div className="stat-container">
        <h3 style={{color: "black", marginTop: "70px"}}>
          Thống kê tỉ lệ phim theo thể loại
        </h3>
        <Doughnut data={sData} />
      </div>
      <div style={{marginBottom:"100px"}}></div>
      <div className="stat-container">
        <h3 style={{color: "black"}}>
          Thống kê điểm IMDB theo thể loại
        </h3>
        <Bar
          data={{
            labels: ratingStat.labels,
            datasets: [
              {
                label: "Điểm",
                // backgroundColor: ["#89ff89"
                // //   "#3e95cd",
                // //   "#8e5ea2",
                // //   "#3cba9f",
                // //   "#e8c3b9",
                // //   "#c45850"
                // ],
                backgroundColor: randomHex,
                data: [...ratingStat.data]
              }
            ]
          }}
          options={{
            legend: { display: true },
            title: {
              color: "black",
              display: true,
              text: "Thống kê phim"
            }
          }}
        />
      </div>
      <div style={{marginBottom:"100px"}}></div>
      <div className="stat-container-scale">
        <h3 style={{color: "black"}}>
          Thống kê số lượng phim theo số nguồn
        </h3>
        <Bar
          data={{
            labels: [...urlStat.labels].slice().splice(1, urlStat.labels.length),
            datasets: [
              {
                label: "Số lượng",
                backgroundColor: ["#ffe4b2"
                //   "#3e95cd",
                //   "#8e5ea2",
                //   "#3cba9f",
                //   "#e8c3b9",
                //   "#c45850"
                ],
                data: [...urlStat.data].slice().splice(1, urlStat.data.length)
              }
            ]
          }}
          options={{
            indexAxis: 'y',
            legend: { display: true },
            title: {
              color: "black",
              display: true,
              text: "Thống kê phim"
            }
          }}
        />
      </div>
      <div style={{marginBottom:"100px"}}></div>
    </div>
  )
}