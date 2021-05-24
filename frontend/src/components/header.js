import React,{useEffect, useState} from "react";
import {
  Navbar,
  Nav,
  NavDropdown,
  Form,
  FormControl,
  Button,
  Container,
  Row,
  Col,
} from "react-bootstrap";
import { Link } from "react-router-dom";

import "./header.css";

export default function Header() {
  let [searchvalue, setSearchValue] = useState('');
  let onSearch=()=>{
    console.log(searchvalue);
    setSearchValue('');
  }
  const handleChange = e => {
    setSearchValue(e.target.value)
    // console.log(searchvalue)
  }
  const categories = [
    { "mystery": "Bí ẩn" },
    { "war": "Chiến tranh" },
    { "drama": "Kịch tính" },
    { "family": "Gia đình" },
    { "comedy": "Hài hước" },
    { "action": "Hành động" },
    { "animation": "Hoạt hình" },
    { "sci-fi": "Khoa học" },
    { "horror": "Kinh dị" },
    { "romance": "Lãng mạn" },
    { "adventure":"Phiêu lưu"},
    { "music":"Âm nhạc"},
    { "kids":"Trẻ em"},
    { "documentary":"Phim tài liệu"}
];
  return (
    <Navbar expand="lg" bg="dark" variant="dark" fixed="top">
      <Navbar.Brand href="/" style={{ fontSize: "28px" }}>
        KHOPHIM.VN
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/" style={{ color: "white" }}>
            Trang chủ
          </Nav.Link>
          <Nav.Link href="/stat" style={{ color: "white" }}>
            Thống kê
          </Nav.Link>
          <NavDropdown title="Danh mục" id="basic-nav-dropdown">
            <Row>
              {categories.map((item, index) => (
                <Col xs={4} key={index}>
                  <NavDropdown.Item href={`/genre/${Object.keys(item)[0]}`}>
                    {Object.values(item)[0]}
                  </NavDropdown.Item>
                </Col>
              ))}
            </Row>
            <NavDropdown.Divider />
            <NavDropdown.Item href="/genre/imdb">Top IMDB</NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <Form inline>
          <FormControl
            type="text"
            placeholder="Tên phim, diễn viên,..."
            className="mr-sm-2"
            value={searchvalue}
            onChange={handleChange}
          />
          <Button variant="outline-warning" href={searchvalue!='' ? `/search/${searchvalue}`:'#'}>Tìm kiếm</Button>
        </Form>
      </Navbar.Collapse>
    </Navbar>
  );
}
