import React, {useState, useEffect} from 'react'
import {useParams} from 'react-router-dom'

import {clientRequest} from '../requests'

const Client = () => {
  let {clientId} = useParams()
  let [client, setClient] = useState({})
  let [funds, setFunds] = useState([])

  useEffect(() => {
    clientRequest(clientId).then(res => {
      setClient(res.client)
      setFunds(res.funds)
    })
  }, [clientId])

  const allFundRows = () => {
    return funds.map(fund => {
      return (
        <tr className="client-fund">
          <td>{fund.name}</td>
          <td>{fund.type_field}</td>
          <td>{fund.inception_date.slice(0,10)}</td>
          <td>{fund.description}</td>
        </tr>
      )
    })
  }
  
  return (
    <div>
      <h1>{client.name}</h1>
      <table className="client-fund-table">
        <thead>
          <tr>
            <td>Fund Name</td>
            <td>Type</td>
            <td>Inception Date</td>
            <td>Description</td>
          </tr>
        </thead>
        <tbody>
          {allFundRows()}
        </tbody>
      </table>
    </div>
  )
}

export default Client