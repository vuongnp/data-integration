import React from "react";
import OneCategory from "./OneCategory";
import "./GridCategory.css"

export default function GridCategory() {
  const categories = [1, 2, 3];
  return (
      <ul className="#content">
        {categories.map((item) => (
          <li>
            <OneCategory />
          </li>
        ))}
      </ul>
  );
}
