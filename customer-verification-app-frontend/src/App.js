import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DeliveryVerification from './components/DeliveryVerification';
import ThankYou from './components/ThankYou';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/verify/FA4492" replace />} />
        <Route path="/verify/:cid" element={<DeliveryVerification />} />
        <Route path="/thank-you" element={<ThankYou />} />
      </Routes>
    </Router>
  );
}

export default App;
