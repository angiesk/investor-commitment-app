import React, { useState, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import axios from "axios";
import { roundAmount } from "./utils";

type Commitment = {
  asset_class: string;
  amount: number;
  currency: string;
  id: number;
};

const CommitmentTable = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const investorName = params.get("name") || "Unknown Investor";


  const [commitments, setCommitments] = useState<Commitment[]>([]);
  const [filteredCommitments, setFilteredCommitments] = useState<Commitment[]>(
    []
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [filter, setFilter] = useState<string>("All");
  const [sumByFilter, setSumByFilter] = useState<Record<string, number>>({
    All: 0,
    Infrastructure: 0,
    "Private Equity": 0,
    "Hedge Funds": 0,
    Other: 0,
  });

  useEffect(() => {
    const fetchCommitments = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/investors/${id}/commitments`
        );
        const fetchedCommitments: Commitment[] = response.data;

        const sumMap: Record<string, number> = {
          All: 0,
          Infrastructure: 0,
          "Private Equity": 0,
          "Hedge Funds": 0,
          Other: 0,
        };

        fetchedCommitments.forEach((commitment) => {
          const assetClass = commitment.asset_class || "Other";
          sumMap.All += commitment.amount;
          sumMap[assetClass] = (sumMap[assetClass] || 0) + commitment.amount;
        });

        setCommitments(fetchedCommitments);
        setSumByFilter(sumMap);
        setFilteredCommitments(fetchedCommitments);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching commitments:", error);
        setLoading(false);
      }
    };

    fetchCommitments();
  }, [id]);

  const filterCommitments = (assetClass: string) => {
    setFilter(assetClass);
    setFilteredCommitments(
      assetClass === "All"
        ? commitments
        : commitments.filter(
            (commitment) => commitment.asset_class === assetClass
          )
    );
  };

  const totalAmount = roundAmount(sumByFilter[filter]);

  if (loading) return <div className="text-center py-10">Loading...</div>;

  const buttonStyles = (active: boolean) =>
    `btn ${active ? "btn-primary" : "btn-outline-secondary"} px-4 py-2 me-2`;

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">
        Commitments for {investorName} (ID: {id})
      </h2>

      {/* Filter buttons */}
      <div className="text-center mb-4">
        <button
          onClick={() => filterCommitments("All")}
          className={buttonStyles(filter === "All")}
          disabled={sumByFilter.All === 0}
          aria-pressed={filter === "All"}
        >
          All
          {sumByFilter.All > 0 && (
            <div className="d-block mt-2">
              <span>{roundAmount(sumByFilter.All)} GBP</span>
            </div>
          )}
        </button>
        {["Infrastructure", "Private Equity", "Hedge Funds", "Other"].map(
          (assetClass) => {
            const sum = sumByFilter[assetClass] || 0;
            const isDisabled = sum === 0;

            return (
              <button
                key={assetClass}
                onClick={() => filterCommitments(assetClass)}
                className={buttonStyles(filter === assetClass)}
                disabled={isDisabled}
                aria-pressed={filter === assetClass}
              >
                {assetClass}
                {sum > 0 && (
                  <div className="d-block mt-2">
                    <span>{roundAmount(sum)} GBP</span>
                  </div>
                )}
              </button>
            );
          }
        )}
      </div>

      {/* Commitment Table */}
      <div className="table-responsive">
        {filteredCommitments.length > 0 ? (
          <table className="table table-striped table-bordered table-hover">
            <thead className="table-dark">
              <tr>
                <th>Asset Class</th>
                <th>Amount</th>
                <th>Currency</th>
              </tr>
            </thead>
            <tbody>
              {filteredCommitments.map((commitment) => (
                <tr key={commitment.id}>
                  <td>{commitment.asset_class || "Other"}</td>
                  <td>{roundAmount(commitment.amount)}</td>
                  <td>{commitment.currency}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-center">No commitments available.</p>
        )}
      </div>
    </div>
  );
};

export default CommitmentTable;
