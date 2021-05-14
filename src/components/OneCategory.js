import React, { useState, useEffect }from "react";
import { Link } from "react-router-dom";
import { IconButton } from "@material-ui/core";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import SliderFilmItem from "./SliderFilmItem";
import "./OneCategory.css";
import axios from 'axios';

export default function OneCategory(props) {
  let [films, setFilms] = React.useState([
      { id: "1", name: "AAAA" },
      { id: "2", name: "BBB" },
      { id: "1", name: "AAAA" },
      { id: "2", name: "BBB" },
      { id: "1", name: "AAAA" },
      { id: "2", name: "BBB" },
      { id: "1", name: "AAAA" },
      { id: "2", name: "BBB" },
      { id: "1", name: "AAAA" },
      { id: "2", name: "BBB" },
      { id: "1", name: "AAAA" },
      { id: "2", name: "BBB" },
    ]);
  let nameCategory = Object.keys(props.genre)[0];
  useEffect(async () => {
    const result = await axios(
      'https://data-intergration.herokuapp.com/category?text='+nameCategory,
    );
 
    setFilms(result.data);
  },[]);
  const ref = React.useRef(null);
  const scroll = (scrollOffset) => {
    ref.current.scrollLeft += scrollOffset;
  };
  return (
    <div className="one-category">
      <Link to={`/genre/${Object.keys(props.genre)[0]}`} className="title">
        {Object.values(props.genre)[0]}
      </Link>
      <div className="main-content">
        <IconButton aria-label="croll-left" onClick={() => scroll(-1250)}>
          <ChevronLeftIcon color="action" />
        </IconButton>
        <div className="list-items" ref={ref}>
          {(films.slice(0,30)).map((item, index) => (
            <SliderFilmItem key={index} item={item}/>
          ))}
        </div>
        <IconButton aria-label="croll-right" onClick={() => scroll(+1250)}>
          <ChevronRightIcon color="action" />
        </IconButton>
      </div>
    </div>
  );
}
