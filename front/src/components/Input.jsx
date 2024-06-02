import React from "react";

export const UserInput = ({ setFirstDate, setSecondDate, onSubmit }) => {
  const getFirstDate = (event) => setFirstDate(event.target.value);
  const getSecondDate = (event) => setSecondDate(event.target.value);
  const handleSubmit = async (event) => {
    event.preventDefault();
    onSubmit();
    
  };
  return (
    <form onSubmit={handleSubmit} className="userInputContainer">
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
      <button type="submit">Submit</button>
    </form>
  );
};
