import React from "react";
import Slide1 from "../assert/slide1.jpg";
import "./filmItem.css";

export default function FilmItem(props) {
  const listlinks = props.item.links;
  return (
    // <ListGroup.Item>
    <div className="one-item">
      <div className="left-item">
        <img src={props.item.image}></img>
        <p>{props.item.name}</p>
      </div>
      <div className="right-item">
        <span className="imdb-score">IMDB {props.item.imdb}</span>
        {listlinks &&
          listlinks.map((link) => (
            <div>
              <a href={link}>Link {listlinks.indexOf(link) + 1}</a>
            </div>
          ))}
      </div>
    </div>
    // </ListGroup.Item>
  );
}
