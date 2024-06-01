import "./App.css";
import Chart from "./components/chart";
import { SimilarChart } from "./components/SimilarChart";
import { UserInput } from "./components/Input";

function App() {
  return (
    <div className="App">
      <div className="userInputContainer">
        <UserInput />
      </div>
      <div className="chart">
        <Chart />
      </div>
      <div className="similarChart">
        <SimilarChart />
      </div>
    </div>
  );
}

export default App;
