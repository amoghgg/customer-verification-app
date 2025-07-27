import React, { useState } from 'react';
import ItemCard from './ItemCard';

const DeliveryVerification = () => {
  const [cid, setCid] = useState('');
  const [customer, setCustomer] = useState(null);

  const fetchData = async () => {
    try {
      const res = await fetch(`/api/customer-details/?cid=${cid}`);
      const data = await res.json();
      if (res.ok) {
        const withReceived = data.items.map(item => ({ ...item, received: item.sent }));
        setCustomer({ ...data, items: withReceived });
      } else {
        alert(data.error || 'Customer not found');
      }
    } catch (err) {
      alert('Failed to fetch');
    }
  };

  const handleReceivedChange = (index, value) => {
    const updatedItems = [...customer.items];
    updatedItems[index].received = value;
    setCustomer({ ...customer, items: updatedItems });
  };

  const handleSubmit = () => {
    const mismatched = customer.items.filter(i => i.sent !== i.received);
    if (mismatched.length > 0) {
      alert(`Shortage in ${mismatched.length} items. Video recording should start.`);
      // ⏺ Integrate video recording logic if needed
    }
    console.log('📦 Submitted:', customer);
  };

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: 'auto' }}>
      <h2>Customer Delivery Verification</h2>
      <input
        value={cid}
        onChange={(e) => setCid(e.target.value)}
        placeholder="Enter Request ID"
        style={{ width: '100%', padding: '8px' }}
      />
      <button onClick={fetchData} style={{ marginTop: 10 }}>Fetch</button>

      {customer && (
        <div>
          <h3>{customer.name}</h3>
          <p><strong>Project:</strong> {customer.project}</p>
          <p><strong>Address:</strong> {customer.address}</p>

          {customer.items.map((item, idx) => (
            <ItemCard key={idx} item={item} index={idx} onChange={handleReceivedChange} />
          ))}

          <button onClick={handleSubmit} style={{ marginTop: 20 }}>Submit</button>
        </div>
      )}
    </div>
  );
};

export default DeliveryVerification;
