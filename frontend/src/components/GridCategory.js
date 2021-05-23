import React from "react";

import OneCategory from "./OneCategory";
import "./GridCategory.css"

export default function GridCategory() {
  // let [categories, setCategories] = React.useState([]);
  const categories = [{'imdb':"TOP IMDB"},{'action':"HÀNH ĐỘNG"},{'romance':"LÃNG MẠN"},{'drama':"KỊCH TÍNH"}];
  return (
      <ul className="#content">
        {categories.map((item) => (
          <li>
            <OneCategory genre={item}/>
          </li>
        ))}
      </ul>
  );
}
