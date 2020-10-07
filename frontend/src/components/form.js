import React, {useState, useEffect} from 'react'
import { cashFlowRequest, submitCashFlow } from '../requests'

// helper methods - rely on existing state
const currentAvailableInvestmentTypes = (client) => {
  if (!client?.permission) return []
  return client.permission
}
const currentAvailableInvestments = (investments, client, investmentType) => {
  return investments.filter(i => {
    return (i.fund.type_field == investmentType && i.client_id == client.id)
  })
}

const Form = () => {
  const [clients, setClients] = useState([])
  const [investments, setInvestments] = useState([])
  const [tempReturn, setTempReturn] = useState(0)
  const [newReturn, setNewReturn] = useState(0)
  const [chosenDate, setDate] = useState(new Date().toISOString().slice(0,10))

  const [currentClient, setCurrentClient] = useState({})
  const [currentInvestmentType, setCurrentInvestmentType] = useState('')
  const [currentInvestment, setCurrentInvestment] = useState({})


  useEffect(() => {
    const fetchData = async() => {
      let response = await cashFlowRequest()
      setClients(response.clients)
      setInvestments(response.investments)
    }
    fetchData()
  }, [])

  // Whenever we choose an option, the other selects should change to match this.
  useEffect(() => {
    setCurrentClient(clients[0])
  }, [clients])

  useEffect(() => {
    let types = currentAvailableInvestmentTypes(currentClient)
    if (types) setCurrentInvestmentType(types[0])
    else setCurrentInvestmentType('')
  }, [currentClient])

  useEffect(() => {
    let invs = currentAvailableInvestments(investments, currentClient, currentInvestmentType)
    if (invs && invs.length) setCurrentInvestment(invs[0])
    else setCurrentInvestment({})
  }, [investments, currentInvestmentType, currentClient])

  // Three selects, each depends on the previous.
  const renderInvestmentSelects = () => {
    const clientOptions = () => {
      return clients.map(client => {
        return <option key={client.id} value={client.id}>{client.name}</option>
    })
    }
    const handleClientChange = (event) => {
      let clientId = event.target.value
      // Linear search is not the most efficient, but will be fine for small scale.
      clients.forEach(client => {
        if (client.id == clientId) setCurrentClient(client)
      })
    }

    // Investment types are dependent only on the client
    const investmentTypeOptions = () => {
      return currentAvailableInvestmentTypes(currentClient).map(type => {
        return <option key={type} value={type}>{type}</option>
      })
    }
    const handleTypeChange = (event) => {
      setCurrentInvestmentType(event.target.value)
    }

    // Available investments depend both on the client and the chosen type
    const investmentOptions = () => {
      return currentAvailableInvestments(
        investments, currentClient, currentInvestmentType).map(i => {
          return <option key={i.id} value={i.id}>{i.name}</option>
        })
    }
    const handleInvestmentChange = (event) => {
      let investmentId = event.target.value
      investments.forEach(i => {
        if (i.id == investmentId) setCurrentInvestment(i)
      })
    }

    return(
      <React.Fragment>
        <select name="client" id="input-client" onChange={handleClientChange}>{clientOptions()}</select>
        <select name="investment-type" id="input-investment-type" onChange={handleTypeChange}>{investmentTypeOptions()}</select>
        <select name="investment-name" id="input-investment-name" onChange={handleInvestmentChange}>{investmentOptions()}</select>
      </React.Fragment>
    )
  }

  const renderCalculateInvestmentFields = () => {
    const currentValue = () => {
      let value = 0
      if (currentInvestment.current_value) value = currentInvestment.current_value
      return value.toFixed(2)
    }
    const updatedValue = () => {
      let value = 0
      if (currentInvestment.amount) value = parseFloat(currentInvestment.amount)
      return (value + (value * newReturn / 100))
    }
    const updateReturn = (event) => {
      event.preventDefault()
      setNewReturn(tempReturn)
    }
    return(
      <React.Fragment>
        <label htmlFor="input-current-value">Current Value</label>
        <input type="number" name="current-value" id="input-current-value" readOnly="readonly" value={currentValue()}/>

        <label htmlFor="input-updated-value">Updated Value</label>
        <input type="number" name="updated-value" id="input-updated-value" readOnly="readonly" value={updatedValue()}/>

        <br/>
        <br/>

        <label htmlFor="input-date">Date</label> 
        <input type="date" name="calculate-date" id="input-date" value={chosenDate} onChange={e => setDate(e.target.value)}/>
        <label htmlFor="input-value">New Return</label>
        <input type="number" name="calculate-value" id="input-value"
          value={tempReturn} onChange={e => setTempReturn(e.target.value)}/>
        <button id="input-calculate-total" onClick={updateReturn}>Calculate</button>
      </React.Fragment>
    )
  }

  const handleSubmit = async(event) => {
    event.preventDefault()
    let res = await submitCashFlow(currentInvestment, newReturn, chosenDate)
    setInvestments(res['investments'])
  }

  return (
    <div className="Form">
      <h1>Form</h1>
      <form id="cash-flow-update-form" onSubmit={handleSubmit}>
        {renderInvestmentSelects()}
        <br/>
        <br/>
        {renderCalculateInvestmentFields()}
        <br/>
        <br/>
        <input type="submit" value="Submit"/>
      </form>
    </div>
  );
}

export default Form