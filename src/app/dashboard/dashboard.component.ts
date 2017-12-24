import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { AngularFireDatabase } from 'angularfire2/database';
import { UserData, Season, Week, UserGame } from '../classes/user-data';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(public authService: AuthService, public adb: AngularFireDatabase) { }

  userId;
  userHistory = '?';

  ngOnInit() {
    this.authService.getUserId().subscribe(user_id => {
      this.userId = user_id;
      this.adb.object<any>('/users/' + this.userId).valueChanges().subscribe(user => {
        this.userHistory = user;
      });
    });
  }

}
