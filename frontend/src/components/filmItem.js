import React from "react";
import Slide1 from "../assert/slide1.jpg";
import "./filmItem.css";

export default function FilmItem(props) {
  const listlinks = props.item.urls;
  const getNamePage=(link)=>{
    let list = link.split('/');
    if (list.length ==1){
      return "###"
    }
    let domain = (list[2]).split('.')[1];
    return domain
  }
  return (
    // <ListGroup.Item>
    <div className="one-item">
      <div className="left-item">
        <img src={props.item.image}></img>
        <p>{props.item.title}</p>
      </div>
      <div className="right-item">
        <span className="imdb-score">IMDB {props.item.rating}</span>
        {listlinks &&
          listlinks.map((link) => (
            <div>
              <a href={link}>{getNamePage(link)}</a>
            </div>
          ))}
      </div>
    </div>
    // </ListGroup.Item>
  );
}
