import React from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";

import Header from "../components/header";
import "./Genre.css";
import FilmItem from "../components/filmItem";
import Paging from "../components/Pagination";

export default function Genre(props) {
  console.log(props);
  let { genreName } = useParams();
  const films=[
      {'name':"Fast and Furious"},
      {'name':"Captain America"},
      {'name':"Fast and Furious"},
      {'name':"Captain America"},
      {'name':"Fast and Furious"},
      {'name':"Captain America"},
      {'name':"Fast and Furious"},
      {'name':"Captain America"},
      {'name':"Fast and Furious"},
      {'name':"Captain America"},
  ]
  return (
    <div className="container-films">
      <Header props={props}/>
      <div className="main">
        <Container>
          <Row>
            {films.map(item => (
              <Col xs={4}>
                <FilmItem name={item.name}/>
              </Col>
            ))}
          </Row>
        </Container>
      </div>
      <Paging/>
    </div>
  );
}
