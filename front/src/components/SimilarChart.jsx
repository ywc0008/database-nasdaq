import React, { useState, useEffect } from "react";

export const SimilarChart = ({ firstDate, secondDate }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [imagesrc, setImageSrc] = useState([]);
  const [pending, setPending] = useState(false); // pending 상태 추가

  const getSimilarData = async () => {
    if (!firstDate || !secondDate) return;

    setPending(true); // 데이터 가져오기 시작 시 pending 상태로 변경

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/cosine_similarity?firstDate=${firstDate}&secondDate=${secondDate}`
      );
      const result = await res.json();
      setData(result.similarity);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching similarity data:", error);
    } finally {
      setPending(false); // 데이터 가져오기 완료 시 pending 상태 해제
    }
  };

  const getImage = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/cosine_graph");
      const img = await res.json();
      setImageSrc(img);
    } catch (error) {
      console.error("Error fetching image:", error);
    }
  };

  useEffect(() => {
    if (firstDate && secondDate) {
      getSimilarData();
      getImage();
    }
  }, [firstDate, secondDate]);
  console.log(imagesrc);
  return (
    <div>
      {pending ? (
        <h1>데이터 가져오는 중...</h1>
      ) : loading ? (
        <h1>Loading...</h1>
      ) : (
        // 데이터가 있는 경우
        <div>
          <ul>
            {Object.entries(data).map(([index, similarity], idx) => (
              <li key={index}>
                <div>{`구간: ${index}, 코사인 유사도: ${similarity}`}</div>
                <img
                  style={{ height: "600px", width: "600px" }}
                  src={`data:image/png;base64,${imagesrc[idx]}`}
                  alt="Similarity chart"
                />
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
