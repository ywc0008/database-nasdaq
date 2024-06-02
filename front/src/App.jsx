import "./App.css";
import Chart from "./components/chart";
import { SimilarChart } from "./components/SimilarChart";
import { UserInput } from "./components/Input";
import { Suspense, useState } from "react";

function App() {
  const [firstDate, setFirstDate] = useState("");
  const [secondDate, setSecondDate] = useState("");
  const [similarityData, setSimilarityData] = useState(null);

  const handleInputSubmit = async () => {
    try {
      const res = await fetch("http://localhost:8000/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          firstDate: firstDate,
          secondDate: secondDate,
        }),
      });
      const data = await res.json();
      setSimilarityData(data);
    } catch (error) {
      console.error("Error submitting input:", error);
    }
  };
  return (
    <div className="App">
    
      {/* <Suspense allback={<h1>데이터 불러오는중</h1>} className="chart">
        <Chart />
      </Suspense> */}
        <Suspense fallback={<h1>화면 로딩중</h1>}>
        <UserInput 
        setFirstDate={setFirstDate}
        setSecondDate={setSecondDate}
        onSubmit={handleInputSubmit}
        setSimilarityData={setSimilarityData}
          />
      </Suspense>
      <Suspense fallback={<h1>화면 로딩중</h1>} className="similarChart">
        <SimilarChart 
        similarityData={similarityData}
        firstDate={firstDate}
        secondDate={secondDate}/>
      </Suspense>
    </div>
  );
}

export default App;
