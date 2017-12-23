import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { DatabaseReference } from 'angularfire2/database/interfaces';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  currentWeek;

  constructor(public dbSrv: DatabaseService) { }

  ngOnInit() {
    this.currentWeek = this.dbSrv.getWeekFromDb("week16");
  }

}
