import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { AngularFireDatabase } from 'angularfire2/database';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  seasonId = '2019-2020';
  weekId = 'currentWeek';

  constructor(public dbSrv: DatabaseService, public adb: AngularFireDatabase, public authService: AuthService) { }

  ngOnInit() {}
}
