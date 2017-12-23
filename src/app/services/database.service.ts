import { Injectable } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';
import { Game } from '../classes/game';

@Injectable()
export class DatabaseService {


  constructor(public adb: AngularFireDatabase) { }

  getWeekFromDb(weekNum) {
    let weekArray = new Array();
    let week = this.adb.list<Game>('/2017-2018/' + weekNum).valueChanges();
    week.subscribe(games => {
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
      console.log(weekArray);
    return weekArray;
  }
}
