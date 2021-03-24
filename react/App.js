import './App.css';
import React from 'react';
import EntryBox from './Components/EntryBox';

const BLUE = "linear-gradient(90deg, rgba(15,76,117,1) 3%, rgba(0,62,103,1) 60%, rgba(11,55,84,1) 100%)";
const RED = "linear-gradient(90deg, rgba(217,33,9,1) 3%, rgba(157,7,7,1) 52%, rgba(103,9,9,1) 100%)";
const YELLOW = "linear-gradient(90deg, rgba(217,183,9,1) 3%, rgba(157,143,7,1) 52%, rgba(103,92,9,1) 100%)";

function App() {
  return (
    <div className="App">
      <EntryBox color={BLUE} title="Sport" img="/sport.jpg"/>
      <EntryBox color={RED} title="News" img="/news.jpg"/>
      <EntryBox color={YELLOW} title="Music" img="/music.jpg"/>
    </div>
  );
}

export default App;
