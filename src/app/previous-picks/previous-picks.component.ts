import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-previous-picks',
  templateUrl: './previous-picks.component.html',
  styleUrls: ['./previous-picks.component.css']
})
export class PreviousPicksComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute, public authService: AuthService) { }

  seasonId
  weekId
  userId
  weekNum
  invalidSeasonAndWeek = true;

  ngOnInit() {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.seasonId = params['seasonId'];
      this.weekId = params['weekId'];
    });
    if ((this.seasonId != 'undefined') && (this.weekId != 'undefined')) {
      this.invalidSeasonAndWeek = false;
    }
    this.authService.getUserId().subscribe(user_id => {
      this.userId = user_id;
    });
    var weekIdArray = this.weekId.split(/(\d+)/)
    this.weekNum = weekIdArray[1];
  }

}
