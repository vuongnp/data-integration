import React from "react";
import OneCategory from "./OneCategory";
import "./GridCategory.css"

export default function GridCategory() {
  const categories = [{'action':"HÀNH ĐỘNG"},{'kid':"TRẺ EM"},{'drama':"KỊCH TÍNH"}];
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
