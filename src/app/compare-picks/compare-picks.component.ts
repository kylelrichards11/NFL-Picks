import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-compare-picks',
  templateUrl: './compare-picks.component.html',
  styleUrls: ['./compare-picks.component.scss']
})
export class ComparePicksComponent implements OnInit {

    constructor(private activatedRoute: ActivatedRoute, public authService: AuthService) { }

    userId: string;
    otherUserId: string;

    seasonId
    weekId
    weekNum
    invalidSeasonAndWeek = true;
    showGames = false;
    otherUserName
  
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
        if(this.userId == "H3EI5DDrbldJEg2FxEk6N9oYnaf2") {
            this.otherUserId = "wzht1HEeVZdTSw61qM6jS2j7TqN2"
            this.otherUserName = "Jay"
        }
        else {
            this.otherUserId = "H3EI5DDrbldJEg2FxEk6N9oYnaf2"
            this.otherUserName = "Kyle"
        }
        this.showGames = true;
        });
      var weekIdArray = this.weekId.split(/(\d+)/)
      this.weekNum = weekIdArray[1];
    }
}
