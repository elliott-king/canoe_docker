import React from 'react'
import {
  BrowserRouter as Router, 
  Link, 
  Switch, 
  Route
} from 'react-router-dom'

import Form from './components/form'
import Home from './components/home'

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/form">Form</Link>
            </li>
          </ul>
        </nav>
        <Switch>
          <Route path="/form">
            <Form />
          </Route>
          <Route path="/clients">
            {/* <Clients /> */}
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  )
}

export default App;
