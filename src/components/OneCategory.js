import React from "react";
import { Link } from "react-router-dom";
import { ListGroup, Button } from "react-bootstrap";
import { IconButton } from "@material-ui/core";
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import SliderItem from "./SliderItem";
import "./OneCategory.css";

export default function OneCategory(genre) {
  const films = [
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
  ];
  const ref = React.useRef(null);
  const scroll = (scrollOffset) => {
    ref.current.scrollLeft += scrollOffset;
  };
  return (
    <div className="one-category">
      <Link to="/genre" className="title">HÀNH ĐỘNG</Link>
      <div className="main-content">
        <IconButton aria-label="croll-left" onClick={() => scroll(-1250)}>
          <ChevronLeftIcon color="action" />
        </IconButton>
        <div className="list-items" ref={ref}>
          {films.map((item, index) => (
            <SliderItem key={index} name={item.name} />
          ))}
        </div>
        <IconButton aria-label="croll-right" onClick={() => scroll(+1250)}>
          <ChevronRightIcon  color="action"/>
        </IconButton>
      </div>
    </div>
  );
}
