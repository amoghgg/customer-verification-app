import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import DeliveryVerification from './components/DeliveryVerification';

function App() {
  const [cid, setCid] = useState('');
  const [data, setData] = useState(null);
  const [received, setReceived] = useState({});

  const fetchData = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/customer-details/?cid=${cid}`);
      
      // Remove non-product fields (like Pincode, C/nee No, etc.)
      const filteredItems = res.data.items.filter(item => {
        return item.sent > 0 &&
               !["Pincode", "PINCODE", "C/nee Number", "C/nee No", "Vendor No"].includes(item.name);
      });

      const updated = filteredItems.reduce((acc, item) => {
        acc[item.name] = 0;
        return acc;
      }, {});

      setData({ ...res.data, items: filteredItems });
      setReceived(updated);
    } catch (err) {
      alert('Customer not found');
      setData(null);
    }
  };

  const handleChange = (name, value) => {
    setReceived({ ...received, [name]: parseInt(value) || 0 });
  };

  const submitConfirmation = async () => {
    await axios.post('http://localhost:8000/api/confirm-delivery/', {
      cid: data.cid,
      received,
    });
    alert('Delivery confirmed!');
  };

  return (
    <div className="App">
      <h1>Customer Delivery Verification</h1>
      <input
        type="text"
        placeholder="Enter Customer ID"
        value={cid}
        onChange={e => setCid(e.target.value)}
      />
      <button onClick={fetchData}>Fetch</button>

      {data && (
        <div className="details">
          <h2>{data.name}</h2>
          <p><strong>Project:</strong> {data.project}</p>
          <p><strong>Address:</strong> {data.address}</p>

          <table>
            <thead>
              <tr>
                <th>Item</th>
                <th>Sent</th>
                <th>Received</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map(item => (
                <tr key={item.name}>
                  <td>{item.name}</td>
                  <td>{item.sent}</td>
                  <td>
                    <input
                      type="number"
                      min="0"
                      max={item.sent}
                      value={received[item.name]}
                      onChange={(e) => handleChange(item.name, e.target.value)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <button onClick={submitConfirmation}>Submit</button>
        </div>
      )}
    </div>
  );
}

export default App;
