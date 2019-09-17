import { Component, OnInit, Input } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';
import { AuthService } from '../services/auth.service';
import { Game } from '../classes/game';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.css']
})
export class GamesComponent implements OnInit {

  @Input() seasonId: string;
  @Input() weekId: string;
  @Input() userId: string;
  @Input() showWeeks: boolean;

  gameArray = new Array();
  userWeekPicks = false;
  gotData = false;
  weekHasStarted = true;
  makePicks = false;

  constructor(public adb: AngularFireDatabase, public authService: AuthService) { }

  ngOnInit() {

    if (this.weekId === 'currentWeek') { //if the component input wants the current week
      // subscribe to all weeks in the season
      this.adb.list<any>(this.seasonId + '/weeks').valueChanges().subscribe(season => {

        //make an array to hold the numbers of weeks that have not yet ended
        var notEndedWeekArray = new Array();
        notEndedWeekArray = [];

        //loop through weeks in database and check if they have ended
        season.forEach(week => {

          // if the week has not ended
          if (!week.weekInfo.ended) {
            var weekNum = week.weekInfo.weekId.split(/(\d+)/) //get the week's number
            notEndedWeekArray.push(weekNum[1]); //add the number to the array
          }
        });

        //if the array is empty, then all weeks must have ended
        if (!notEndedWeekArray.length) {
          this.weekId = 'week17'; //if the season has ended, display the last week
        }

        //if the array is not empty, then there must be weeks that have not ended
        else {
          var minNum = 18; //minNum stores the week number that is the lowest (first occuring in the season)
          //we use 18 since week 17 is the highest possible week
          for (let num of notEndedWeekArray) { // loop through the array
            if (Number(num) < minNum) { // if the number in the array is less than the current min, 
              minNum = Number(num); //make that the min
            }
          }
          // once we have the lowest week number that has not ended, 
          this.weekId = 'week' + String(minNum); //append that number to 'week' to make the weekId
        }
        this.getWeekGameInfo(); //get the games for the weekId to display
      });
    }
    else { //if we already know the weekId we want
      this.getWeekGameInfo(); //get the games for the weekId to display
    }
  }

  getWeekGameInfo() {
    this.adb.list<Game>('/' + this.seasonId + '/weeks/' + this.weekId + '/games').valueChanges().subscribe(games => {
      this.gameArray = [];
      var foundStarted = false;
      games.forEach(game => {

        //get home and away team name for image 
        var homeImgPath = "../assets/teamLogos/" + game.home.name.toLowerCase() + ".png"
        var awayImgPath = "../assets/teamLogos/" + game.away.name.toLowerCase() + ".png"

        let uniqueGame = new Game(game.home, game.away, game.gameId, game.date, game.time, game.started, game.ended, homeImgPath, awayImgPath);
        this.gameArray.push(uniqueGame);

        if (!foundStarted) {
          if (game.started) {
            this.weekHasStarted = true;
            foundStarted = true;
          }
        }
      })
    });

    this.authService.getUserId().subscribe(user_id => {
      this.userId = user_id;
      this.adb.object<any>('/users/' + this.userId).valueChanges().subscribe(user => {
        this.userWeekPicks = user.seasons[this.seasonId].weeks[this.weekId];
        this.gotData = true;
      });
      this.makePicks = true;
    });
  }

  pickTeam(teamCity, teamName, gameId) {
    var pick = teamCity + " " + teamName;
    this.adb.object<any>('/users/' + this.userId + '/seasons/' + this.seasonId + '/weeks/' + this.weekId + '/' + gameId).update({ pick: pick });
  }

  clearPicks() {
    this.adb.object<any>('/users/' + this.userId + '/seasons/' + this.seasonId + '/weeks/' + this.weekId + '/games/').remove();
  }

  changeWeek(newWeek) {
    this.weekId = newWeek;
    this.ngOnInit();
  }
}
