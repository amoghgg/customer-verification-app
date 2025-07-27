import React from 'react';
import './ItemCard.css';

const ItemCard = ({ item, index, onChange }) => {
  const isMatch = item.sent === item.received;

  return (
    <div className={`item-card ${isMatch ? 'matched' : 'mismatch'}`}>
      <div className="item-name">{index + 1}. {item.name}</div>
      <div className="qty-group">
        <div><strong>Sent:</strong> {item.sent}</div>
        <div>
          <strong>Received:</strong>{' '}
          <input
            type="number"
            min="0"
            value={item.received}
            onChange={(e) => onChange(index, parseInt(e.target.value, 10))}
          />
        </div>
      </div>
    </div>
  );
};

export default ItemCard;
