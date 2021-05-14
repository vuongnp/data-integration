import React, { useState, useEffect } from "react";
import { ListGroup, Button } from "react-bootstrap";

import "./SliderFilmItem.css";

export default function SliderFilmItem(props) {
  let [isHovering, serIsHovering] = useState(false);

  return (
    <ListGroup.Item>
      <div
        className="one-film"
        onMouseEnter={() => serIsHovering(true)}
        onMouseLeave={() => serIsHovering(false)}
      >
        <img src={props.item.image} alt=""></img>
        <p>{props.item.name}</p>
        {isHovering && (
          <div class="watch-now">
            <Button
              href={props.item.links[0]}
              className="link-to-watch"
              variant="danger"
            >
              Xem ngay
            </Button>
          </div>
        )}
      </div>
    </ListGroup.Item>
  );
}
