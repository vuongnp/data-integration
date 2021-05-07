import React from "react";
import {
  Navbar,
  Nav,
  NavDropdown,
  Form,
  FormControl,
  Button,
} from "react-bootstrap";
import { Link } from "react-router-dom";

import "./header.css";

export default function Header(props) {
  console.log("header",props)
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
          <Nav.Link href="#link" style={{ color: "white" }}>
            Thống kê
          </Nav.Link>
          <NavDropdown title="Thể loại" id="basic-nav-dropdown">
            <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
            {/* <Link to="genre/action" className="title">
              Hành động
            </Link> */}
            <NavDropdown.Item href="#action/3.2">
              Another action
            </NavDropdown.Item>
            <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/3.4">
              Separated link
            </NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <Form inline>
          <FormControl type="text" placeholder="Tìm kiếm" className="mr-sm-2" />
          <Button variant="outline-warning">Tìm kiếm</Button>
        </Form>
      </Navbar.Collapse>
    </Navbar>
  );
}
