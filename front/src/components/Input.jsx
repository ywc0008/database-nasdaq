import React from "react";
import { useState } from "react";
import axios from "axios";

export const UserInput = () => {
  const [firstDate, setFirstDate] = useState("");
  const [secondDate, setSecondDate] = useState("");
  const getFirstDate = (event) => setFirstDate(event.target.value);
  const getSecondDate = (event) => setSecondDate(event.target.value);
  const [postData, setPostData] = useState({ firstDate: "", secondDate: "" });
  const handleSubmit = async (event) => {
    event.preventDefault();
    const dataToSend = {
      firstDate: firstDate,
      secondDate: secondDate,
    };
    setPostData(dataToSend);
    axios.defaults.baseURL = "http://127.0.0.1:8000";
    try {
      const res = await axios.post("http://127.0.0.1:8000/submit", dataToSend, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log(res);
    } catch (e) {
      console.log(`err : ${e}`);
    }
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
