import React from "react";
import { ListGroup } from "react-bootstrap";
import Slide1 from "../assert/slide1.jpg";
import "./SliderItem.css";

export default function SliderItem(props) {
  return (
    <ListGroup.Item>
      <div className="one-film">
        <img src={Slide1}></img>
        <h2>{props.name}</h2>
      </div>
    </ListGroup.Item>
  );
}
