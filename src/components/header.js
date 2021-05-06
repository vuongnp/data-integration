import React from "react";
import {Navbar,Nav,NavDropdown,Form, FormControl, Button} from 'react-bootstrap';

export default function Header() {
  return (
    <Navbar expand="lg" bg="dark" variant="dark" fixed="top">
      <Navbar.Brand href="/">Khophim.vn</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/">Trang chủ</Nav.Link>
          <Nav.Link href="#link">Thống kê</Nav.Link>
          <NavDropdown title="Chủ đề" id="basic-nav-dropdown">
            <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
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
