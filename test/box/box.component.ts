import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-box',
  templateUrl: './box.component.html',
  styleUrls: ['./box.component.css']
})
export class BoxComponent implements OnInit {
  
  @Input() color: string;
  @Input() img: string;
  @Input() title: string;

  constructor() {
    this.color = ""
    this.img = ""
    this.title = ""
  }

  ngOnInit(): void {
  }
  

}
