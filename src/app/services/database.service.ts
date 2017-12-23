import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';
import { Observable } from 'rxjs/Observable';
import { Game } from '../classes/game';
import { Team } from '../classes/team';

@Injectable()
export class DatabaseService {


  constructor(public adb: AngularFireDatabase) { }

  getWeekFromDb(weekNum) {
    let weekArray = new Array();
    this.adb.list<Game>('/2017-2018/' + weekNum).valueChanges().subscribe(games => {
      games.forEach(game => {

        //get home and away team name without city for image name
        var homeSplit = game.home.split(" ");
        var homeImg = homeSplit[homeSplit.length - 1].toLowerCase();
        var homeImgPath = "../assets/teamLogos/" + homeImg + ".png"
        var awaySplit = game.away.split(" ");
        var awayImg = awaySplit[awaySplit.length - 1].toLowerCase();
        var awayImgPath = "../assets/teamLogos/" + awayImg + ".png"

        let uniqueGame = new Game(game.home, game.away, game.date, game.time, homeImgPath, awayImgPath);
        weekArray.push(uniqueGame);
      })
    });
    return weekArray;
  }

  getTeam(teamName) {
    var team = this.adb.object<Team>('/2017-2018/teams/' + teamName).valueChanges().subscribe(myTeam => {
      console.log('myteam: ', myTeam);
      return myTeam;
    });
  }

  getTeamWinLoss(teamName) {
    this.adb.object<Team>('/2017-2018/teams/' + teamName).valueChanges().subscribe(team => {
      var recordString = (team.wins + " - " + team.losses);
      console.log("recordString: ", recordString);
      return recordString;
    });
  }
}
