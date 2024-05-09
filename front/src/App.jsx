import "./App.css";
import Chart from "./components/chart";

function App() {
  return (
    <div className="App">
      <div className="userInputContainer">
        <input type="text" placeholder="원하는 기간을 입력하세요" />
        <input type="text" placeholder="원하는 비율을 입력하세요" />
      </div>
      <Chart />
    </div>
  );
}

export default App;
