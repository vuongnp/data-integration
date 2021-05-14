import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import axios from "axios";

import Header from "../components/header";
import "./Genre.css";
import FilmItem from "../components/filmItem";
import Paging from "../components/Pagination";

export default function Genre(props) {
  // console.log(props);
  let { genreName } = useParams();
  // console.log(genreName);
  let [films, setFilms] = React.useState([]);
  useEffect(async () => {
    const result = await axios(
      "https://data-intergration.herokuapp.com/category?text=" + genreName
    );

    setFilms(result.data);
  });
  // console.log(films);
  return (
    <div className="container-films">
      <Header />
      <div className="main">
        <Container>
          <Row>
            {films.map((item) => (
              <Col xs={4}>
                <FilmItem item={item} />
              </Col>
            ))}
          </Row>
        </Container>
      </div>
      <Paging />
    </div>
  );
}
