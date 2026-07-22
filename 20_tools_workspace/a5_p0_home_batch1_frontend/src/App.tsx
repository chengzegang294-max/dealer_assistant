import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "@/pages/Home";
import Stock from "@/pages/Stock";
import StockQa from "@/pages/StockQa";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/stock/:stockCode" element={<Stock />} />
        <Route path="/stock/:stockCode/qa" element={<StockQa />} />
        <Route path="/other" element={<div className="text-center text-xl">Other Page - Coming Soon</div>} />
      </Routes>
    </Router>
  );
}
