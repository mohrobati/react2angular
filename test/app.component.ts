import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  BLUE = "linear-gradient(90deg, rgba(15,76,117,1) 3%, rgba(0,62,103,1) 60%, rgba(11,55,84,1) 100%)"
  RED = "linear-gradient(90deg, rgba(217,33,9,1) 3%, rgba(157,7,7,1) 52%, rgba(103,9,9,1) 100%)"
  YELLOW = "linear-gradient(90deg, rgba(217,183,9,1) 3%, rgba(157,143,7,1) 52%, rgba(103,92,9,1) 100%)"
  SPORT_URL = "/assets/sport.jpg"
  NEWS_URL = "/assets/news.jpg"
  MUSIC_URL = "/assets/music.jpg"
}
