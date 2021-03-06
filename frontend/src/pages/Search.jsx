import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import axios from "axios";

import Header from "../components/header";
import "./Genre.css";
import FilmItem from "../components/filmItem";
import Paging from "../components/Pagination";
import config from "../config/config";

export default function Search() {
  let { text } = useParams();
  console.log('text',text);
  // let [films, setFilms] = useState([]);
  let [totalTilms, setTotalFilms] = useState(0);
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
    axios
    .get(`${config.SERVER_URI}/search?text=` + text+'&page='+page+'&limit='+numberFilmsPage)
      .then((response) => {
        // setFilms(response.data.data);
        setTotalFilms(response.data.length);
        setNumberPages(Math.ceil(response.data.length / numberFilmsPage));
        setFilmsPage(response.data.data);
        // console.log(response.data);
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  },[page]);
  // console.log(films);
  return (
    <div className="container-films">
      <Header />
      <div style={{color:"white", fontSize:"26px", marginTop:"100px"}}>Tìm thấy {totalTilms} kết quả</div>
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
