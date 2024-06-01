import React, { useState, useEffect } from "react";
export const SimilarChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const getSimilarData = async () => {
    const res = await (
      await fetch("http://127.0.0.1:8000/cosine_similarity")
    ).json();
    setData(res);
    setLoading(false);
  };
  console.log(data);
  useEffect(() => {
    getSimilarData();
  }, []);
  return (
    <h1>
      {loading ? (
        <h1>로딩중...</h1>
      ) : (
        data.map((item, index) => (
          <ul>
            <li key={index}>{item.similarity}</li>
          </ul>
        ))
      )}
    </h1>
  );
};
