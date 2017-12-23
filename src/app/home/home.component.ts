import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { DatabaseReference } from 'angularfire2/database/interfaces';
import { AngularFireDatabase } from 'angularfire2/database';
import { Game } from '../classes/game';
import { Team } from '../classes/team';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  gameArray = new Array();
  team = new Team('?', '?');
  weekNum = 'week16';

  constructor(public dbSrv: DatabaseService, public adb: AngularFireDatabase) { }

  ngOnInit() {

    this.adb.list<Game>('/2017-2018/' + this.weekNum).valueChanges().subscribe(games => {
      this.gameArray = [];
      games.forEach(game => {

        //get home and away team name without city for image name
        var homeSplit = game.home.split(" ");
        var homeImg = homeSplit[homeSplit.length - 1].toLowerCase();
        var homeImgPath = "../assets/teamLogos/" + homeImg + ".png"
        var awaySplit = game.away.split(" ");
        var awayImg = awaySplit[awaySplit.length - 1].toLowerCase();
        var awayImgPath = "../assets/teamLogos/" + awayImg + ".png"

        let uniqueGame = new Game(game.home, game.away, game.date, game.time, homeImgPath, awayImgPath);
        this.gameArray.push(uniqueGame);
      })
    });
    
    this.adb.object<Team>('/2017-2018/teams/Baltimore Ravens').valueChanges().subscribe(myTeam => {
      this.team=myTeam;
      console.log('myteam: ', myTeam);
    });
    
  }

  getTeamRecord(teamName) {
    return this.dbSrv.getTeamWinLoss(teamName);
  }

}
