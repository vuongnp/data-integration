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
  let { text } = useParams();
  // console.log(genreName);
  let [films, setFilms] = React.useState([]);
  useEffect(() => {
    // GET request using axios inside useEffect React hook
    axios
      .get("https://data-intergration.herokuapp.com/search?text=" + text)
      .then((response) => setFilms(response.data));

    // empty dependency array means this effect will only run once (like componentDidMount in classes)
  }, []);
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
