import React, { useState } from "react";

export const UserInput = ({ setFirstDate, setSecondDate, onSubmit }) => {
  const [pending, setPending] = useState(false);

  const getFirstDate = (event) => setFirstDate(event.target.value);
  const getSecondDate = (event) => setSecondDate(event.target.value);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setPending(true); // 데이터 전송 시작 시 pending 상태로 변경
    await onSubmit(); // onSubmit 함수 실행 (데이터 전송)
    setPending(false); // 데이터 전송 완료 후 pending 상태 해제
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
      <button type="submit" disabled={pending}>
        {pending ? "분석중..." : "검색하기"}
      </button>
    </form>
  );
};
