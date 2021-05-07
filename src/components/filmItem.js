import React from "react";
import Slide1 from "../assert/slide1.jpg";
import "./filmItem.css";

export default function FilmItem(props) {
    const links=[1,2,3,4,5,6,7,8]
  return (
    // <ListGroup.Item>
      <div className="one-item">
        <div className="left-item">
          <img src={Slide1}></img>
          <h3>{props.name}</h3>
        </div>
        <div className="right-item">
          {links.map((index,link)=>(
              <div>
              <a href='#'>Link {index}</a>
              </div>
          ))}
        </div>
      </div>
    // </ListGroup.Item>
  );
}
