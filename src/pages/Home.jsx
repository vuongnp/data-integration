import React from "react";

import Header from "../components/header";
import BigSlider from "../components/bigslider";
import GridCategory from "../components/GridCategory";
import "./Home.css"

export default function Home(props) {
    // console.log(props)
  return (
    <div className="home-container">
      <Header props={props}/>
      <BigSlider />
      <GridCategory />
    </div>
  );
}
