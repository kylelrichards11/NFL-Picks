import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { DatabaseReference } from 'angularfire2/database/interfaces';
import { AngularFireDatabase } from 'angularfire2/database';
import { Game } from '../classes/game';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  seasonId = '2017-2018';
  weekId;

  constructor(public dbSrv: DatabaseService, public adb: AngularFireDatabase) { }

  ngOnInit() {

    this.adb.list<any>('2017-2018').valueChanges().subscribe(season => {
      console.log(season);
      var foundCurrentWeek = false;
      season.forEach(week => {
        if(!week.ended && !foundCurrentWeek) {
          this.weekId = week.weekId;
          foundCurrentWeek = true;
        }
      });
      if(!foundCurrentWeek) {
        console.log('never found week')
        this.weekId = 'week17';
      }
    });
  }
}
