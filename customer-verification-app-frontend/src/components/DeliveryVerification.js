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

  useEffect(() => {
    const fetchCustomer = async () => {
      try {
        const res = await fetch(`/api/customer-details/?cid=${cid}`);
        const data = await res.json();
        const withReceived = data.items.map(item => ({ ...item, received: '' }));
        setCustomer({ ...data, items: withReceived });
      } catch (err) {
        setError('Failed to fetch customer data');
      }
    };

    if (cid) fetchCustomer();
  }, [cid]);

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
      await axios.post("/api/upload-proof-video/", formData);
    } catch (err) {
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
      await fetch('/api/confirm-delivery/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cid: customer.cid, received }),
      });

      if (videoBlob) {
        await uploadVideo();
      }

      navigate('/thankyou');
    } catch {
      alert("❌ Failed to confirm delivery");
    }
  };

  if (error) return <div>{error}</div>;
  if (!customer) return <div>Loading...</div>;

  const hasMismatch = customer.items.some(item =>
    item.received !== '' && item.sent !== item.received
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
