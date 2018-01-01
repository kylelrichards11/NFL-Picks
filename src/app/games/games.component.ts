import { Component, OnInit, Input } from '@angular/core';
import { DatabaseReference } from 'angularfire2/database/interfaces';
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
  @Input() makePicks: boolean = false;
  @Input() userId: string;

  gameArray = new Array();
  userWeekPicks = false;
  gotData = false;
  weekHasStarted = false;

  constructor(public adb: AngularFireDatabase, public authService: AuthService) { }

  ngOnInit() {

    this.adb.list<Game>('/' + this.seasonId + '/' + this.weekId).valueChanges().subscribe(games => {
      this.gameArray = [];
      var foundStarted = false;
      games.forEach(game => {

        //get home and away team name for image 
        var homeImgPath = "../assets/teamLogos/" + game.home.name.toLowerCase() + ".png"
        var awayImgPath = "../assets/teamLogos/" + game.away.name.toLowerCase() + ".png"

        let uniqueGame = new Game(game.home, game.away, game.gameId, game.date, game.time, game.started, game.ended, homeImgPath, awayImgPath);
        this.gameArray.push(uniqueGame);

        if(!foundStarted) {
          if(game.started) {
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
        console.log('games', this.gameArray);
        console.log('picks', this.userWeekPicks);
        this.gotData = true;
      });
    });

    
  }

  pickTeam(teamCity, teamName, gameId) {
    var pick = teamCity + " " + teamName;
    this.adb.object<any>('/users/' + this.userId + '/seasons/' + this.seasonId + '/weeks/' + this.weekId + '/games/' + gameId).update({pick: pick});
  }

  clearPicks() {
    this.adb.object<any>('/users/' + this.userId + '/seasons/' + this.seasonId + '/weeks/' + this.weekId + '/games/').remove();
  }
}
