import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-make-picks',
  templateUrl: './make-picks.component.html',
  styleUrls: ['./make-picks.component.css']
})
export class MakePicksComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute, public authService: AuthService) { }

  seasonId
  weekId
  userId
  weekDisplay

  ngOnInit() {
    this.authService.getUserId().subscribe(user_id => {
      this.userId = user_id;
      this.seasonId = '2019-2020'
      this.weekId = 'currentWeek'
    });
    if(this.weekId === 'currentWeek') {
      this.weekDisplay = 'Current Week'
    }
    else {
      var weekIdArray = this.weekId.split(/(\d+)/);
      this.weekDisplay = 'Week ' + String(weekIdArray[1]);
    }
  }

  reload() {
    location.reload();
  }

}
