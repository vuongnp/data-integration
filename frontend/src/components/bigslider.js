import React from "react";
import {
  Carousel,
} from "react-bootstrap";
import Slide1 from "../assert/slide1.jpg"
import Slide2 from "../assert/slide2.jpg";
import Slide3 from "../assert/slide3.jpg";
import "./bigslider.css"
export default function BigSlider() {
  return (
    <Carousel className="bigslide">
      <Carousel.Item interval={3000} className="item-slide">
        <img
          className="d-block img-slide"
          src={Slide1}
          alt="First slide"
        />
        {/* <Carousel.Caption>
          <h3>First slide label</h3>
          <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
        </Carousel.Caption> */}
      </Carousel.Item>
      <Carousel.Item interval={3000}  className="item-slide">
        <img
          className="d-block img-slide"
          src={Slide2}
          alt="Second slide"
        />
        {/* <Carousel.Caption>
          <h3>Second slide label</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        </Carousel.Caption> */}
      </Carousel.Item>
      <Carousel.Item  interval={3000}  className="item-slide">
        <img
          className="d-block img-slide"
          src={Slide3}
          alt="Third slide"
        />
        {/* <Carousel.Caption>
          <h3>Third slide label</h3>
          <p>
            Praesent commodo cursus magna, vel scelerisque nisl consectetur.
          </p>
        </Carousel.Caption> */}
      </Carousel.Item>
    </Carousel>
  );
}
