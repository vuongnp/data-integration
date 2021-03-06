import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import axios from "axios";

import Header from "../components/header";
import "./Genre.css";
import FilmItem from "../components/filmItem";
import Paging from "../components/Pagination";
import config from "../config/config";

export default function Genre() {
  let { genreName } = useParams();
  // console.log(genreName);
  // let [films, setFilms] = useState([]);
  const [filmsPage, setFilmsPage] = useState([]);
  const [page, setPage] = useState(1);
  const numberFilmsPage = 30;
  const [numberPages, setNumberPages] = useState(1);

  const handleNextPage = (event, page) => {
    // let start = (page - 1) * numberFilmsPage;
    // let end = start + numberFilmsPage;
    // setFilmsPage(films.slice(start, end));
    setPage(page);
  };


  useEffect(() => {
    // let aimURL = `${config.SERVER_URI}/category?text=` + genreName;
    // if (genreName === "imdb") {
    //   aimURL = aimURL + "&limit=100";
    // }
    axios
      .get(`${config.SERVER_URI}/category?text=` + genreName+'&page='+page+'&limit='+numberFilmsPage)
      .then((response) => {
        // setFilms(response.data.data);
        setNumberPages(Math.ceil(response.data.length / numberFilmsPage));
        setFilmsPage(response.data.data);
        // console.log(response.data);
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
    // const result = await axios(
    //   "https://data-intergration.herokuapp.com/category?text=" + genreName
    // );

    // setFilms(result.data);
  },[page]);
  // console.log(films);
  return (
    <div className="container-films">
      <Header />
      <div style={{marginTop:"100px"}}></div>
      <Paging
        count={numberPages}
        onChange={(event, page) => handleNextPage(event, page)}
      />
      <div className="main">
        <Container>
          <Row>
            {filmsPage.map((item, id) => (
              <Col xs={4} key={id}>
                <FilmItem item={item} />
              </Col>
            ))}
          </Row>
        </Container>
      </div>
      <Paging
        count={numberPages}
        onChange={(event, page) => handleNextPage(event, page)}
      />
    </div>
  );
}
