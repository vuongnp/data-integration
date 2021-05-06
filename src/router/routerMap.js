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

class RouterMap extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route path="/" exact={true}>
            <Home />
          </Route>
          <Route path={RouterList.GENRE} exact={true}>
            {/* <Login/> */}
          </Route>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default RouterMap;
