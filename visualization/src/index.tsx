import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { HashRouter } from "react-router-dom";
import ReduxPromise from "redux-promise";
import reducers from "./reducers";
import Root from "./root";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

const createStoreWithMiddleware = applyMiddleware(ReduxPromise)(createStore);
const containerId = "root";

const store = createStoreWithMiddleware(reducers);
export default store;

ReactDOM.render(
  <MuiThemeProvider>
    <Provider store={store}>
      <HashRouter>
        <Root />
      </HashRouter>
    </Provider>
  </MuiThemeProvider>,
  document.getElementById(containerId)
);
