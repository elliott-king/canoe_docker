import React, {useState, useEffect} from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

import {allClientsRequest} from '../requests'
import Client from './client'

const Home = () => {
  let [clients, setClients] = useState([])

  useEffect(() => {
    console.log('making request')
    allClientsRequest().then(res => setClients(res.clients))
  }, [])

  let match = useRouteMatch()

  const clientLinks = () => {
    return clients.map(client => {
      return (
        <li key={client.id}>
          <Link to={`/${client.id}`}>{client.name}</Link>
        </li>
      )
    })
  }

  return (
    <div>
      <h1>Clients</h1>
      <ul>
        {clientLinks()}
      </ul>
      <Switch>
        <Route path={`/:clientId`}>
          <Client/>
        </Route>
      </Switch>
    </div>
  )
} 

export default Home