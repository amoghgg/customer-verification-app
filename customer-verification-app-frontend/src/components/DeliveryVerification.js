import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ItemCard from './ItemCard';
import { ReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

const DeliveryVerification = () => {
  const { cid } = useParams();
  const navigate = useNavigate();
  const [customer, setCustomer] = useState(null);
  const [error, setError] = useState('');
  const [videoBlob, setVideoBlob] = useState(null);

  // Detect environment and pick the correct backend URL
  const BASE_URL = process.env.REACT_APP_BACKEND_URL?.trim();

  useEffect(() => {
    console.log("Using API Base URL:", BASE_URL);
    if (!BASE_URL) {
      setError('⚠️ API base URL missing. Set REACT_APP_BACKEND_URL in .env');
      return;
    }

    const fetchCustomer = async () => {
      try {
        const res = await fetch(`${BASE_URL}/api/customer-details/?cid=${cid}`);
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        const withReceived = data.items.map(item => ({ ...item, received: '' }));
        setCustomer({ ...data, items: withReceived });
      } catch (err) {
        console.error(err);
        setError('Failed to fetch customer data from backend');
      }
    };

    if (cid) fetchCustomer();
  }, [cid, BASE_URL]);

  const handleReceivedChange = (index, value) => {
    const updated = [...customer.items];
    updated[index].received = parseInt(value) || 0;
    setCustomer({ ...customer, items: updated });
  };

  const uploadVideo = async () => {
    if (!videoBlob || !cid) return;

    const formData = new FormData();
    formData.append("file", videoBlob, `${cid}_proof.mp4`);
    formData.append("cid", cid);

    try {
      await axios.post(`${BASE_URL}/api/upload-proof-video/`, formData);
    } catch (err) {
      console.error(err);
      alert("❌ Video upload failed");
    }
  };

  const handleSubmit = async () => {
    const unfilled = customer.items.some(item => item.received === '');
    if (unfilled) {
      alert("Please fill all received quantities (use 0 if not received).");
      return;
    }

    const received = {};
    customer.items.forEach(item => {
      received[item.name] = item.received;
    });

    try {
      const res = await fetch(`${BASE_URL}/api/confirm-delivery/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cid: customer.cid, received }),
      });

      if (!res.ok) throw new Error('Failed to confirm delivery');

      if (videoBlob) {
        await uploadVideo();
      }

      navigate('/ThankYou');
    } catch (err) {
      console.error(err);
      alert("❌ Failed to confirm delivery");
    }
  };

  if (error) return <div style={{ padding: 20, color: 'red' }}>{error}</div>;
  if (!customer) return <div style={{ padding: 20 }}>Loading customer data...</div>;

  const hasMismatch = customer.items.some(
    item => item.received !== '' && item.sent !== item.received
  );

  return (
    <div style={{ padding: 20, maxWidth: 700, margin: 'auto' }}>
      <h2>Customer Delivery Verification</h2>
      <h3>{customer.name}</h3>
      <p><strong>Project:</strong> {customer.project}</p>
      <p><strong>Address:</strong> {customer.address}</p>

      {customer.items.map((item, idx) => (
        <ItemCard
          key={idx}
          item={item}
          value={item.received}
          onChange={(name, value) => handleReceivedChange(idx, value)}
        />
      ))}

      {hasMismatch && (
        <div style={{ marginTop: 30 }}>
          <h4>🎥 Optional Proof Video</h4>
          <ReactMediaRecorder
            video
            onStop={(blobUrl, blob) => setVideoBlob(blob)}
            render={({ startRecording, stopRecording, mediaBlobUrl }) => (
              <div>
                <button onClick={startRecording}>Start Recording</button>
                <button onClick={stopRecording} style={{ marginLeft: 10 }}>Stop</button>
                {mediaBlobUrl && <video src={mediaBlobUrl} controls width="300" />}
              </div>
            )}
          />
        </div>
      )}

      <button onClick={handleSubmit} style={{ marginTop: 30 }}>Submit</button>
    </div>
  );
};

export default DeliveryVerification;
