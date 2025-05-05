import React, { useState } from "react";

type VoteData = {
  Address: string;
  "Time Diff between first and last (Mins)": number;
  "Face Attempts": number;
  "Detected As a Robot At Least Once": number;
  "Face Match Percentage": number;
  "Liveness Score of The Face": number;
};

type ApiResponse = {
  Address: string;
  is_fraud: boolean;
};

function ValidateVote() {
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const sendVoteData = async () => {
    const data: VoteData = {
      "Address": "0x3f5CE5FBFe3E9af3971dD833D26BA9b5C936f0bE",
      "Time Diff between first and last (Mins)": 12.0,
      "Face Attempts": 3,
      "Detected As a Robot At Least Once": 0,
      "Face Match Percentage": 44.2,
      "Liveness Score of The Face": 53.6,
    };

    try {
      const response = await fetch("http://localhost:8000/validate_vote/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Server responded with an error");
      }

      const responseData: ApiResponse = await response.json();
      setResult(responseData);
      setError(null);
    } catch (err) {
      console.error("Error:", err);
      setError("Something went wrong while validating the vote.");
      setResult(null);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Election Fraud Detection</h2>
      <button onClick={sendVoteData}>Validate Vote</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h4>Result:</h4>
          <p><strong>Address:</strong> {result.Address}</p>
          <p><strong>Is Fraud:</strong> {result.is_fraud ? "Yes" : "No"}</p>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default ValidateVote;
