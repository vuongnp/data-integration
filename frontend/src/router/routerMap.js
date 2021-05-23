import {
  Redirect,
  Route,
  Switch,
  withRouter,
  BrowserRouter,
} from "react-router-dom";
import React from "react";
// import history from "../router/history";
import RouterList from "./routeList";
import Home from "../pages/Home";
import Genre from "../pages/Genre";
import Search from "../pages/Search";

export default function RouterMap() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route exact path="/genre/:genreName"  component={Genre} />
        <Route exact path="/search/:text"  component={Search} />
      </Switch>
    </BrowserRouter>
  );
}
