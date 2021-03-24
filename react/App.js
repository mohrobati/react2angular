import './App.css';
import React from 'react';
import EntryBox from './Components/EntryBox';

const BLUE = "linear-gradient(90deg, rgba(15,76,117,1) 3%, rgba(0,62,103,1) 60%, rgba(11,55,84,1) 100%)";
const RED = "linear-gradient(90deg, rgba(217,33,9,1) 3%, rgba(157,7,7,1) 52%, rgba(103,9,9,1) 100%)";
const YELLOW = "linear-gradient(90deg, rgba(217,183,9,1) 3%, rgba(157,143,7,1) 52%, rgba(103,92,9,1) 100%)";

function App() {
  return (
    <div className="App">
      <EntryBox color={BLUE} title="Sport" img="https://cdn.uanews.arizona.edu/s3fs-public/styles/uaqs_large/public/story-images/track.jpg?itok=_lEae3Fs"/>
      <EntryBox color={RED} title="News" img="https://thumbor.forbes.com/thumbor/fit-in/1200x0/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F1017726862%2F0x0.jpg"/>
      <EntryBox color={YELLOW} title="Music" img="https://www.austrianblog.com/media/images/music-of-austria-modern-music-1.width-1600.jpg"/>
    </div>
  );
}

export default App;
