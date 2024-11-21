import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CommitmentTable from "./CommitmentTable";
import InvestorTable from "./InvestorTable"; // Assuming this is another component you have
import "bootstrap/dist/css/bootstrap.min.css";
const App = () => {
  return (
    <Router>
      <div>
        <h1>
          <center>Investor Dashboard</center>
        </h1>
        <Routes>
          {/* Route for the investor table */}
          <Route path="/" element={<InvestorTable />} />

          {/* Route for the commitment table, passing investor ID as a param */}
          <Route path="/commitments/:id" element={<CommitmentTable />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
