import React from "react";
import { useState } from "react";
export const UserInput = () => {
  const [firstDate, setFirstDate] = useState("");
  const [secondDate, setSecondDate] = useState("");
  const getFirstDate = (event) => setFirstDate(event.target.value);
  const getSecondDate = (event) => setSecondDate(event.target.value);
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(firstDate, secondDate);
  };
  return (
    <form onKeyPress={handleSubmit} className="userInputContainer">
      <input
        type="date"
        min="1980-03-18"
        max="2024-05-01"
        onChange={getFirstDate}
      />
      <input
        type="date"
        min="1980-03-18"
        max="2024-05-01"
        onChange={getSecondDate}
      />
    </form>
  );
};
