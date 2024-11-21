
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { calculateTotalCommitments } from "./utils"; // Assume calculateTotalCommitments exists
import { roundAmount } from "./utils"; // Assume roundAmount exists

type Investor = {
  id: number;
  name: string;
  email: string;
  country: string;
  commitments: {
    amount: number;
    currency: string;
  }[];
};

const InvestorTable = () => {
  const [investors, setInvestors] = useState<Investor[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInvestors = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/investors/"
        );
        setInvestors(response.data); // Assuming the API returns a list of investors
        setLoading(false);
      } catch (err) {
        console.error("Error fetching investors:", err);
        setError("Failed to fetch investors. Please try again later.");
        setLoading(false);
      }
    };

    fetchInvestors();
  }, []);

  if (loading) {
    return (
      <div className="text-center py-10">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className="alert alert-danger text-center">{error}</div>;
  }

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Investor Table</h2>

      <div className="table-responsive">
        <table className="table table-striped table-bordered table-hover">
          <thead className="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Country</th>
              <th>Commitment Amount(GBP)</th>
            </tr>
          </thead>
          <tbody>
            {investors.map((investor) => {
              const totalCommitment = calculateTotalCommitments(
                investor.commitments,
                "GBP"
              );

              return (
                <tr key={investor.id}>
                  <td>{investor.name || "N/A"}</td>
                  <td>{investor.email || "N/A"}</td>
                  <td>{investor.country || "N/A"}</td>
                  <td>
                    <Link
                      to={`/commitments/${
                        investor.id
                      }?name=${encodeURIComponent(investor.name)}`}
                      className="btn btn-link p-0 text-decoration-none"
                    >
                      {totalCommitment > 0
                        ? `${roundAmount(totalCommitment)}`
                        : "No commitments"}
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default InvestorTable;

