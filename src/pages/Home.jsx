import React from "react";

import Header from "../components/header";
import BigSlider from "../components/bigslider";
import GridCategory from "../components/GridCategory";
import "./Home.css"

export default function Home() {
  return (
    <div className="home-container">
      <Header />
      <BigSlider />
      <GridCategory />
    </div>
  );
}
