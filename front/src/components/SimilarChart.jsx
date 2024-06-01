import React, { useState, useEffect } from "react";
export const SimilarChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [imagesrc, setImageSrc] = useState("");
  const getSimilarData = async () => {
    const res = await (
      await fetch("http://127.0.0.1:8000/cosine_similarity")
    ).json();
    setData(res);
    setLoading(false);
  };

  const getImage = async () => {
    const img = await (
      await fetch("http://127.0.0.1:8000/cosine_graph")
    ).json();
    setImageSrc(img);
  };

  useEffect(() => {
    getSimilarData();
  }, []);
  useEffect(() => {
    getImage();
  }, []);
  console.log(`data:image/png;base64,${imagesrc}`);
  return (
    <h1>
      {loading ? (
        <h1>로딩중...</h1>
      ) : (
        data.map((item, index) => (
          <ul>
            <li key={index}>{item.similarity}</li>
            <img
              style={{ height: "600px", width: "600px" }}
              src={`data:image/png;base64,${imagesrc}`}
              alt={`Similarity chart ${index}`}
            />
          </ul>
        ))
      )}
    </h1>
  );
};
