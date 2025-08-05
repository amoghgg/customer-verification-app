import React from 'react';
import './ItemCard.css';

const ItemCard = ({ item, value, onChange }) => {
  const sent = parseInt(item.sent);

  return (
    <div className="item-card">
      <div className="item-name">{item.name}</div>
      <div className="item-qty">
        <span>Sent: {item.sent}</span>
        <input
          type="number"
          min="0"
          value={value}
          placeholder="Received"
          onChange={(e) => onChange(item.name, e.target.value)}
        />
      </div>
    </div>
  );
};

export default ItemCard;
