import React, { useState, useEffect } from "react";
import { ListGroup, Button } from "react-bootstrap";

import "./SliderFilmItem.css";

export default function SliderFilmItem(props) {
  let [isHovering, serIsHovering] = useState(false);
  const getNamePage=(link)=>{
    let list = link.split('/');
    if (list.length ==1){
      return "###"
    }
    let domain = (list[2]).split('.')[1];
    return domain
  }

  return (
    <ListGroup.Item>
      <div
        className="one-film"
        onMouseEnter={() => serIsHovering(true)}
        onMouseLeave={() => serIsHovering(false)}
      >
        <img src={props.item.image} alt=""></img>
        <p>{props.item.title}</p>
        {isHovering && (
          <div className="watch-now">
            <div style={{fontSize: 26, color: "white", fontWeight:"bold"}}>Xem ngay</div>
            {props.item.urls && props.item.urls.map((link) => (
              <div>
                <a href={link}>{getNamePage(link)}</a>
              </div>
            ))}
          </div>
        )}
      </div>
    </ListGroup.Item>
  );
}
